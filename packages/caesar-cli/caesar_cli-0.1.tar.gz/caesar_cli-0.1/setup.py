from setuptools import setup, find_packages

setup(
    name="caesar-cli",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'caesar = caesar.cli:main',
        ],
    },
    install_requires=[],
    python_requires=">=3.13",
    author="Farhan Khan",
    author_email="ftkover9k@gmail.com",
    description="A Caesar Cipher encryption and decryption program",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ftkovr9k/caesar-cli",
    classifiers=[
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
