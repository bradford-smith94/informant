import re
from setuptools import setup

# read version string from main file
_version = '0.0.0'
with open('./informant/informant.py') as version_file:
    file_dat = version_file.read()
    _version = re.findall(r"^__version__ = '(\d+\.\d+\.\d+)'", file_dat, re.MULTILINE)[0]

setup(
        name='informant',
        version=_version,
        author='Bradford Smith',
        author_email='aur@bradfords.me',
        packages=['informant'],
        license='LICENSE',
        description='An Archlinux news reader and pacman hook',
        install_requires=[
            'docopt',
            'feedparser',
            'html2text',
            'python-dateutil',
            'CacheControl',
            'lockfile',
            'psutil'
        ],
        entry_points={
            'console_scripts': [
                'informant = informant.informant:main'
            ]
        },
)
