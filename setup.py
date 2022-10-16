from setuptools import setup, find_packages

setup(
    name='indexxo',
    version='0.0.1',
    description='File indexer',
    author='Sad Ellie',
    author_email='sadellie@gmail.com',
    url='https://github.com/sadellie/indexxo',
    packages=find_packages(include=['server', 'server.*']),
    install_requires=[
        'autopep8==1.7.0',
        'click==8.1.3',
        'Flask==2.2.2',
        'Flask-Cors==3.0.10',
        'itsdangerous==2.1.2',
        'Jinja2==3.1.2',
        'MarkupSafe==2.1.1',
        'peewee==3.15.3',
        'pip==22.0.2',
        'pycodestyle==2.9.1',
        'setuptools==59.6.0',
        'six==1.16.0',
        'toml==0.10.2',
        'Werkzeug==2.2.2',
    ],
    entry_points={
        'console_scripts': ['indexxo=server.main:main']
    }
)
