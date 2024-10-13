from setuptools import setup

setup(
    name='gdpr15',
    version='0.0.1',
    py_modules=['gdpr15'],
    entry_points={
        'console_scripts': [
            'gdpr15=gdpr15:main',
        ],
    },
)
