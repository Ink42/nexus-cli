from setuptools import setup, find_packages

setup(
    name="nexus-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml",  
    ],
    entry_points={
        "console_scripts": [
            "nexus=nexuscli.cli:main",  # Makes `nexus` command available
        ],
    },
    include_package_data=True,
    description="A modular CLI framework with plugin support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ink42",
    author_email="lindomash001@gmail.com",
    url="https://github.com/Ink42/nexus-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)