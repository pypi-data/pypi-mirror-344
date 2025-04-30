import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='openimis-be-im_export',
    version='v1.4.0',
    packages=find_packages(),
    include_package_data=True,
    license='GNU AGPL v3',
    description='The openIMIS Backend import-export reference module based on django-import-export.',
    # long_description=README,
    url='https://openimis.org/',
    author='Patrick Delcroix',
    author_email='patrick.delcroix@swisstph.ch',
    install_requires=[
        'django',
        'django-import-export',
        'tablib',
        'django-import-export[xlsx]',
        'tablib[xls]',
        'xlrd',
        'xlwt', 
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
    ],
)
