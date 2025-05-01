from setuptools import setup, find_packages

setup(
    name="investments-python-module",
    version="0.1.0",
    author="Ricardo Vicentini",
    author_email="ric_vicentini@hotmail.com",
    description="A Python module for investment calculations and analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ricavicentini/py-module",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "isort>=5.0",
            "flake8>=3.9",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/ricavicentini/py-module/issues",
        "Source": "https://github.com/ricavicentini/py-module",
    },
)
