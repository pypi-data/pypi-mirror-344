from setuptools import setup, find_packages

setup(
    name="prival",
    version="0.1.3",  # 新版本号，spaCy 改为可选依赖
    author="Eugene Xiang",
    author_email="you@example.com",
    description="Prompt Input Validation toolkit",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://huggingface.co/EugeneXiang/prival",
    license="MIT",
    packages=find_packages(include=["prival", "prival.*"]),
    include_package_data=True,
    install_requires=[
        "pyyaml",                   # 解析配置
        "language-tool-python",     # 语法/拼写检查
        "sentence-transformers",    # 关联度检测
    ],
    extras_require={
        "full": [
            "spacy",               # 需要 spaCy 时再安装
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
