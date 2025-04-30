from setuptools import setup, find_packages

setup(
    name="web3author",
    version="1.0.0",
    author="web3rpcs",
    author_email="",
    description="tools for web3",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
