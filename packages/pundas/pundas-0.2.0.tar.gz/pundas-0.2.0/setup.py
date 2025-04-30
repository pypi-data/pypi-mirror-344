from setuptools import setup, find_packages

setup(
    name='pundas',
    version='0.2.0',
    description='A simple library that does nothing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='emptyness',
    author_email='iwannadie@nature.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)

