from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="password-toolkit", 
    version="0.1.0",         
    author="lzc0331",
    author_email="898925970@qq.com",
    description="Secure password encryption/decryption toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/8888888b/password-module",
    packages=find_packages(),
    install_requires=[
        "cryptography>=3.4.7",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
    ],
    python_requires='>=3.6',
    keywords='password encryption security',
)
