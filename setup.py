"""
PtWebkit
--------

Webkit based webclient.

"""
from setuptools import setup, find_packages


setup(
    name='PtWebkit',
    version='0.1',
    url='https://github.com/',
    license='mit',
    author='Joseph',
    author_email='serafinjp@gmail.com',
    description='Webkit based webclient.',
    long_description=__doc__,
    data_files=[('ghost', ['README.rst',])],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    use_2to3=True,
)