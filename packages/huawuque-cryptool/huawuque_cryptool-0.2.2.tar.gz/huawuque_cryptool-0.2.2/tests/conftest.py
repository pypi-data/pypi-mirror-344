import os
from pathlib import Path
from dotenv import load_dotenv

def pytest_configure(config):
    """配置 pytest 环境"""
    # 加载测试环境变量
    env_path = Path(__file__).parent.parent / '.env.test'
    load_dotenv(env_path) 