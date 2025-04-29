from setuptools import setup, find_packages

setup(
    name="netcrackr",
    version="1.0.3",
    author="Eytin",
    description="Network live monitor with ping, speedtest, and traceroute",
    packages=find_packages(),
    install_requires=[
        "speedtest-cli",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "netcrackr=netcrackr:cli",
        ],
    },
    python_requires=">=3.7",
)
