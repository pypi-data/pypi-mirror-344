from setuptools import setup, find_packages

setup(
    name='logo_plugin',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
        'pymongo>=4.0.0,<5.0.0'
    ],
    entry_points={
        'console_scripts': [
            'logo-fetch = logo_plugin.service:main',
        ],
    },
)