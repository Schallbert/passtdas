from setuptools import setup

setup(
    name='passtdas',
    version='0.9.2',
    author='Schallbert',
    url='https://schallbert.de',
    description='Command-line application to preview CNC paths',
    py_modules=['passtdas'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'passtdas = passtdas:path_preview',
        ],
    },
)