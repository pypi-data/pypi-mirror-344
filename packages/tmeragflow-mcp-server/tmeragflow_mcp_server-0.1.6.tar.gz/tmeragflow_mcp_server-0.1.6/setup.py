from setuptools import setup, find_packages

setup(
    name="ragflow-mcp-server",
    version="0.1",
    packages=find_packages(),
    install_requires=[
         "click>=8.1.8",
 "mcp>=1.6.0",
 "python-dotenv>=1.1.0",
 "ragflow-sdk>=0.17.2",

    ],
)
