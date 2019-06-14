#!/bin/bash

set -ex

sudo apt-get -y update
sudo apt-get -y install build-essential python3-dev
sudo apt-get -y install python-pip

sudo apt-get -y install postgresql postgresql-contrib libpq-dev
sudo service postgresql start

sudo -u postgres createuser -s -d assessor
sudo -u postgres psql -c "ALTER USER assessor WITH PASSWORD 'assessor';"
sudo -u postgres createdb assessor
sudo -u postgres psql -c "grant all privileges on database assessor to assessor"

sudo pip install virtualenv

git clone https://github.com/codefornola/assessor-scraper.git

virtualenv -p python3 venv_scraper

. venv_scraper/bin/activate

pip install requests
pip install psycopg2==2.7.3.2
pip install pyproj
pip install SQLAlchemy==1.1.15
pip install Scrapy==1.4.0
