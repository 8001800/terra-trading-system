#!/bin/sh

# Install and start Docker
sudo yum update -y
sudo yum install -y docker git
sudo service docker start
sudo usermod -aG docker ec2-user

# Install docker-compose
sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install celery env

yes | sudo yum install python36
sudo alternatives --set python /usr/bin/python3.6
#sudo rm /usr/bin/python
#sudo ln /usr/bin/python3.6 /usr/bin/python
yes | sudo yum install python36-devel

sudo pip install celery
yes | sudo yum install gcc
sudo pip install python-binance
sudo pip install kafka-python
sudo pip install redis==2.10.6
