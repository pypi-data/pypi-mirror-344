import os
import sqlite3
from pathlib import Path
from cryptography.fernet import Fernet
import logging
import time

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """初始化数据库"""
    try:
        # 创建安全的数据存储目录
        data_dir = Path.home() / '.cryptool' / 'data'
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # 设置目录权限
        os.chmod(data_dir, 0o700)
        
        # 数据库文件路径
        db_path = data_dir / 'crypto_keystore.db'
        
        # 如果数据库已存在，先备份
        if db_path.exists():
            backup_path = data_dir / f'crypto_keystore_{int(time.time())}.db'
            db_path.rename(backup_path)
            logger.info(f"Existing database backed up to {backup_path}")
        
        # 创建新的数据库
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # 创建密钥表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_type TEXT NOT NULL,
            key_data BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            description TEXT
        )
        ''')
        
        # 创建加密记录表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS encryption_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation_type TEXT NOT NULL,
            algorithm TEXT NOT NULL,
            key_id INTEGER,
            file_path TEXT,
            file_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (key_id) REFERENCES keys (id)
        )
        ''')
        
        # 创建用户表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
        ''')
        
        conn.commit()
        conn.close()
        
        # 设置数据库文件权限
        os.chmod(db_path, 0o600)
        
        logger.info(f"Database initialized at {db_path}")
        return str(db_path)
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

def backup_database():
    """备份数据库"""
    try:
        data_dir = Path.home() / '.cryptool' / 'data'
        db_path = data_dir / 'crypto_keystore.db'
        
        if not db_path.exists():
            logger.warning("Database file not found")
            return False
            
        # 创建备份目录
        backup_dir = data_dir / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        # 生成备份文件名
        timestamp = int(time.time())
        backup_path = backup_dir / f'crypto_keystore_{timestamp}.db'
        
        # 复制数据库文件
        import shutil
        shutil.copy2(str(db_path), str(backup_path))
        
        # 设置备份文件权限
        os.chmod(backup_path, 0o600)
        
        logger.info(f"Database backed up to {backup_path}")
        return True
        
    except Exception as e:
        logger.error(f"Database backup failed: {str(e)}")
        return False

if __name__ == "__main__":
    init_database()
    backup_database() 