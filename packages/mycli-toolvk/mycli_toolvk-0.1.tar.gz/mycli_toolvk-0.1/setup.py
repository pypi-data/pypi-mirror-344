from setuptools import setup, find_packages

setup(
    name='mycli-toolvk',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mycli = mycli.cli:main'
        ]
    },
    install_requires=[],
    author='AnandaKrishnanGr',
    description='AWS CLI verification and deployment helper',
    python_requires='>=3.6',
)
