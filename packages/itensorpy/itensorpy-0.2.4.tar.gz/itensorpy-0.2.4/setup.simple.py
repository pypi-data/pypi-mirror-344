from setuptools import setup, find_packages

setup(
    name="itensorpy",
    version="0.2.3",
    author="iTensorPy Team",
    author_email="itensorpy@example.com",
    description="A Python package for tensor calculations in general relativity",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/itensorpy",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.7",
    install_requires=[
        "sympy>=1.7.1",
        "numpy>=1.19.0",
    ],
) 