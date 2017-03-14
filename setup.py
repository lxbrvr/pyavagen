import os
from setuptools import setup, find_packages

import pyavagen


cur_dir = os.path.abspath(os.path.dirname(__file__))

setup(
    name='pyavagen',
    url='https://github.com/abalx/pyavagen',
    version=pyavagen.__version__,
    license='MIT',
    author='Alexander Abrosimov',
    author_email='to100100100@gmail.com',
    description='Avatars generation of different types',
    long_description=open(os.path.join(cur_dir, 'README.md')).read(),
    install_requires=[
        'Pillow',
    ],
    packages=find_packages(),
    include_package_data=True,
    requires=['python (>= 3.6)',],
    keywords=['image', 'avatar'],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Topic :: Multimedia :: Graphics",
    ],
)