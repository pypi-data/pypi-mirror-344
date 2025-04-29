import os
import logging
from typing import Callable, Optional, List
import time
import tempfile

logger = logging.getLogger(__name__)

class FileHandler:
    """统一文件操作处理类"""
    
    def __init__(self):
        self.temp_files: List[str] = []
    
    def create_temp_file(self, suffix: str = None) -> str:
        """创建临时文件"""
        try:
            fd, temp_path = tempfile.mkstemp(suffix=suffix)
            os.close(fd)  # 关闭文件描述符
            self.temp_files.append(temp_path)
            return temp_path
        except Exception as e:
            logger.error(f"创建临时文件失败: {str(e)}")
            raise RuntimeError(f"创建临时文件失败: {str(e)}")
    
    def process_file(self, input_file: str, output_file: str, 
                    process_func: Callable[[bytes], bytes],
                    chunk_size: int = 1024*1024,
                    progress_callback: Optional[Callable[[int, int], None]] = None) -> None:
        """
        通用文件处理方法
        
        Args:
            input_file: 输入文件路径
            output_file: 输出文件路径
            process_func: 处理函数，接收字节数据并返回处理后的字节数据
            chunk_size: 分块大小，默认1MB
            progress_callback: 进度回调函数，接收当前进度和总大小
        """
        try:
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"输入文件不存在: {input_file}")
            
            # 获取文件大小
            total_size = os.path.getsize(input_file)
            processed_size = 0
            
            with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
                while True:
                    chunk = f_in.read(chunk_size)
                    if not chunk:
                        break
                    
                    processed_chunk = process_func(chunk)
                    f_out.write(processed_chunk)
                    
                    # 更新进度
                    processed_size += len(chunk)
                    if progress_callback:
                        progress_callback(processed_size, total_size)
                    
            logger.info(f"文件处理完成: {output_file}")
        except Exception as e:
            logger.error(f"文件处理失败: {str(e)}")
            # 如果输出文件已创建但处理失败，删除它
            if os.path.exists(output_file):
                try:
                    os.remove(output_file)
                except:
                    pass
            raise RuntimeError(f"文件处理失败: {str(e)}")
    
    def read_file(self, file_path: str, chunk_size: int = 1024*1024) -> bytes:
        """读取文件内容"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")
            with open(file_path, 'rb') as f:
                return f.read()
        except Exception as e:
            logger.error(f"读取文件失败: {str(e)}")
            raise RuntimeError(f"读取文件失败: {str(e)}")
    
    def write_file(self, file_path: str, data: bytes) -> None:
        """写入文件内容"""
        try:
            # 确保目标目录存在
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(data)
        except Exception as e:
            logger.error(f"写入文件失败: {str(e)}")
            raise RuntimeError(f"写入文件失败: {str(e)}")
    
    def cleanup_temp_file(self, file_path: str) -> None:
        """清理临时文件"""
        if not file_path or not os.path.exists(file_path):
            return
        
        max_retries = 3
        retry_delay = 0.1  # 100ms
        
        for i in range(max_retries):
            try:
                # 尝试删除文件
                os.remove(file_path)
                logger.info(f"已删除临时文件: {file_path}")
                if file_path in self.temp_files:
                    self.temp_files.remove(file_path)
                return
            except PermissionError:
                # 如果文件被占用，等待一段时间后重试
                if i < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                logger.warning(f"清理临时文件失败: 文件被占用 {file_path}")
            except Exception as e:
                logger.warning(f"清理临时文件失败: {str(e)}")
                break
    
    def cleanup_all_temp_files(self) -> None:
        """清理所有临时文件"""
        for file_path in list(self.temp_files):  # 使用列表副本进行迭代
            self.cleanup_temp_file(file_path)
    
    def __del__(self):
        """析构函数，确保清理所有临时文件"""
        self.cleanup_all_temp_files() 