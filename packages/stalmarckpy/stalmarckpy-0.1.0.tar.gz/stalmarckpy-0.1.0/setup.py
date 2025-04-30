import os
from setuptools import setup

# Let scikit-build-core handle the actual build process
setup(
    name="stalmarckpy",
    version="0.1.0",
    author="StalmarckSAT Team",
    author_email="ljdavis27@amherst.edu",
    description="Python bindings for StalmarckSAT solver",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/StalmarckSAT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)