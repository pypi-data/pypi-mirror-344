# setup.py

from setuptools import setup, find_packages

setup(
    name='gabutcat',
    version='0.1',
    packages=find_packages(),
    description="Library lucu untuk mensimulasikan kebiasaan kucing saat gabut",
    author="Nama Kamu",
    author_email="emailkamu@example.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

