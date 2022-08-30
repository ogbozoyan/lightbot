from setuptools import setup, find_packages

setup(
    name='lightbot',
    version=version,
    description='Python interface to telegram-api.',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='dmitrii-subb',
    author_email='',
    url='https://github.com/dmitrii-subb/lightbot',
    packages = find_packages(exclude = ['tests', 'examples']),
    # license='GPL2',
    keywords='telegram python',
    install_requires=['requests'],
    extras_require={
      'json': 'ujson',
      'loguru': 'loguru',
     },
    #  classifiers=[
    #   'Development Status :: 5 - Production/Stable',
    #   'Programming Language :: Python :: 3',
    #   'Environment :: Console',
    #   'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
    # ]
)
