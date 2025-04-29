import os
import pytest
from cryptool.core.file_handler import FileHandler
import tempfile

@pytest.fixture
def file_handler():
    return FileHandler()

@pytest.fixture
def test_file():
    # 创建临时文件
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"test data")
        return f.name

def test_read_file(file_handler, test_file):
    """测试读取文件功能"""
    data = file_handler.read_file(test_file)
    assert data == b"test data"

def test_write_file(file_handler, test_file):
    """测试写入文件功能"""
    output_file = test_file + ".out"
    try:
        file_handler.write_file(output_file, b"new data")
        with open(output_file, 'rb') as f:
            assert f.read() == b"new data"
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)

def test_process_file(file_handler, test_file):
    """测试文件处理功能"""
    output_file = test_file + ".out"
    try:
        def process_func(data):
            return data.upper()
            
        file_handler.process_file(test_file, output_file, process_func)
        with open(output_file, 'rb') as f:
            assert f.read() == b"TEST DATA"
    finally:
        if os.path.exists(output_file):
            os.remove(output_file)

def test_cleanup_temp_file(file_handler):
    """测试清理临时文件功能"""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        temp_file = f.name
        assert os.path.exists(temp_file)
        # 关闭文件以确保它不被占用
        f.close()
        file_handler.cleanup_temp_file(temp_file)
        assert not os.path.exists(temp_file) 