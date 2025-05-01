from setuptools import setup, find_packages

setup(
    name='pygame-setup',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['inquirer'],
    entry_points={
        'console_scripts': [
            'pygame-setup=pygame_setup.main:run'
        ]
    },
)