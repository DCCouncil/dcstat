#!/bin/bash

# Install python and dependencies
sudo apt-get install build-essential python-dev python-pip

# Install git and get the DC Stat
sudo apt-get update
sudo apt-get -y install git
git clone https://github.com/DCCouncil/dcstat.git
cd dcstat

# Install mongo (http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/)
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo service mongod start

# Install nginx-ssl
cd ~
git clone https://github.com/vzvenyach/nginx-ssl.git
cd nginx-ssl
sudo bash bootstrap.sh -p 4000 -s dcstat.dccode.gov

# Initialize the Flask App
pip install virtualenv
cd ~/dcstat
virtualenv -p python2.7 env
source env/bin/activate
pip install -r requirements.txt

# After init is done, from local system laws.bson
# scp dcstat/dump/sal/laws.bson council@dcstat.dccode.gov:/home/council/dcstat/data/laws.bson
# mongorestore --db sal data/laws.bson


# Set up the uwsgi server
pip install uwsgi

# Create directories
sudo mkdir /var/run/dcstat
sudo mkdir /var/log/dcstat-uwsgi
sudo chown council:council /var/run/dcstat
sudo chown council:council /var/log/dcstat-uwsgi
sudo mkdir /etc/dcstat-uwsgi

sudo cp ~/dcstat/conf/uwsgi.conf /etc/init/dcstat-uwsgi.conf
sudo cp ~/dcstat/conf/uwsgi.ini /etc/dcstat-uwsgi/dcstat-uwsgi.ini

sudo service dcstat-uwsgi start

# uwsgi --http 0.0.0.0:5000 --home env --wsgi-file app.py --callable app --master