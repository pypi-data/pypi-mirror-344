from setuptools import setup
from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='Scan_binpy',
    version='0.0.2',
    license='MIT License',
    author='R00T.bin',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='pedromarsan06@gmail.com',
    keywords='Scan_binpy',
    description='Scan_binpy original programming',
    packages=['Scan_binpy'],
    install_requires=[],)