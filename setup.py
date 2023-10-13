from setuptools import setup

setup(
    name='CNCPathPreview',
    version='0.9.2',
    author='Schallbert',
    url='https://schallbert.de',
    description='Command-line application to preview CNC paths',
    py_modules=['cncpathpreview'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'cncpathpreview = cncpathpreview:path_preview',
        ],
    },
)