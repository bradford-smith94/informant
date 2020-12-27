from setuptools import setup

setup(
        name='informant',
        version='0.3.0',
        author='Bradford Smith',
        author_email='aur@bradfords.me',
        packages=['informant'],
        license='LICENSE',
        description='An Archlinux news reader and pacman hook',
        install_requires=[
            'docopt',
            'feedparser',
            'python-dateutil',
            'CacheControl',
            'lockfile'
        ],
        entry_points={
            'console_scripts': [
                'informant = informant.informant:main'
            ]
        },
)
