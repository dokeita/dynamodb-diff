from setuptools import setup, find_packages

setup(
    name="dynamodb_diff",
    version="0.1.0",
    author="dokeita",
    author_email="dokeita@example.com",
    description="A Python package to compare DynamoDB tables",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dokeita/dynamodb-diff",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "boto3>=1.20.0",
    ],
    entry_points={
        "console_scripts": [
            "dynamodb-diff=src.main:compare_dynamodb_tables",
        ],
    },
)
