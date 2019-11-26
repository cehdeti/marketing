import os
from setuptools import find_packages, setup


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


with open('README.md') as readme:
    README = readme.read()


def get_requirements_tests():
    with open('requirements.txt') as f:
        return f.readlines()


setup(
    name='eti_marketing',
    version='0.1.6',
    packages=find_packages(),
    include_package_data=True,
    license='None',
    description='A simple Django UI for Marketing folks to add landing pages from the admin.',
    long_description=README,
    url='https://github.com/cehdeti/marketing.git',
    author=['Mon Sucher', 'Jake Bell'],
    author_email='msucher@umn.edu',
    install_requires=[
        'django',
        'django-admin-sortable2',
        'django-ckeditor',
        'pillow',
        'requests'
    ],
    tests_require=get_requirements_tests(),
    test_suite='tests',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: None',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
