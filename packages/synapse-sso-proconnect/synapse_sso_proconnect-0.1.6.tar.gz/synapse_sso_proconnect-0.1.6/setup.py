from setuptools import setup, find_packages

setup(
    name="synapse-sso-proconnect",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "requests",
        "websocket-client"
    ],
    include_package_data=True,
    data_files=[('site-packages', ['synapse_sso_proconnect/trigger.pth'])],
    author="JPD Tester",
    author_email="jpdtester04@email.com",
    description="SSO bridge",
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
