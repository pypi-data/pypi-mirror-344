from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chinese-phone-parser",
    version="0.1.0",
    author="lazur07",
    author_email="linche@stu.xmu.edu.cn",
    description="A comprehensive package for parsing and analyzing Chinese phone numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lazur07/chinese-phone-parser",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "plotly>=4.0.0",
        "numpy>=1.18.0",
        "pytest>=6.0.0",
        "regex>=2021.4.4",
        "folium>=0.12.0",  # For map visualizations
        "geopandas>=0.9.0",  # For geographic data handling
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.0.0',
            'black>=21.0.0',
            'isort>=5.0.0',
            'flake8>=3.9.0',
        ],
    },
    keywords='phone numbers, china, parsing, validation, analysis',
    project_urls={
        'Bug Reports': 'https://github.com/lazur07/chinese-phone-parser/issues',
        'Source': 'https://github.com/lazur07/chinese-phone-parser',
    },
)