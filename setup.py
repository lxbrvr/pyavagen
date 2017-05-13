import os
from setuptools import setup


def get_version():
    with open("pyavagen/version.py", "rt") as f:
        return f.readline().split("=")[1].strip(' "\n')

cur_dir = os.path.abspath(os.path.dirname(__file__))

setup(
    name='pyavagen',
    version=get_version(),
    author='Alexander Abrosimov',
    author_email='to100100100@gmail.com',
    url='https://github.com/abalx/pyavagen',
    description='Avatars generation of different types',
    long_description=open(os.path.join(cur_dir, 'README.rst')).read(),
    license='MIT',
    requires=['python (>= 3.6)',],
    tests_require=['pytest'],
    install_requires=[
        'Pillow',
    ],
    packages=[
        'pyavagen',
    ],
    include_package_data=True,
    keywords=['image', 'avatar'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Topic :: Multimedia :: Graphics",
    ],
)