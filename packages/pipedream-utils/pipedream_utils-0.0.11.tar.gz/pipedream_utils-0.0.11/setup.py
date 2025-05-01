from setuptools import setup, find_packages

setup(
    name='pipedream-utils',
    version='0.0.11',
    author='Dhaval Mehta',
    description='Pipedream Utils',
    long_description='Pipedream Utils',
    url='https://github.com/dhaval-mehta/pipedream-utils',
    keywords='',
    python_requires='>=3.7, <4',
    packages=find_packages(),
    install_requires=[
        'prettytable',
        'telebot',
    ],
)