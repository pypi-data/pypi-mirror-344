

from setuptools import setup, find_packages

setup(
    name="geomltools",  
    version="0.1.0",
    author="Mohammad Ali Fneich",
    author_email="fneichmohamad@gmail.com",
    description="A Python library for spatial machine learning and geospatial analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Fneich/geomltools",  
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

