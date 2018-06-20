from pathlib import Path
from setuptools import setup, find_packages

version = '1.0.0'

name = 'postgis_loader'
description = 'load layers data from postgis'
url = 'https://gitlab.com/atelier-cartographique/be-lb/postgis-loader'
author = 'Atelier Cartographique'
author_email = 'contact@atelier-cartographique.be'
license = 'Affero GPL3'

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
]

install_requires = ['django']

packages = find_packages()

setup(
    name=name,
    version=version,
    url=url,
    license=license,
    description=description,
    author=author,
    author_email=author_email,
    packages=packages,
    install_requires=install_requires,
    classifiers=classifiers,
)
