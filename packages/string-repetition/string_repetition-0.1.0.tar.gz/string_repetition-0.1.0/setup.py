from setuptools import setup, find_packages
import os

# 读取 README.md 文件内容作为 long_description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="string-repetition",
    version="0.1.0",
    description="高效的字符串重复检测工具，使用前缀哈希和二分查找算法",
    long_description=long_description, # 添加 long_description
    long_description_content_type='text/markdown', # 指定内容类型为 Markdown
    author="Your Name", # 请替换为实际作者名
    author_email="your.email@example.com", # 请替换为实际邮箱
    # url="https://github.com/yourusername/string-repetition", # 可选：添加项目 URL
    packages=find_packages(exclude=["tests*", "examples*"]), # 排除测试和示例目录
    python_requires=">=3.7,<3.14",
    install_requires=[], # typing 是标准库，无需在此列出
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent", # 添加操作系统无关标识
        "Programming Language :: Python :: 3", # 通用 Python 3 标识
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules", # 添加主题分类
        "Topic :: Text Processing", # 添加主题分类
    ],
)