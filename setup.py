from setuptools import setup

setup(
    name='coinpaprika-sdk',
    version='1.1.0',
    author='Coinpaprika',
    author_email='it@coinpaprika.com',
    description='Official coinpaprika API Python client',
    packages=['coinpaprika'],
    url='https://github.com/coinpaprika/coinpaprika-api-python-client',
    license='Apache License 2.0',
    install_requires=['requests'],
    python_requires='>=3.9',
    keywords='coinpaprika api cryptocurrency',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
