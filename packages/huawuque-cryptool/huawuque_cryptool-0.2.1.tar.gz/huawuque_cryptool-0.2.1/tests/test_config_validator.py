from cryptool.utils.config_validator import ConfigValidator

def test_validate_env_config():
    """测试环境变量配置验证"""
    validator = ConfigValidator()
    
    # 测试有效的配置
    valid_config = {
        'AES_KEY_LENGTH': '256',
        'RSA_KEY_SIZE': '2048',
        'KEY_STORAGE_PATH': 'D:\\path\\to\\keys',
        'LOG_FILE': 'D:\\path\\to\\logs\\crypto.log',
        'DB_HOST': 'localhost',
        'DB_PORT': '3306',
        'MASTER_KEY': 'test_master_key',
        'KEY_ROTATION_DAYS': '60',
        'LOG_LEVEL': 'INFO'
    }
    assert validator.validate_env_config(valid_config) is True
    
    # 测试无效的AES密钥长度
    invalid_aes_config = valid_config.copy()
    invalid_aes_config['AES_KEY_LENGTH'] = '512'
    assert validator.validate_env_config(invalid_aes_config) is False
    
    # 测试无效的RSA密钥大小
    invalid_rsa_config = valid_config.copy()
    invalid_rsa_config['RSA_KEY_SIZE'] = '512'
    assert validator.validate_env_config(invalid_rsa_config) is False
    
    # 测试无效的日志级别
    invalid_log_config = valid_config.copy()
    invalid_log_config['LOG_LEVEL'] = 'INVALID'
    assert validator.validate_env_config(invalid_log_config) is False

def test_validate_database_config():
    """测试数据库配置验证"""
    validator = ConfigValidator()
    
    # 测试有效的配置
    valid_config = {
        'DB_HOST': 'localhost',
        'DB_PORT': '3306',
        'DB_USER': 'test_user',
        'DB_NAME': 'test_db',
        'DB_PASSWORD': 'Test123!'
    }
    assert validator.validate_database_config(valid_config) is True
    
    # 测试缺少必需参数
    missing_param_config = valid_config.copy()
    del missing_param_config['DB_HOST']
    assert validator.validate_database_config(missing_param_config) is False
    
    # 测试弱密码
    weak_password_config = valid_config.copy()
    weak_password_config['DB_PASSWORD'] = 'weak'
    assert validator.validate_database_config(weak_password_config) is False 