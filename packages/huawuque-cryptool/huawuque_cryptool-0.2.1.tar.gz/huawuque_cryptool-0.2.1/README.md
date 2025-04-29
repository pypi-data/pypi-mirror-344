# huawuque-cryptool

一个具有图形界面的加密工具，支持多种加密算法。

> **注意：PyPI 包名为 `huawuque-cryptool`，导入时仍然使用 `cryptool` 作为模块名。**

## 功能特点

- 支持 AES、RSA 和混合加密
- 直观的图形用户界面
- 文件加密和解密
- Base64 编码/解码
- 密钥管理系统
- 详细的操作日志
- 支持密钥轮换
- 安全的密钥存储

## 安装

```bash
pip install huawuque-cryptool==0.2.1
```

## 使用方法

1. 命令行启动：
```bash
cryptool
```

2. 或在 Python 中导入：
```python
from cryptool.gui.main import main
main()
```

## 环境要求

- Python 3.8 或更高版本
- 操作系统：Windows/Linux/macOS

## 配置

1. 创建 `.env` 文件，包含以下配置：
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=crypto_keystore
MASTER_KEY=your_master_key
```

2. 确保 `logs` 目录存在并可写

## 开发

1. 克隆仓库：
```bash
git clone https://github.com/hwq/cryptool.git
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行测试：
```bash
pytest
```

## 更新日志

### v0.2.0
- 包名正式更名为 huawuque-cryptool
- 适配 PyPI 上传规范
- 更新Python版本要求到3.8+
- 添加密钥轮换功能
- 改进密钥存储安全性
- 优化GUI界面
- 增加更多测试用例

## 许可证

MIT License 