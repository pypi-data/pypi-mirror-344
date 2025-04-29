from setuptools import setup, find_packages

setup(
    name="netcrackr",  # Package name
    version="1.0.0",  # Version number
    packages=find_packages(),  # Automatically find all packages in the directory
    install_requires=[],  # List of external dependencies (if any)
    entry_points={  # If you want to create a command-line tool
        'console_scripts': [
            'netcrackr=netcrackr:main',  # Adjust if you have a main() function
        ],
    },
    author="Eytin",  # Author name
    description="A powerful tool for network analysis and cracking.",
    long_description=open("README.md").read(),  # Long description from README.md
    long_description_content_type="text/markdown",  # Format for README file
    url="https://github.com/eytin/netcrackr",  # Your project's URL (e.g., GitHub repository)
    classifiers=[  # Metadata about your package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
