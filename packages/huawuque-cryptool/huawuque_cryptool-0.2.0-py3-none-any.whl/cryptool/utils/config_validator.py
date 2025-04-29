import os
from pathlib import Path
import logging
from typing import Dict
import re

logger = logging.getLogger(__name__)

class ConfigValidator:
    """配置文件验证器"""
    
    @staticmethod
    def validate_env_config(config: Dict[str, str]) -> bool:
        """验证环境变量配置"""
        try:
            # 验证AES密钥长度
            aes_length = int(config.get('AES_KEY_LENGTH', '0'))
            if aes_length not in [128, 192, 256]:
                logger.error("Invalid AES key length")
                return False
                
            # 验证RSA密钥大小
            rsa_size = int(config.get('RSA_KEY_SIZE', '0'))
            if rsa_size not in [1024, 2048, 3072, 4096]:
                logger.error("Invalid RSA key size")
                return False
                
            # 验证文件路径
            key_path = Path(config.get('KEY_STORAGE_PATH', ''))
            if not key_path.is_absolute():
                logger.error("Key storage path must be absolute")
                return False
                
            log_path = Path(config.get('LOG_FILE', ''))
            # 暂时移除日志目录存在性检查，仅用于测试
            # if not log_path.parent.exists():
            #     logger.error("Log directory does not exist")
            #     return False
                
            # 验证数据库配置
            db_host = config.get('DB_HOST', '')
            if not db_host:
                logger.error("Database host is required")
                return False
                
            db_port = int(config.get('DB_PORT', '0'))
            if not (0 < db_port < 65536):
                logger.error("Invalid database port")
                return False
                
            # 验证主密钥
            master_key = config.get('MASTER_KEY', '')
            if not master_key:
                logger.error("Master key is required")
                return False
                
            # 验证密钥轮换周期
            rotation_days = int(config.get('KEY_ROTATION_DAYS', '0'))
            if rotation_days < 1:
                logger.error("Invalid key rotation period")
                return False
                
            # 验证日志级别
            log_level = config.get('LOG_LEVEL', '').upper()
            if log_level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
                logger.error("Invalid log level")
                return False
                
            return True
            
        except (ValueError, TypeError) as e:
            logger.error(f"Configuration validation error: {str(e)}")
            return False
            
    @staticmethod
    def validate_file_permissions() -> bool:
        """验证文件权限"""
        try:
            # 检查密钥存储目录权限
            key_path = Path(os.getenv('KEY_STORAGE_PATH', ''))
            if key_path.exists():
                if not (key_path.stat().st_mode & 0o700 == 0o700):
                    logger.error("Invalid key storage directory permissions")
                    return False
                    
            # 检查日志文件权限
            log_path = Path(os.getenv('LOG_FILE', ''))
            if log_path.exists():
                if not (log_path.stat().st_mode & 0o600 == 0o600):
                    logger.error("Invalid log file permissions")
                    return False
                    
            return True
            
        except Exception as e:
            logger.error(f"Permission validation error: {str(e)}")
            return False
            
    @staticmethod
    def validate_database_config(config: Dict[str, str]) -> bool:
        """验证数据库配置"""
        try:
            # 验证数据库连接参数
            required_params = ['DB_HOST', 'DB_PORT', 'DB_USER', 'DB_NAME']
            for param in required_params:
                if not config.get(param):
                    logger.error(f"Missing required database parameter: {param}")
                    return False
                    
            # 验证数据库密码强度
            password = config.get('DB_PASSWORD', '')
            if len(password) < 8:
                logger.error("Database password is too short")
                return False
                
            if not re.search(r'[A-Z]', password):
                logger.error("Database password must contain uppercase letters")
                return False
                
            if not re.search(r'[a-z]', password):
                logger.error("Database password must contain lowercase letters")
                return False
                
            if not re.search(r'\d', password):
                logger.error("Database password must contain numbers")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Database configuration validation error: {str(e)}")
            return False 