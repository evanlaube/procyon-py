from setuptools import setup, find_packages

setup(
    name='procyon-py',
    version='0.2.0',
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
