from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='developer',
    version='0.1.0',
    author='PC',
    description='Simple underlying object logic.',
    packages=find_packages(),
    install_requires=required,
)