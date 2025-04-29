from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="huawuque-cryptool",
    version="0.2.2",
    author="hwq",
    author_email="hwq@example.com",
    description="一个具有GUI界面的加密工具，支持AES、RSA和混合加密",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hwq/cryptool",
    project_urls={
        "Bug Tracker": "https://github.com/hwq/cryptool/issues",
        "Documentation": "https://github.com/hwq/cryptool/wiki",
        "Source Code": "https://github.com/hwq/cryptool",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Security :: Cryptography",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pycryptodome>=3.9.0",
        "python-dotenv>=0.19.0",
        "cryptography>=41.0.0",
        "mysql-connector-python>=8.0.0",
        "psutil>=5.9.0",
        "tkinter",
    ],
    entry_points={
        "console_scripts": [
            "cryptool=cryptool.gui.main:main",
            "cryptool-gui=cryptool.run_gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "cryptool": ["*.ini", "*.env", "*.log"],
    },
    keywords="encryption, cryptography, security, gui, aes, rsa",
    license="MIT",
    zip_safe=False,
) 