import setuptools

from distutils.core import setup

setup(
    name='action_mapper',
    version='0.8',
    author='KK',
    author_email='kandhan.kuhan@gmail.com',
    packages=['action_mapper', 'action_mapper.adapters'],
    license='LICENSE.txt',
    long_description=open('README.txt').read(),
    install_requires=[
        "Django >= 1.1.1",
        "cerberus",
    ],
)