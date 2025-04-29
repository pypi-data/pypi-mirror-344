import pytest
import os
from cryptool.core.asymmetric import RSAHandler
from cryptool.core.key_management import KeyManager
import tempfile
import uuid

@pytest.fixture
def key_manager():
    """创建KeyManager实例"""
    km = KeyManager()
    return km

@pytest.fixture
def rsa_handler(key_manager):
    """创建RSAHandler实例"""
    return RSAHandler(key_manager)

@pytest.fixture
def key_pair(rsa_handler):
    """生成RSA密钥对"""
    key_id = str(uuid.uuid4())
    pub_key_id, priv_key_id = rsa_handler.generate_keypair(key_id)
    return (pub_key_id, priv_key_id)

@pytest.fixture
def test_file():
    """创建临时测试文件"""
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'wb') as tmp:
        tmp.write(b"test data for encryption")
    yield path
    try:
        os.remove(path)
    except OSError:
        pass

def test_generate_keypair(rsa_handler):
    """测试RSA密钥对生成"""
    key_id = str(uuid.uuid4())
    pub_key_id, priv_key_id = rsa_handler.generate_keypair(key_id)
    assert pub_key_id.endswith('_public')
    assert priv_key_id.endswith('_private')
    # 验证密钥存在
    pub_key_data, pub_algo = rsa_handler.key_manager.get_key(pub_key_id)
    priv_key_data, priv_algo = rsa_handler.key_manager.get_key(priv_key_id)
    assert pub_key_data is not None
    assert priv_key_data is not None
    assert pub_algo == 'RSA-PUBLIC'
    assert priv_algo == 'RSA-PRIVATE'

def test_encrypt_decrypt(rsa_handler, key_pair):
    """测试基本的加密解密功能"""
    test_data = b"test data"
    pub_key_id, priv_key_id = key_pair
    # 加密
    encrypted_data = rsa_handler.encrypt(test_data, pub_key_id)
    assert isinstance(encrypted_data, bytes)
    # 解密
    decrypted_data = rsa_handler.decrypt(encrypted_data, priv_key_id)
    assert decrypted_data == test_data

def test_sign_verify(rsa_handler, key_pair):
    """测试数字签名功能"""
    test_data = b"test data"
    pub_key_id, priv_key_id = key_pair
    # 签名
    signature = rsa_handler.sign(test_data, priv_key_id)
    assert isinstance(signature, bytes)
    # 验证
    assert rsa_handler.verify(test_data, signature, pub_key_id)
    # 测试错误的数据
    assert not rsa_handler.verify(b"wrong data", signature, pub_key_id)

def test_encrypt_decrypt_large_data(rsa_handler, key_pair):
    """测试大数据的分块加密解密"""
    large_data = b"A" * 1000  # 创建一个大于RSA块大小的数据
    pub_key_id, priv_key_id = key_pair
    # 加密
    encrypted_data = rsa_handler.encrypt(large_data, pub_key_id)
    assert isinstance(encrypted_data, bytes)
    # 解密
    decrypted_data = rsa_handler.decrypt(encrypted_data, priv_key_id)
    assert decrypted_data == large_data

def test_encrypt_decrypt_file(rsa_handler, key_pair, test_file):
    """测试文件加密解密功能"""
    pub_key_id, priv_key_id = key_pair
    output_file = test_file + ".enc"
    decrypted_file = test_file + ".dec"
    try:
        # 加密文件
        rsa_handler.encrypt_file(test_file, output_file, pub_key_id)
        assert os.path.exists(output_file)
        # 解密文件
        rsa_handler.decrypt_file(output_file, decrypted_file, priv_key_id)
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

def test_invalid_key_id(rsa_handler):
    """测试使用无效的密钥ID"""
    test_data = b"test data"
    with pytest.raises(RuntimeError, match="RSA加密失败"):
        rsa_handler.encrypt(test_data, "invalid_key_id")

def test_invalid_key_format(rsa_handler, key_pair):
    """测试使用无效格式的密钥"""
    pub_key_id, _ = key_pair
    # 存储一个无效格式的密钥
    rsa_handler.key_manager.store_key("invalid_key", b"invalid key data", "RSA-PUBLIC")
    test_data = b"test data"
    with pytest.raises(RuntimeError, match="RSA加密失败"):
        rsa_handler.encrypt(test_data, "invalid_key") 