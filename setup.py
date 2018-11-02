from distutils.core import setup
from vkAPI import __version__, __author__, __doc__

setup(
    name='vkAPI',
    version=__version__,
    packages=['vkAPI'],
    url='https://github.com/sakost/vkAPI',
    license='Apache 2.0',
    author=__author__,
    author_email='sakost01@gmail.com',
    description='Library for interaction with API of vk',
    long_description=__doc__,
    test_suite='tests',
    install_requires=[
        'requests>=2.20.0'
    ]
)
