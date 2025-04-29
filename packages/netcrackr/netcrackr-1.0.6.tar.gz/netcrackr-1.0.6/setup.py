from setuptools import setup, find_packages

setup(
    name='netcrackr',
    version='1.0.6',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'netcrackr=netcrackr.main:cli',  # This runs the cli function in netcrackr/main.py
        ],
    },
    install_requires=[
        'rich', 
        'speedtest-cli',
    ],
)
