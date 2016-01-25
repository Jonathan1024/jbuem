from setuptools import setup, find_packages

setup(
    name='jbuem',
    version='0.0',
    packages=find_packages(),
    classifiers=[
        'Private :: Do Not Upload',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.9,<2.0',
        'psycopg2',
        'gunicorn',
        'whitenoise',
    ],
)
