from setuptools import setup, find_packages

setup(
    name="rooq",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask",
    ],
    license="MIT",
    entry_points={
        "console_scripts": [
            "rooq=rooq:run_app",
        ],
    },
    author='Naser Jamal',
    author_email='naser.dll@hotmail.com',
    description='automatically create files/folders according to provided structure',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/naserjamal/rooq',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
