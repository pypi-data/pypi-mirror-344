from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import HMAC, SHA256
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from .symmetric import AESHandler
from .asymmetric import RSAHandler
from .hashing import SHA256Handler
from .key_management import KeyManager
from .file_handler import FileHandler
import os
from typing import Tuple, Optional, Any, Union
from Crypto.PublicKey.RSA import RsaKey
import logging
from Crypto.PublicKey import RSA

logger = logging.getLogger(__name__)

class HybridHandler:
    def __init__(self, key_manager: KeyManager, aes_handler: AESHandler, rsa_handler: RSAHandler):
        self.key_manager = key_manager
        self.aes_handler = aes_handler
        self.rsa_handler = rsa_handler
        self.hash = SHA256Handler()
        self.file_handler = FileHandler()
    
    def encrypt(self, plaintext: Union[str, bytes], key_id: str) -> dict:
        """
        混合加密
        :param plaintext: 明文
        :param key_id: 密钥ID
        :return: 包含加密结果的字典
        """
        try:
            # 生成AES密钥
            aes_key = get_random_bytes(32)  # 256-bit key
            
            # 检查key_id是否已经包含'_public'后缀
            rsa_key_id = key_id
            if not key_id.endswith('_public'):
                rsa_key_id = key_id + '_public'
            
            # 使用RSA加密AES密钥
            encrypted_key = self.rsa_handler.encrypt(aes_key, rsa_key_id)
            
            # 为AES密钥生成临时ID并存储
            temp_aes_key_id = f"temp_aes_key_{os.urandom(4).hex()}"
            self.key_manager.store_key(temp_aes_key_id, aes_key, 'AES-256')
            
            # 使用AES加密明文
            ciphertext, iv, tag = self.aes_handler.encrypt(plaintext, temp_aes_key_id)
            
            # 计算HMAC
            hmac_key = get_random_bytes(32)
            hmac = HMAC.new(hmac_key, digestmod=SHA256)
            hmac.update(ciphertext)
            hmac_signature = hmac.digest()
            
            # 使用RSA加密HMAC密钥
            encrypted_hmac_key = self.rsa_handler.encrypt(hmac_key, rsa_key_id)
            
            # 清理临时密钥
            self.key_manager.revoke_key(temp_aes_key_id)
            
            result = {
                'ciphertext': ciphertext,
                'encrypted_key': encrypted_key,
                'iv': iv,
                'tag': tag,
                'hmac_key': encrypted_hmac_key,
                'hmac_signature': hmac_signature
            }
            # --- 添加日志 ---
            logger.debug(f"Encrypt: enc_key hash: {SHA256.new(encrypted_key).hexdigest()}")
            logger.debug(f"Encrypt: hmac_key hash: {SHA256.new(encrypted_hmac_key).hexdigest()}")
            # --- 日志结束 ---
            return result
        except Exception as e:
            raise RuntimeError(f"混合加密失败: {str(e)}")
    
    def decrypt(self, encrypted_data: dict, key_id: str) -> Union[str, bytes]:
        """
        混合解密
        :param encrypted_data: 加密数据字典
        :param key_id: 密钥ID
        :return: 解密后的明文
        """
        temp_aes_key_id = None
        try:
            # 检查key_id是否已经包含'_private'后缀
            rsa_key_id = key_id
            if not key_id.endswith('_private'):
                rsa_key_id = key_id + '_private'
            
            # 解密AES密钥
            aes_key = self.rsa_handler.decrypt(encrypted_data['encrypted_key'], rsa_key_id)
            
            # 解密HMAC密钥并验证HMAC
            hmac_key = self.rsa_handler.decrypt(encrypted_data['hmac_key'], rsa_key_id)
            hmac = HMAC.new(hmac_key, digestmod=SHA256)
            hmac.update(encrypted_data['ciphertext'])
            try:
                hmac.verify(encrypted_data['hmac_signature'])
            except ValueError:
                raise RuntimeError("HMAC验证失败，数据可能被篡改")
            
            # 为解密的AES密钥生成临时ID并存储
            temp_aes_key_id = f"temp_aes_key_{os.urandom(4).hex()}"
            self.key_manager.store_key(temp_aes_key_id, aes_key, 'AES-256')
            
            # 使用AES解密
            plaintext = self.aes_handler.decrypt(
                encrypted_data['ciphertext'],
                encrypted_data['iv'],
                encrypted_data['tag'],
                temp_aes_key_id
            )
            
            # --- 添加日志 ---
            logger.debug(f"Decrypt: enc_key hash: {SHA256.new(encrypted_data['encrypted_key']).hexdigest()}")
            logger.debug(f"Decrypt: hmac_key hash: {SHA256.new(encrypted_data['hmac_key']).hexdigest()}")
            # --- 日志结束 ---
            
            return plaintext
        except Exception as e:
            raise RuntimeError(f"混合解密失败: {str(e)}")
        finally:
            # 确保无论解密是否成功都清理临时密钥
            if temp_aes_key_id:
                try:
                    self.key_manager.revoke_key(temp_aes_key_id)
                except Exception as e:
                    logger.warning(f"清理临时AES密钥失败: {str(e)}")
    
    def encrypt_file(self, input_file: str, output_file: str, key_id: str) -> None:
        """使用混合加密方法加密文件"""
        temp_file = None
        try:
            logger.info(f"开始混合加密文件: {input_file}")
            
            # 检查输入文件是否存在
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"输入文件不存在: {input_file}")
            
            # 生成AES密钥
            logger.info("生成AES密钥")
            aes_key = get_random_bytes(32)  # 256-bit key
            
            # 为AES密钥生成临时ID并存储
            temp_aes_key_id = f"temp_aes_key_{os.urandom(4).hex()}"
            logger.info(f"存储临时AES密钥: {temp_aes_key_id}")
            self.key_manager.store_key(temp_aes_key_id, aes_key, 'AES-256')
            
            # 使用RSA加密AES密钥
            logger.info("使用RSA加密AES密钥")
            try:
                # 检查key_id是否已经包含'_public'后缀
                rsa_key_id = key_id
                if not key_id.endswith('_public'):
                    rsa_key_id = key_id + '_public'
                logger.info(f"使用RSA公钥ID: {rsa_key_id}")
                
                encrypted_key = self.rsa_handler.encrypt(aes_key, rsa_key_id)
                logger.info("AES密钥加密成功")
            except Exception as e:
                logger.error(f"RSA加密AES密钥失败: {e}")
                raise RuntimeError(f"RSA加密AES密钥失败: {str(e)}")
            
            # 使用AES加密文件
            logger.info("使用AES加密文件")
            temp_file = output_file + '.temp'
            self.aes_handler.encrypt_file(input_file, temp_file, temp_aes_key_id)
            
            # 组合加密结果
            with open(temp_file, 'rb') as f:
                encrypted_data = f.read()
            
            # 写入最终文件
            with open(output_file, 'wb') as f:
                # 写入加密密钥长度
                f.write(len(encrypted_key).to_bytes(4, 'big'))
                # 写入加密后的AES密钥
                f.write(encrypted_key)
                # 写入加密后的数据
                f.write(encrypted_data)
            
            logger.info(f"文件加密成功: {output_file}")
            
        except Exception as e:
            logger.error(f"文件加密失败: {str(e)}")
            raise RuntimeError(f"文件加密失败: {str(e)}")
        finally:
            # 清理临时文件
            self.file_handler.cleanup_temp_file(temp_file)
    
    def decrypt_file(self, input_file: str, output_file: str, key_id: str) -> None:
        """使用混合加密方法解密文件"""
        temp_file = None
        try:
            with open(input_file, 'rb') as f:
                # 读取加密密钥长度
                key_length = int.from_bytes(f.read(4), 'big')
                # 读取加密后的AES密钥
                encrypted_key = f.read(key_length)
                # 读取加密后的数据
                encrypted_data = f.read()
            
            # 检查key_id是否已经包含'_private'后缀
            rsa_key_id = key_id
            if not key_id.endswith('_private'):
                rsa_key_id = key_id + '_private'
            logger.info(f"使用RSA私钥ID: {rsa_key_id}")
            
            # 使用RSA解密AES密钥
            aes_key = self.rsa_handler.decrypt(encrypted_key, rsa_key_id)
            
            # 为AES密钥生成临时ID并存储
            temp_aes_key_id = f"temp_aes_key_{os.urandom(4).hex()}"
            logger.info(f"存储临时AES密钥: {temp_aes_key_id}")
            self.key_manager.store_key(temp_aes_key_id, aes_key, 'AES-256')
            
            # 将加密数据写入临时文件
            temp_file = input_file + '.temp'
            self.file_handler.write_file(temp_file, encrypted_data)
            
            # 使用AES解密文件
            self.aes_handler.decrypt_file(temp_file, output_file, temp_aes_key_id)
            
            logger.info(f"文件解密成功: {output_file}")
            
        except Exception as e:
            logger.error(f"文件解密失败: {str(e)}")
            raise RuntimeError(f"文件解密失败: {str(e)}")
        finally:
            # 清理临时文件
            self.file_handler.cleanup_temp_file(temp_file)
