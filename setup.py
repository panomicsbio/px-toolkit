from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setup(
    name='px-toolkit',
    version='0.0.1',
    author='Radu Andrei Tanasa',
    author_email='radu@geneguard.bio',
    license='MIT',
    description='CLI for interacting with Panomics',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/panomicsbio/px-toolkit',
    py_modules=['px', 'app'],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires='>=3.10',
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        px=px:cli
    '''
)
