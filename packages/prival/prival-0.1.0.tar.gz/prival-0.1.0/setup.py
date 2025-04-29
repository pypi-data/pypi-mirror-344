# setup.py
from setuptools import setup, find_packages

setup(
    name="prival",
    version="0.1.0",              # 发布的版本号
    author="Peng Xiang",
    author_email="eugene.p.xiang@gmail.com",
    description="Prompt Input Validation toolkit",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://huggingface.co/EugeneXiang/prival",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyyaml",
        "spacy",
        "language-tool-python",
        "openpromptinject",
        "sentence-transformers",
        # …根据实际需要补充依赖…
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)