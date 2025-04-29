import pytest
import os
from cryptool.core.symmetric import AESHandler
from cryptool.core.key_management import KeyManager

@pytest.fixture
def aes_handler(key_manager):
    manager, _ = key_manager
    return AESHandler(manager)

@pytest.fixture
def key_manager():
    manager = KeyManager()
    key_id = "test_key"
    manager.generate_key("AES-256", key_id)
    return manager, key_id

@pytest.fixture
def test_file(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("test data for encryption")
    return str(test_file)

def test_encrypt_decrypt(aes_handler, key_manager):
    """测试基本加密解密功能"""
    manager, key_id = key_manager
    data = b"test data"
    encrypted_data, iv, tag = aes_handler.encrypt(data, key_id)
    decrypted_data = aes_handler.decrypt(encrypted_data, iv, tag, key_id)
    assert decrypted_data == data

def test_encrypt_decrypt_file(aes_handler, key_manager, test_file, tmp_path):
    """测试文件加密解密"""
    manager, key_id = key_manager
    output_file = str(tmp_path / "encrypted.txt")
    decrypted_file = str(tmp_path / "decrypted.txt")
    
    aes_handler.encrypt_file(test_file, output_file, key_id)
    assert os.path.exists(output_file)
    
    aes_handler.decrypt_file(output_file, decrypted_file, key_id)
    assert os.path.exists(decrypted_file)
    assert open(decrypted_file, 'rb').read() == open(test_file, 'rb').read()

def test_empty_file(aes_handler, key_manager, tmp_path):
    """测试空文件处理"""
    manager, key_id = key_manager
    empty_file = str(tmp_path / "empty.txt")
    open(empty_file, 'w').close()
    
    output_file = str(tmp_path / "encrypted_empty.txt")
    decrypted_file = str(tmp_path / "decrypted_empty.txt")
    
    aes_handler.encrypt_file(empty_file, output_file, key_id)
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) == 0
    
    aes_handler.decrypt_file(output_file, decrypted_file, key_id)
    assert os.path.exists(decrypted_file)
    assert os.path.getsize(decrypted_file) == 0

def test_invalid_decryption(aes_handler, key_manager):
    """测试无效解密"""
    manager, key_id = key_manager
    data = b"test data"
    encrypted_data, iv, tag = aes_handler.encrypt(data, key_id)
    
    # 使用错误的IV
    with pytest.raises(RuntimeError, match="AES解密失败"):
        aes_handler.decrypt(encrypted_data, b"wrong_iv", tag, key_id)
    
    # 使用错误的tag
    with pytest.raises(RuntimeError, match="AES解密失败"):
        aes_handler.decrypt(encrypted_data, iv, b"wrong_tag", key_id)

def test_invalid_key(key_manager):
    """测试无效密钥"""
    manager, _ = key_manager
    handler = AESHandler(manager)
    with pytest.raises(RuntimeError, match="AES加密失败：无效的密钥ID"):
        handler.encrypt(b"test data", "invalid_key")

def test_nonexistent_file(key_manager):
    """测试不存在的文件"""
    manager, _ = key_manager
    handler = AESHandler(manager)
    with pytest.raises(RuntimeError, match="AES文件加密失败：输入文件不存在"):
        handler.encrypt_file("nonexistent.txt", "output.txt", "test_key") 