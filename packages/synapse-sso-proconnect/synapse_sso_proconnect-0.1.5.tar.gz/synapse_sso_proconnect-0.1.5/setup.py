from setuptools import setup, find_packages
from setuptools.command.install import install
import os

setup(
    name="synapse-sso-proconnect",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        "requests",
        "websocket-client"
    ],
    data_files=[("site-packages", ["synapse_sso_proconnect/synapse_sso_proconnect.pth"])],
    include_package_data=True,
    author="JPD Tester",
    author_email="jpdtester04@email.com",
    description="A short description of what your package does",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jpd/synapse-sso-proconnect",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
