import os
from setuptools import setup, find_packages

REQUIREMENTS = [
    'aiogram',
    'pymongo'
]

DEPENDENCY_LINKS = []
CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(CURRENT_DIRECTORY, 'README.md')) as readme_file:
    README = readme_file.read()

SETUP_CONFIG = {
    'name': 'FN4DBot',
    'version': '0.0.1',
    'description': 'Bot',
    'long_description': README,
    'classifiers': [
        "Programming Language :: Python"
    ],
    'author': 'GregYavis',
    'author_email': 'gregyavis@gmail.com',
    'packages': find_packages(),
    'include_package_data': True,
    'zip_safe': False,
    'extras_require': {},
    'install_requires': REQUIREMENTS,
    # 'dependency_links': DEPENDENCY_LINKS
}

setup(**SETUP_CONFIG, install_requires=['aiogram'])
