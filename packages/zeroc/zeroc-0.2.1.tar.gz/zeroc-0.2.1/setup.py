from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='zeroc',
    version='0.2.1',
    author='Fidal PalamParambil',
    author_email='mrfidal@proton.me',
    description='Run C code directly from Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['zeroc'],
    install_requires=[],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Source": "https://github.com/mrfidal/zeroc",
    },
)