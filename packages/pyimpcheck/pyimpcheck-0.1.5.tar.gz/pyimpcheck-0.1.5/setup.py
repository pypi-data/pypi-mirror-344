from setuptools import setup, find_packages
import os

current_dir = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(current_dir, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Module used for check if the library is available, if not, it will install it automatically"

setup(
    name="pyimpcheck",
    version="0.1.5",
    author="Cheng",
    author_email="xcxhxxg08@gmail.com",
    description="Module used for check if the library is available, if not, it will install it automatically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hibro114/pyimp",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],  # Add dependencies if needed
    entry_points={},  # Add console scripts if needed
)