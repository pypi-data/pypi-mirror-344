from setuptools import setup, find_packages

#Add Readme File to PyPi:
with open("README.md", "r") as f:
    description = f.read()

setup(
    name='httprequestor',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        #add dependencies here.
        # e.g. 'numpy>=1.11.1
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)