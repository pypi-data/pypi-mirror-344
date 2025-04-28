from setuptools import setup, find_packages

setup(
    name="SMA_Package",  # name on PyPI
    version="0.1.0",
    packages=find_packages(),  # automatically finds your .py files inside folders
    install_requires=[],  # dependencies (if any)
    author="Rocks",
    author_email="you@example.com",
    description="A short description of your package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/yourpackage",  # link to your repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)
