from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from .key_management import KeyManager
from .file_handler import FileHandler
from typing import Union, Tuple
import os
import logging

logger = logging.getLogger(__name__)

class AESHandler:
    def __init__(self, key_manager: KeyManager):
        self.key_manager = key_manager
        self.file_handler = FileHandler()
    
    def encrypt(self, data: bytes, key_id: str) -> Tuple[bytes, bytes, bytes]:
        """加密数据"""
        try:
            key, algorithm = self.key_manager.get_key(key_id)
            if not key or not algorithm or algorithm != 'AES-256':
                raise RuntimeError("AES加密失败：无效的密钥ID")
            
            # 生成随机IV
            iv = os.urandom(16)
            cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
            
            # 加密数据
            ciphertext, tag = cipher.encrypt_and_digest(data)
            return ciphertext, iv, tag
        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"AES加密失败：{str(e)}")
    
    def decrypt(self, ciphertext: bytes, iv: bytes, tag: bytes, key_id: str) -> bytes:
        """解密数据"""
        try:
            key, algorithm = self.key_manager.get_key(key_id)
            if not key:
                raise RuntimeError("AES解密失败：无效的密钥ID")
            
            cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
            try:
                return cipher.decrypt_and_verify(ciphertext, tag)
            except ValueError as e:
                raise RuntimeError(f"AES解密失败：{str(e)}")
        except Exception as e:
            raise RuntimeError(f"AES解密失败：{str(e)}")
    
    def encrypt_file(self, input_file: str, output_file: str, key_id: str) -> None:
        """加密文件"""
        try:
            if not os.path.exists(input_file):
                raise RuntimeError("AES文件加密失败：输入文件不存在")
            
            if os.path.getsize(input_file) == 0:
                with open(output_file, 'wb') as f:
                    f.write(b'')
                return
            
            key, algorithm = self.key_manager.get_key(key_id)
            if not key:
                raise RuntimeError("AES文件加密失败：无效的密钥ID")
            
            # 生成随机IV
            iv = os.urandom(16)
            cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
            
            with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
                # 写入IV
                f_out.write(iv)
                
                # 加密数据
                while True:
                    chunk = f_in.read(1024)
                    if not chunk:
                        break
                    ciphertext = cipher.encrypt(chunk)
                    f_out.write(ciphertext)
                
                # 写入认证标签
                tag = cipher.digest()
                f_out.write(tag)
        except Exception as e:
            raise RuntimeError(f"AES文件加密失败：{str(e)}")
    
    def decrypt_file(self, input_file: str, output_file: str, key_id: str) -> None:
        """解密文件"""
        try:
            if not os.path.exists(input_file):
                raise RuntimeError("AES文件解密失败：输入文件不存在")
            
            if os.path.getsize(input_file) == 0:
                with open(output_file, 'wb') as f:
                    f.write(b'')
                return
            
            key, algorithm = self.key_manager.get_key(key_id)
            if not key:
                raise RuntimeError("AES文件解密失败：无效的密钥ID")
            
            with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
                # 读取IV
                iv = f_in.read(16)
                if len(iv) != 16:
                    raise RuntimeError("AES文件解密失败：无效的IV")
                
                cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
                
                # 读取文件内容（除了最后的tag）
                encrypted_data = f_in.read()
                if len(encrypted_data) < 16:
                    raise RuntimeError("AES文件解密失败：文件内容过短")
                
                # 分离加密数据和tag
                ciphertext = encrypted_data[:-16]
                tag = encrypted_data[-16:]
                
                try:
                    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
                    f_out.write(decrypted_data)
                except ValueError as e:
                    raise RuntimeError(f"AES文件解密失败：{str(e)}")
        except Exception as e:
            raise RuntimeError(f"AES文件解密失败：{str(e)}")