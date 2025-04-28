from setuptools import setup, find_packages

setup(
    name='cchenutils',
    version='0.8.29',
    keywords=('utils'),
    description='cc personal use',
    license='MIT License',
    install_requires=['selenium', 'ordered-set', 'dask'],
    include_package_data=True,
    zip_safe=True,

    author='chench',
    author_email='phantomkidding@gmail.com',

    packages=find_packages(),
    platforms='any',
)