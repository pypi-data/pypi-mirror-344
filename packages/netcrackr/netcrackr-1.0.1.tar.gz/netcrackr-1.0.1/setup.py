from setuptools import setup, find_packages

setup(
    name='netcrackr',
    version='1.0.1',
    packages=find_packages(),  # <- it will now find the "netcrackr" package
    install_requires=[],
    author='Eytin',
    author_email='your_email@example.com',
    description='A description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/eytin/netcrackr',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
