from setuptools import setup, find_packages

def getVersion():
    version_file = 'procyon/__version__.py'
    with open(version_file) as f:
        globals_dict = {}
        exec(f.read(), globals_dict)
        return globals_dict['__version__']

setup(
    name='procyon-py',
    version=getVersion(),
    description='A terminal based UI library for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/evanlaube/procyon-py',
    author='Evan Laube',
    author_email='laubeevan@gmail.com',
    license='GPL 3.0',
    packages=find_packages(),
    install_requires=[

    ],
    extras_require={
        'windows': [
            'windows-curses',
        ],
        'dev': [
            'pytest',
        ],
    },
    test_suite='tests',
)
