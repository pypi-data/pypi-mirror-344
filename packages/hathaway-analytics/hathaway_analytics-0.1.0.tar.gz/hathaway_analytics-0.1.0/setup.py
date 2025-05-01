from setuptools import setup, find_packages

setup(
    name='hathaway_analytics',
    version='0.1.0',
    description='Minimal non-blocking data analytics collection for Flask apps',
    author='Isaac Hathaway',
    author_email='isaaczhathaway@gmail.com',
    license='GPL-3.0-only',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'requests',
        'user-agents',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)
