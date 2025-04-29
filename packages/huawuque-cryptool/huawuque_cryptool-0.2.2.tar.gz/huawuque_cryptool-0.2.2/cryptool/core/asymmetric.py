# 非对称加密模块
"""
RSA非对称加密模块
支持密钥生成、加密解密、数字签名、PEM格式密钥序列化
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from .key_management import KeyManager
from typing import Union, Tuple
import logging
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from Crypto.PublicKey.RSA import RsaKey

logger = logging.getLogger(__name__)

class RSAHandler:
    def __init__(self, key_manager: KeyManager):
        self.key_manager = key_manager
    
    def generate_keypair(self, key_id: str) -> Tuple[str, str]:
        """生成RSA密钥对并存储"""
        try:
            # 生成RSA密钥对
            key = RSA.generate(2048)
            
            # 导出公钥和私钥
            public_key = key.publickey().export_key()
            private_key = key.export_key()
            
            # 生成密钥ID
            public_key_id = f"{key_id}_public"
            private_key_id = f"{key_id}_private"
            
            # 存储密钥
            self.key_manager.store_key(public_key_id, public_key, "RSA-PUBLIC")
            self.key_manager.store_key(private_key_id, private_key, "RSA-PRIVATE")
            
            return public_key_id, private_key_id
        except Exception as e:
            logger.error(f"生成RSA密钥对失败: {e}")
            raise RuntimeError(f"生成RSA密钥对失败: {str(e)}")
    
    def encrypt(self, data: Union[str, bytes], key_id: str) -> bytes:
        """RSA加密"""
        try:
            # 获取公钥（直接获取二进制数据）
            key_data, algorithm = self.key_manager.get_key(key_id)
            if not key_data:
                raise ValueError(f"未找到密钥: {key_id}")
            
            # 验证RSA密钥格式
            if not self.key_manager.verify_rsa_key(key_data):  
                raise ValueError("无效的RSA公钥格式")
            
            # 加载公钥
            try:
                public_key = RSA.import_key(key_data)
            except ValueError as e:
                logger.error(f"导入RSA公钥失败: {e}")
                raise ValueError(f"无效的RSA公钥格式: {str(e)}")
            
            cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
            
            # 如果数据是字符串，转换为字节
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            # 计算最大块大小
            max_chunk_size = (public_key.size_in_bytes() - 2 * SHA256.digest_size - 2)
            
            # 如果数据小于最大块大小，直接加密
            if len(data) <= max_chunk_size:
                return cipher.encrypt(data)
            
            # 分块加密
            encrypted_chunks = []
            for i in range(0, len(data), max_chunk_size):
                chunk = data[i:i + max_chunk_size]
                try:
                    encrypted_chunk = cipher.encrypt(chunk)
                    encrypted_chunks.append(encrypted_chunk)
                except Exception as e:
                    logger.error(f"加密块失败: {e}")
                    raise RuntimeError(f"加密块失败: {str(e)}")
            
            return b''.join(encrypted_chunks)
        except Exception as e:
            logger.error(f"RSA加密失败: {e}")
            raise RuntimeError(f"RSA加密失败: {str(e)}")
    
    def decrypt(self, encrypted_data: bytes, key_id: str = None, private_key_obj: RsaKey = None) -> bytes:
        """RSA解密. 可以接受 key_id 或预加载的 private_key_obj.
        
        Args:
            encrypted_data: 要解密的密文数据.
            key_id: 私钥的ID (如果未提供 private_key_obj).
            private_key_obj: 预先加载的RSA私钥对象 (如果提供，则忽略 key_id).
            
        Returns:
            解密后的明文字节.
            
        Raises:
            ValueError: 如果密钥无效、未找到或密文长度不正确.
            RuntimeError: 如果解密操作失败.
        """
        private_key = None
        log_key_ref = "unknown" # 用于日志记录

        try:
            if private_key_obj:
                private_key = private_key_obj
                log_key_ref = f"provided object (key size: {private_key.size_in_bits()})"
                logger.info(f"使用提供的私钥对象进行解密。")
            elif key_id:
                log_key_ref = key_id
                private_key_id = key_id
                # 保留之前的检查，以防直接调用此方法
                if not key_id.endswith('_private'):
                    logger.warning(f"解密时可能使用了非私钥ID: {key_id}. 追加 '_private'.")
                    private_key_id = key_id + '_private'
                    log_key_ref = private_key_id # 更新日志参考
                    
                key_data, algorithm = self.key_manager.get_key(private_key_id)
                if not key_data or algorithm != 'RSA-PRIVATE':
                    raise ValueError(f"未找到或类型错误的RSA私钥: {private_key_id} (Algo: {algorithm})")
                
                try:
                    private_key = RSA.import_key(key_data)
                    log_key_ref += f" (loaded, size: {private_key.size_in_bits()})" # 添加加载信息
                except ValueError as e:
                    logger.error(f"导入RSA私钥失败: {e}")
                    raise ValueError(f"无效的RSA私钥格式 ({private_key_id}): {str(e)}")
            else:
                 raise ValueError("RSA解密需要提供 key_id 或 private_key_obj")

            # --- 解密逻辑 --- 
            cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
            # RSA 密钥的字节大小，也是每个加密块的大小
            chunk_size = private_key.size_in_bytes()
            logger.info(f"尝试解密 RSA 数据块. 密钥参考: {log_key_ref}, 块大小: {chunk_size}, 密文总长: {len(encrypted_data)}")

            # 检查密文总长度是否是块大小的整数倍
            if len(encrypted_data) % chunk_size != 0:
                raise ValueError(f"RSA密文总长度 ({len(encrypted_data)}) 不是块大小 ({chunk_size}) 的整数倍")

            decrypted_chunks = []
            try:
                for i in range(0, len(encrypted_data), chunk_size):
                    chunk = encrypted_data[i:i + chunk_size]
                    decrypted_chunk = cipher.decrypt(chunk)
                    decrypted_chunks.append(decrypted_chunk)
                
                # 拼接解密后的块
                decrypted_data = b''.join(decrypted_chunks)
                return decrypted_data
            except ValueError as e:
                 # ValueError 通常表示解密失败 (e.g., 密钥错误, 数据损坏)
                 logger.error(f"RSA块解密操作失败 ({log_key_ref}): {e}", exc_info=True)
                 raise RuntimeError(f"RSA解密失败: {str(e)}") from e
            except Exception as e:
                 logger.error(f"RSA块解密时发生意外错误 ({log_key_ref}): {e}", exc_info=True)
                 raise RuntimeError(f"RSA解密时发生意外错误: {str(e)}") from e
                 
        except Exception as e:
             logger.error(f"RSA解密方法失败 ({log_key_ref}): {e}", exc_info=True)
             if isinstance(e, (ValueError, RuntimeError)):
                 raise
             else:
                 raise RuntimeError(f"RSA解密失败: {str(e)}") from e
    
    def sign(self, data: Union[str, bytes], key_id: str) -> bytes:
        """RSA签名"""
        try:
            # 获取私钥
            key_data, algorithm = self.key_manager.get_key(key_id)
            if not key_data:
                raise ValueError(f"未找到密钥: {key_id}")
            
            # 加载私钥
            private_key = RSA.import_key(key_data)
            
            # 如果数据是字符串，转换为字节
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            # 计算哈希
            h = SHA256.new(data)
            
            # 签名
            signature = pkcs1_15.new(private_key).sign(h)
            return signature
        except Exception as e:
            raise RuntimeError(f"RSA签名失败: {str(e)}")
    
    def verify(self, data: Union[str, bytes], signature: bytes, key_id: str) -> bool:
        """RSA验证签名"""
        try:
            # 获取公钥
            key_data, algorithm = self.key_manager.get_key(key_id)
            if not key_data:
                raise ValueError(f"未找到密钥: {key_id}")
            
            # 加载公钥
            public_key = RSA.import_key(key_data)
            
            # 如果数据是字符串，转换为字节
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            # 计算哈希
            h = SHA256.new(data)
            
            # 验证签名
            try:
                pkcs1_15.new(public_key).verify(h, signature)
                return True
            except (ValueError, TypeError):
                return False
        except Exception as e:
            raise RuntimeError(f"RSA验证签名失败: {str(e)}")
    
    def encrypt_file(self, input_file: str, output_file: str, key_id: str, chunk_size: int = 1024*1024) -> None:
        """RSA分块加密文件"""
        try:
            # 获取公钥
            key_data, algorithm = self.key_manager.get_key(key_id)
            if not key_data:
                raise ValueError(f"未找到密钥: {key_id}")
            
            # 加载公钥
            public_key = RSA.import_key(key_data)
            cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
            
            # 计算RSA加密的最大块大小
            max_chunk_size = (public_key.size_in_bytes() - 2 * SHA256.digest_size - 2)
            
            with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
                while True:
                    chunk = f_in.read(max_chunk_size)
                    if not chunk:
                        break
                    
                    # 加密数据块
                    encrypted_chunk = cipher.encrypt(chunk)
                    # 写入加密块大小和加密块
                    f_out.write(len(encrypted_chunk).to_bytes(4, 'big'))
                    f_out.write(encrypted_chunk)
                
        except Exception as e:
            raise RuntimeError(f"RSA文件加密失败: {str(e)}")
    
    def decrypt_file(self, input_file: str, output_file: str, key_id: str) -> None:
        """RSA分块解密文件"""
        try:
            # 获取私钥
            key_data, algorithm = self.key_manager.get_key(key_id)
            if not key_data:
                raise ValueError(f"未找到密钥: {key_id}")
            
            # 加载私钥
            try:
                private_key = RSA.import_key(key_data)
            except ValueError:
                # 如果导入失败，尝试解码后再导入
                try:
                    key_str = key_data.decode('utf-8')
                    private_key = RSA.import_key(key_str)
                except:
                    raise ValueError("无效的RSA私钥格式")
            
            cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
            
            with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
                while True:
                    # 读取块大小
                    size_data = f_in.read(4)
                    if not size_data:
                        break
                    
                    chunk_size = int.from_bytes(size_data, 'big')
                    # 读取加密块
                    encrypted_chunk = f_in.read(chunk_size)
                    if not encrypted_chunk:
                        break
                    
                    # 解密数据块
                    try:
                        decrypted_chunk = cipher.decrypt(encrypted_chunk)
                        f_out.write(decrypted_chunk)
                    except Exception as e:
                        raise RuntimeError(f"解密块失败: {str(e)}")
                
        except Exception as e:
            raise RuntimeError(f"RSA文件解密失败: {str(e)}")

    def hybrid_encrypt_file(self, input_file: str, output_file: str, key_id: str) -> None:
        """
        使用混合加密方法加密文件（RSA+AES）
        :param input_file: 输入文件路径
        :param output_file: 输出文件路径
        :param key_id: RSA密钥ID
        """
        temp_file = None
        try:
            # 生成AES密钥
            aes_key = get_random_bytes(32) 
            
            # 使用RSA加密AES密钥
            encrypted_key = self.encrypt(aes_key, key_id)
            
            # 使用AES加密文件
            from cryptool.core.symmetric import AESHandler
            aes_handler = AESHandler()
            
            # 创建临时文件
            temp_file = output_file + '.temp'
            aes_handler.encrypt_file(input_file, temp_file, aes_key)
            
            # 将加密后的AES密钥写入文件头部
            with open(temp_file, 'rb') as f:
                encrypted_data = f.read()
            
            with open(output_file, 'wb') as f:
                # 写入加密密钥长度
                f.write(len(encrypted_key).to_bytes(4, 'big'))
                # 写入加密后的AES密钥
                f.write(encrypted_key)
                # 写入加密后的数据
                f.write(encrypted_data)
                
        except Exception as e:
            raise RuntimeError(f"混合加密失败: {str(e)}")
        finally:
            # 清理临时文件
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception as e:
                    logger.warning(f"清理临时文件失败: {str(e)}")

    def hybrid_decrypt_file(self, input_file: str, output_file: str, key_id: str) -> None:
        """
        使用混合加密方法解密文件（RSA+AES）
        :param input_file: 输入文件路径
        :param output_file: 输出文件路径
        :param key_id: RSA密钥ID
        """
        temp_file = None
        try:
            with open(input_file, 'rb') as f:
                # 读取加密密钥长度
                key_length = int.from_bytes(f.read(4), 'big')
                # 读取加密后的AES密钥
                encrypted_key = f.read(key_length)
                # 读取加密后的数据
                encrypted_data = f.read()
            
            # 使用RSA解密AES密钥
            aes_key = self.decrypt(encrypted_key, key_id + '_private')
            
            # 将加密数据写入临时文件
            temp_file = input_file + '.temp'
            with open(temp_file, 'wb') as f:
                f.write(encrypted_data)
            
            # 使用AES解密文件
            from cryptool.core.symmetric import AESHandler
            aes_handler = AESHandler()
            aes_handler.decrypt_file(temp_file, output_file, aes_key)
                    
        except Exception as e:
            raise RuntimeError(f"混合解密失败: {str(e)}")
        finally:
            # 清理临时文件
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception as e:
                    logger.warning(f"清理临时文件失败: {str(e)}")

