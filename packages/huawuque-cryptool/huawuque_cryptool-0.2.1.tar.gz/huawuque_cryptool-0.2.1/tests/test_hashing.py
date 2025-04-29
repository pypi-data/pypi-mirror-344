import pytest
import os
from cryptool.core.hashing import SHA256Handler
import tempfile

@pytest.fixture
def sha256_handler():
    """创建SHA256Handler实例"""
    return SHA256Handler()

@pytest.fixture
def test_file():
    """创建临时测试文件"""
    fd, path = tempfile.mkstemp()
    with os.fdopen(fd, 'wb') as tmp:
        tmp.write(b"test data for hashing")
    yield path
    try:
        os.remove(path)
    except OSError:
        pass

def test_compute_hash(sha256_handler):
    """测试基本的哈希计算功能"""
    test_data = b"test data"
    hash_value = sha256_handler.compute_hash(test_data)
    assert isinstance(hash_value, bytes)
    assert len(hash_value) == 32  # SHA-256哈希值长度为32字节

def test_compute_hmac(sha256_handler):
    """测试HMAC计算功能"""
    test_data = b"test data"
    key = b"test key"
    hmac_value = sha256_handler.compute_hmac(test_data, key)
    assert isinstance(hmac_value, bytes)
    assert len(hmac_value) == 32  # HMAC-SHA256输出长度为32字节

def test_verify_hmac(sha256_handler):
    """测试HMAC验证功能"""
    test_data = b"test data"
    key = b"test key"
    hmac_value = sha256_handler.compute_hmac(test_data, key)
    assert sha256_handler.verify(test_data, hmac_value, key)
    # 测试错误的数据
    assert not sha256_handler.verify(b"wrong data", hmac_value, key)
    # 测试错误的密钥
    assert not sha256_handler.verify(test_data, hmac_value, b"wrong key")

def test_pbkdf2_derive(sha256_handler):
    """测试PBKDF2密钥派生功能"""
    password = "test password"
    key, salt = sha256_handler.pbkdf2_derive(password)
    assert isinstance(key, bytes)
    assert isinstance(salt, bytes)
    assert len(key) == 32  # 派生密钥长度为32字节
    assert len(salt) == sha256_handler.salt_length  # 盐值长度应该匹配配置

def test_verify_hash(sha256_handler):
    """测试哈希值验证功能"""
    test_data = b"test data"
    hash_value = sha256_handler.compute_hash(test_data)
    assert sha256_handler.verify_hash(test_data, hash_value)
    # 测试错误的数据
    assert not sha256_handler.verify_hash(b"wrong data", hash_value)

def test_file_hash(sha256_handler, test_file):
    """测试文件哈希计算功能"""
    hash_value = sha256_handler.file_hash(test_file)
    assert isinstance(hash_value, bytes)
    assert len(hash_value) == 32
    # 验证相同文件产生相同的哈希值
    second_hash = sha256_handler.file_hash(test_file)
    assert hash_value == second_hash

def test_generate_random_salt(sha256_handler):
    """测试随机盐值生成功能"""
    salt1 = sha256_handler.generate_random_salt()
    salt2 = sha256_handler.generate_random_salt()
    assert isinstance(salt1, bytes)
    assert isinstance(salt2, bytes)
    assert len(salt1) == 16  # 默认盐值长度
    assert salt1 != salt2  # 两次生成的盐值应该不同

def test_invalid_hash_algorithm():
    """测试不支持的哈希算法"""
    with pytest.raises(ValueError, match="不支持的哈希算法"):
        SHA256Handler(hash_algorithm="INVALID") 