from setuptools import setup, find_packages

setup(
    name="simple-package-gxb",
    version="0.1.0",
    packages=find_packages(),
    author="GXB",
    author_email="example@example.com",
    description="一个简单的测试包",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/simple-package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 