from setuptools import setup, find_packages

setup(
    name='netcrackr',
    version='1.0.4',
    packages=find_packages(),  # This will automatically include the netcrackr package
    install_requires=[
        'speedtest-cli',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'netcrackr=netcrackr.main:cli',  # This tells setuptools to call netcrackr.main.cli
        ],
    },
)
