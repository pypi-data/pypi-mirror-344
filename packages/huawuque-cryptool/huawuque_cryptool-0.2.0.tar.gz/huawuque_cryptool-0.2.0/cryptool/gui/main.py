import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv
from cryptool.gui.main_window import CryptoGUI

# 配置日志
def setup_logging():
    """配置日志系统"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 确保日志文件存在并可写
    log_file = log_dir / "cryptool.log"
    if not log_file.exists():
        log_file.touch()
    
    # 配置日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # 测试日志
    logger = logging.getLogger(__name__)
    logger.info("日志系统初始化完成")

def check_environment():
    """检查运行环境"""
    logger = logging.getLogger(__name__)
    
    # 检查环境变量
    if not load_dotenv('.env'):
        logger.error("无法加载环境变量文件")
        return False
        
    required_vars = ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"缺少必要的环境变量: {', '.join(missing_vars)}")
        return False
        
    return True

def main():
    """主程序入口"""
    # 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # 检查环境
        if not check_environment():
            sys.exit(1)
            
        # 启动GUI
        logger.info("启动加密工具")
        app = CryptoGUI()
        app.mainloop()
        
    except Exception as e:
        logger.error(f"程序运行时错误: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("程序退出")

if __name__ == '__main__':
    main() 