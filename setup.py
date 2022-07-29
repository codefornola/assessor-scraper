from setuptools import setup

setup(
    name='assessor-scraper',
    version='0.1',
    description='',
    url='https://github.com/codefornola/assessor-scraper',
    author='CodeForNola',
    author_email='',
    packages=['scraper'],
    install_requires=[
        "psycopg2==2.7.3.2",
        "pyproj",
        "requests",
        "Scrapy==2.6.2",
        "SQLAlchemy==1.1.15",
    ],
    zip_safe=False
)
