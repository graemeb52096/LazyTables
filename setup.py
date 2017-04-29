from setuptools import setup, find_packages

setup(
    name = 'LazyTable',
    version='0.0.1',
    description='Database manager',
    url='https://github.com/graemeb52096/LazyTables',
    author='Graeme Bates',
    author_email='batesg1996@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Database :: Development tools',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],
    keywords='Mysql sql database',
    packages=['LazyTable'],
)