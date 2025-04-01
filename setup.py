import os

from setuptools import __version__, find_packages, setup

init_path = os.path.join(os.path.dirname(__file__), "ncatbot_sync/__init__.py")

with open(init_path, "r") as f:
    exec(f.read())

version = __version__


setup(
    name="ncatbot_sync",
    version=version,
    author="木子",
    author_email="lyh_02@foxmail.com",
    description="NapCat Python SDK, 提供一站式开发部署方案",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/liyihao1110/ncatbot_sync",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.10",
    install_requires=[
        "websocket-client >= 1.8.0",
        "PyYAML >= 6.0.2",
        "colorama >= 0.4.6"
    ],
)
