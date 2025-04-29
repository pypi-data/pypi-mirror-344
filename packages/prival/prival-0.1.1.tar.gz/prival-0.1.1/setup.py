from setuptools import setup, find_packages

setup(
    name="prival",
    version="0.1.1",              # 新版本号
    author="Eugene Xiang",
    author_email="you@example.com",
    description="Prompt Input Validation toolkit",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://huggingface.co/EugeneXiang/prival",
    license="MIT",
    packages=find_packages(),     # 确保 prival/ 被打包
    include_package_data=True,
    install_requires=[
        "pyyaml",
        "spacy",
        "language-tool-python",
        "sentence-transformers",
        # "openpromptinject",  # 去掉这一行
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)