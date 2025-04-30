from setuptools import setup, find_packages

setup(
    name='bayes-crypto-sdk',
    version='0.1.0',
    author='afaan',
    author_email='afaan@bayes.global',
    description='SDK for MongoDB sentiment access',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://pypi.org/project/bayes-crypto-sdk/',
    packages=find_packages(),
    install_requires=[
        'pymongo>=3.12'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
