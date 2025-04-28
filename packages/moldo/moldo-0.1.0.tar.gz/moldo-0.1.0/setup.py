from setuptools import setup, find_packages

setup(
    name="moldo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "antlr4-python3-runtime>=4.13.1",
    ],
    entry_points={
        "console_scripts": [
            "moldo=moldo.cli:main",
        ],
    },
    author="Mutiibwa Grace Peter",
    author_email="mutiibwa.grace@example.com",
    description="A visual programming language that compiles to Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mutiibwa/moldo",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Compilers",
    ],
    python_requires=">=3.8",
) 