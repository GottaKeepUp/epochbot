try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Bot for Twitch.tv',
    'author': 'Anthony Alves',
    'url': 'https://github.com/while-loop/epochbot',
    'author_email': 'botepoch@gmail.com.',
    'version': '0.1',
    'install_requires': ['requests'],
    'packages': ['epochbot'],
    'scripts': [],
    'name': 'EpochBot'
}

setup(**config)
