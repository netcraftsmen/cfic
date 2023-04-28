# README.md

## References

Useful references for Event Driven Ansible

* 6 Guidelines for creating custom source plugins for Event-Driven Ansible! <https://www.youtube.com/watch?v=4f7ARUnVZmY>
* AIOKafka <https://aiokafka.readthedocs.io/en/stable/api.html>

## Installation

Installation documentation when installing on Digital Ocean 

ubuntu-s-2vcpu-2gb-nyc1-01 / 2 GB Memory / 60 GB Disk / NYC1 - Ubuntu 20.04 (LTS) x64

# https://www.oracle.com/java/technologies/downloads/
# https://askubuntu.com/questions/1430509/how-to-install-jdk-19-on-ubuntu-22-04-lts
#
# wget https://download.oracle.com/java/20/latest/jdk-20_linux-x64_bin.deb
#
# Installing on Digital Ocean Droplet
#     1  sudo apt update
#     2  apt install git
#     3  python --version
#     4  python
#     5  which python
#     6  apt install python3-pip
#     7  apt install wget
#     8  pip3 install --upgrade pip
#     9  apt install default-jdk
#    10  which python
#    11  apt install python3.8
#    12  which python
#    13  python3.8
#    14  java --version
#  https://www.oracle.com/java/technologies/downloads/#java20
#    15  wget https://download.oracle.com/java/20/latest/jdk-20_linux-x64_bin.deb
#    16  ls
#    17  sudo apt-get -qqy install ./jdk-20_linux-x64_bin.deb
#    18  ls /usr/lib/jvm
#    19  sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk-20/bin/java 2020
#    20  java --version
#    21  history
#
# java --version
# java 20.0.1 2023-04-18
# Java(TM) SE Runtime Environment (build 20.0.1+9-29)
# Java HotSpot(TM) 64-Bit Server VM (build 20.0.1+9-29, mixed mode, sharing)

#    28  pip install testresources
#    29  pip install ansible-rulebook
#    30  ansible-rulebook --version
#    31  ansible collection install ansible.eda
#    32  ansible-galaxy collection install ansible.eda

# https://raw.githubusercontent.com/ansible/event-driven-ansible/main/requirements.txt
# pip install -r requirements.txt

# pip install importlib-resources

### Success!

# root@ubuntu-s-2vcpu-2gb-nyc1-01:~# ansible-rulebook --version
# __version__ = '0.13.0'
#   Executable location = /usr/local/bin/ansible-rulebook
#   Drools_jpy version = 0.3.1
#   Java home = /usr/lib/jvm/jdk-20
#   Java version = 20.0.1
#   Python version = 3.8.10 (default, Mar 13 2023, 10:26:41) [GCC 9.4.0]



## Installed Docker on the Droplet

Using these instructions, installed Docker to run Kafka in a container

<https://docs.docker.com/engine/install/ubuntu/>

Following the installation, shut the Droplet and created a snapshot


## Create Kafka Broker

https://developer.confluent.io/quickstart/kafka-docker/


### Create the docker-compose.yml

### Start the containers

docker compose up -d

### Create a topic

docker exec broker \
kafka-topics --bootstrap-server broker:9092 \
             --create \
             --topic cfic_0


# Verify connectivity

 nc -zv 68.183.30.227 9092
Connection to 68.183.30.227 9092 port [tcp/*] succeeded!

### Look at logs


docker compose logs broker | grep 24.163.48.106

Install the offset Explorer (UI tool)

https://kafkatool.com/download.html
