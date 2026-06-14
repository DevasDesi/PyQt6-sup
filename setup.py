from setuptools import setup, find_packages

setup(
    name='shoes-exam',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyQt6>=6.4',
        'PyMySQL>=1.0',
    ],
    entry_points={
        'console_scripts': [
            'shoes-exam=shoes_exam.main:main',
        ],
    },
)
