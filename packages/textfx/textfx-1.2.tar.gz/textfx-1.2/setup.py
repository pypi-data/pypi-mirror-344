from setuptools import setup, find_packages
from pathlib import Path

# محتوای فایل README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="textfx",
    version="1.2",
    packages=find_packages(),
    install_requires=[],
    description="textfx is a Python library for creating dynamic and visually engaging text effects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ilia Karimi",
    url="https://github.com/iliakarimi/textfx",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
