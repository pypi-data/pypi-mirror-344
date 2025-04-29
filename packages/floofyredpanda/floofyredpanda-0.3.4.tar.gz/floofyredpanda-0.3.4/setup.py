from setuptools import setup, find_packages

setup(
    name="floofyredpanda",
    version="0.3.4",
    description="load & train .pt models on any inputs/files, emit any outputs",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "torch>=1.7.0",
        "soundfile>=0.10.0",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
