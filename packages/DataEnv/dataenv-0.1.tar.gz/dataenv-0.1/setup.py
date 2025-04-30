from setuptools import setup, find_packages

setup(
    name='DataEnv',
    version='0.1',
    author='ProgVM',
    author_email='progvminc@gmail.com',
    description='The package for doing many sorts of operations with data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ProgVM/DataEnv/',
    packages=find_packages(),
    license='Apache License 2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
