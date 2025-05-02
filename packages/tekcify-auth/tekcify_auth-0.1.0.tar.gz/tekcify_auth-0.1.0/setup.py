from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tekcify-auth",
    version="0.1.0",
    author="Agboola Olamidipupo Favour",
    author_email="dipoagboola2019@campux.io",
    description="Authentication library for Tekcify services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tekcify/tekcify-auth-python-library",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        "tekcify_auth": ["py.typed"],
    },
    install_requires=[
        "requests>=2.25.0",
    ],
) 