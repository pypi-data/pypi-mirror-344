from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chinese-phone-parser",
    version="0.1.0",
    author="Lazur",
    author_email="linche@stu.xmu.edu.cn",
    description="A Python package for cleaning and analyzing Chinese phone numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lazur07/chinese-phone-parser",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "plotly>=4.0.0",
        "numpy>=1.18.0",
    ],
)