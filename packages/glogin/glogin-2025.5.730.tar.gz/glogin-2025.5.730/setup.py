from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    install_requires = [line.strip() for line in f.readlines()]

setup(
    name='glogin',
    version='2025.5.0730',
    packages=find_packages(),
    install_requires=install_requires,
    author='tcp2',
    description='python package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.5'
)
