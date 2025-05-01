from setuptools import setup, find_packages

setup(
    name="datacmp",
    version="0.1.0",
    author="Moustafa Mohamed",
    author_email="moustafa.mh.mohamed@gmail.com",
    description="A lightweight library for exploring and cleaning datasets for ML workflows.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MoustafaMohamed01/datacmp",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "tabulate>=0.8.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
