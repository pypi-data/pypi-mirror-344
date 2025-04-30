from setuptools import setup, find_packages
import os

# Read the README for a detailed project description
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="syntaxmatrix",
    version="1.2.0",
    author="Bob Nti",
    author_email="bob.nti@syntaxmatrix.com",
    description="SyntaxMUI: A customizable UI framework for Python AI Assistant Projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bobganti/SyntaxMatrixDemo",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.0.0",
        "requests>=2.0.0",
        "markdown>=3.3.0",
        "matplotlib>=3.5.0",
        "plotly>=5.0.0",
        "openai>=0.27.0",
        "PyPDF2>=1.26.0",
        "numpy>=1.21.0",
    ],
    extras_require={
        "advanced_nlp": ["transformers>=4.0.0", "torch>=1.9.0"],
        "data": ["pandas>=1.3.0"],
        "testing": ["pytest", "pytest-flask"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
