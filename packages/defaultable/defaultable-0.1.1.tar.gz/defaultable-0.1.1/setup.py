from setuptools import setup, find_packages

setup(
    name='defaultable',
    version='0.1.1',
    description='A simple Python package for defaultable abstract base classes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tal Fiderer',
    author_email='talfiderer@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
