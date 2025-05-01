from setuptools import setup, find_packages

setup(
    name = 'addmylog',
    version='0.1',
    packages=find_packages(),
    
)

from setuptools import setup, find_packages
import pathlib

# Read the contents of your README file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='addmylog',
    version='0.2.0',
    description='A library for creating text logs',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Sharad Ingle',
    author_email='shrdingle@gmail.com',
    url='https://github.com/Sharad2124Ingle/arial_distance',
    packages=find_packages(),
    install_requires=[
        # list dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
