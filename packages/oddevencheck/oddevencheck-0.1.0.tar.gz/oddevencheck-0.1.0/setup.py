from setuptools import setup, find_packages

setup(
    name="oddevencheck",
    version="0.1.0",
    description="A package to check if a number is odd or even",
    author="Abinash",
    packages=find_packages(),
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)