from setuptools import setup, find_packages

setup(
    name="rooq",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flake8",
        "openai",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "rooq=rooq.cli:main",
        ],
    },
    author="Naser Jamal",
    author_email="naser.dll@hotmail.com",
    description="A wrapper on flake8 that uses GPT-4o mini to automatically fix code",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NaserJamal/rooq",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)