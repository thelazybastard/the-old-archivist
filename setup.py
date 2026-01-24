from setuptools import setup

setup(
    name='TheOldArchivist',
    version='1.0.0',
    py_modules=['main'],
    entry_points={
        'console_scripts': [
            'do-my-bidding=main:main',
        ],
    },
)