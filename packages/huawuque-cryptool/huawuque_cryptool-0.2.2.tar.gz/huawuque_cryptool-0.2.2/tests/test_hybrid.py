import pytest
import os
from cryptool.core.hybrid import HybridHandler
from cryptool.core.key_management import KeyManager
from cryptool.core.symmetric import AESHandler
from cryptool.core.asymmetric import RSAHandler
import tempfile
import uuid

@pytest.fixture
def key_manager():
    """创建KeyManager实例"""
    km = KeyManager()
    return km

@pytest.fixture
def aes_handler(key_manager):
    """创建AESHandler实例"""
    return AESHandler(key_manager)

@pytest.fixture
def rsa_handler(key_manager):
    """创建RSAHandler实例"""
    return RSAHandler(key_manager)

@pytest.fixture
def hybrid_handler(key_manager, aes_handler, rsa_handler):
    """创建HybridHandler实例"""
    return HybridHandler(key_manager, aes_handler, rsa_handler)

@pytest.fixture
def test_keys(rsa_handler):
    # 生成测试用RSA密钥对
    key_id = "test_key"
    rsa_handler.generate_keypair(key_id)
    return key_id

@pytest.fixture
def key_pair(rsa_handler):
    """生成RSA密钥对"""
    key_id = str(uuid.uuid4())
    pub_key_id, priv_key_id = rsa_handler.generate_keypair(key_id)
    return (key_id, pub_key_id, priv_key_id)

@pytest.fixture
def test_file():
    """创建临时测试文件"""
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'wb') as tmp:
        tmp.write(b"test data for hybrid encryption")
    yield path
    try:
        os.remove(path)
    except OSError:
        pass

def test_encrypt_decrypt(hybrid_handler, test_keys):
    """测试基本的加密解密功能"""
    test_data = b"Hello, World!"
    
    # 加密
    encrypted_data = hybrid_handler.encrypt(test_data, test_keys)
    
    # 验证加密数据包含所有必要字段
    assert isinstance(encrypted_data, dict)
    assert all(key in encrypted_data for key in ['ciphertext', 'encrypted_key', 'iv', 'tag'])
    
    # 解密
    decrypted_data = hybrid_handler.decrypt(encrypted_data, test_keys)
    assert decrypted_data == test_data

def test_encrypt_decrypt_file(hybrid_handler, key_pair, test_file):
    """测试文件的混合加密解密功能"""
    key_id, _, _ = key_pair
    output_file = test_file + ".enc"
    decrypted_file = test_file + ".dec"
    try:
        # 加密文件
        hybrid_handler.encrypt_file(test_file, output_file, key_id)
        assert os.path.exists(output_file)
        # 解密文件
        hybrid_handler.decrypt_file(output_file, decrypted_file, key_id)
        assert os.path.exists(decrypted_file)
        # 验证内容
        with open(test_file, 'rb') as f:
            original_content = f.read()
        with open(decrypted_file, 'rb') as f:
            decrypted_content = f.read()
        assert original_content == decrypted_content
    finally:
        # 清理测试文件
        for f in [output_file, decrypted_file]:
            try:
                os.remove(f)
            except OSError:
                pass

def test_encrypt_decrypt_large_data(hybrid_handler, test_keys):
    """测试大数据量的加密解密"""
    large_data = os.urandom(1024 * 1024)  # 1MB的随机数据
    
    encrypted_data = hybrid_handler.encrypt(large_data, test_keys)
    decrypted_data = hybrid_handler.decrypt(encrypted_data, test_keys)
    
    assert decrypted_data == large_data

def test_invalid_key(hybrid_handler, test_keys):
    """测试使用错误的密钥进行解密"""
    test_data = b"Test data"
    encrypted_data = hybrid_handler.encrypt(test_data, test_keys)
    
    # 使用不存在的密钥尝试解密
    with pytest.raises(RuntimeError):
        hybrid_handler.decrypt(encrypted_data, "nonexistent_key")

def test_empty_data(hybrid_handler, test_keys):
    """测试空数据的加密解密"""
    test_data = b""
    
    encrypted_data = hybrid_handler.encrypt(test_data, test_keys)
    decrypted_data = hybrid_handler.decrypt(encrypted_data, test_keys)
    
    assert decrypted_data == test_data 