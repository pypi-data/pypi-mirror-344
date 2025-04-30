from setuptools import setup, find_packages

setup(
    name="Terminal-Colorify",  # The name of your package
    version="1.1.1",  # Version of your package
    packages=find_packages(),  # Automatically find the packages
    install_requires=[],  # Any external dependencies (leave empty if none)
    description="A simple Python module for adding colors to text in the terminal",  # Short description
    long_description=open("README.md").read(),  # Read long description from README.md
    long_description_content_type="text/markdown",  # Type of README file
    author="amiryona",  # Your name
    author_email="amiryona6@gmail.com",  # Your email
    classifiers=[  # Classification for PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
)
