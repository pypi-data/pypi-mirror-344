from setuptools import setup, find_packages

setup(
    name="numpynp-avina02",
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'tensorflow',
        'numpy',
        'matplotlib',
        'Pillow'
    ],
    author='soham',
    description='Plant disease detection using CNN',
)
