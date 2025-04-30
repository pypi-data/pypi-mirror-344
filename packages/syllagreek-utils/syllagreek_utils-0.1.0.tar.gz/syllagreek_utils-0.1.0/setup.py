from setuptools import setup, find_packages

setup(
    name="syllagreek_utils",
    version="0.1.0",
    description="Greek preprocessing and syllabification utilities for SyllaMoBert",
    author="Your Name",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    license="MIT"
)