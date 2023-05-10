# README.md

## References

Useful references for Event Driven Ansible

* 6 Guidelines for creating custom source plugins for Event-Driven Ansible! <https://www.youtube.com/watch?v=4f7ARUnVZmY>
* AIOKafka <https://aiokafka.readthedocs.io/en/stable/api.html>

## Installation

Installation documentation when installing on Digital Ocean 

ubuntu-s-2vcpu-2gb-nyc1-01 / 2 GB Memory / 60 GB Disk / NYC1 - Ubuntu 20.04 (LTS) x64

```
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

```

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





### Look at logs


docker compose logs broker | grep 24.163.48.106

Install the offset Explorer (UI tool)

https://kafkatool.com/download.html



## Documentation

https://www.ansible.com/blog/creating-custom-event-driven-ansible-source-plugins


## Testing an event source outside of a rulebook

You can test your event_source by running from a python interpreter.

~/cfic/cfic/collections/ansible_collections/netcraftsmen/kafka/plugins/event_source# python3 consumer.py

## Environment variables

### Meraki Dashboard

The semaphore program requires the Meraki dashboard API key and a timer configured

```shell
export MERAKI_DASHBOARD_API_KEY=1c6fc04dd872a2redacted10275f5aaa17d34a
export MERAKI_TIMESPAN=43200
```

### Kafka Cluster

Both the publisher and consumer (client) require several environment variables

```bash
export BOOTSTRAP_SERVER=pkc-n00kk.us-east-1.aws.confluent.cloud:9092
IFS=':'    # Set colon as delimiter
read -a cluster <<< "$BOOTSTRAP_SERVER"
export CLUSTER_HOST=${cluster[0]}
export CLUSTER_PORT=${cluster[1]}

export CLUSTER_API_SECRET=KTI3pZBFYs4Xp91WuFSY3yrKDredactedkmS7fCeZPzO/6IR9B3RU
export CLUSTER_API_KEY=UV3UB3YBIMAGAYIQR4J

export TOPIC=cfic_0
export OFFSET=latest
export GROUP=semaphore_1
```

#### Verify network connectivity to the Kafka Broker

Verify connectivity to the Kafka Broker defined in the environment variables by using `netcat`.

```shell
# nc -zv $CLUSTER_HOST $CLUSTER_PORT
Connection to pkc-n00kk.us-east-1.aws.confluent.cloud 9092 port [tcp/*] succeeded!
```
### Splunk SOAR

Auth Token for Phantom (Splunk SOAR)  configure this under the user configuration screen for user `automation`

{ "ph-auth-token": "1GvdkA220zFlbJMjIredactedRXmhmm9QANjCg0k=","server": "https://54.144.142.30" }

```shell
export SOAR_AUTHTOKEN="1GvdkA220zFlbJMjISwCl9NredactedXmhmm9QANjCg0k="
export SOAR_SERVER=ec2-54-144-142-30.compute-1.amazonaws.com
```

### Ansible Config file

You need to set the ENV variable for ansible-rulebook to locate the configuration file.

https://docs.ansible.com/ansible/latest/reference_appendices/config.html#the-configuration-file

export ANSIBLE_CONFIG=/root/cfic/cfic/playbooks/ansible.cfg

>Note: do not use relative paths

>NOTE Test using a symbolic link

from the home directory `ln -s  /root/cfic/cfic/playbooks/ansible.cfg .ansible.cfg`

## Running a rulebook 

example of running the rulebook

```shell
ansible-rulebook -r rb.kafka.yml -i inventory.yml -v --env-vars CLUSTER_API_KEY,CLUSTER_API_SECRET,TOPIC,OFFSET,GROUP,CLUSTER_HOST,CLUSTER_PORT
```

## Splunk SOAR

Installation instructions for Splunk SOAR 

https://docs.splunk.com/Documentation/SOARonprem/6.0.0/Install/InstallAMI

Refer to https://github.com/joelwking/csna_/blob/main/DEVELOPMENT_NOTES.md  **HOWEVER** these instructions may be OUT OF DATE!

The version installed is `version 6.0.0.114895`.

Following launching of the instance, create a security group and apply to the instance

Allow SSH and HTTPS, HTTP and TCP port 9999 from your source IP address (or include your team's IP address.)

You should be able to connect to the instance via SSH using the key-pair assigned at launch

```
ssh -i ~/.ssh/id_ed25519 phantom@52.3.242.131
```
>Note: In order to log in to the operating system of your AMI-based installation using SSH, use the user id `phantom`. If you need root access, use `sudo su -`.

<https://docs.splunk.com/Documentation/SOARonprem/latest/Install/Login>
Login to the web UI using `soar_local_admin` and the instance ID `i-04647a8ebf382b26a`

Change the password of the `soar_local_admin` account. Get the API key from the `automation` userid.



## Debugging messages received from Kafka

Run this rulebook to determine what data is being returned from Kafka

```shell
ansible-rulebook -r rb.pretty.yml -i inventory.yml -v --env-vars CLUSTER_API_KEY,CLUSTER_API_SECRET,TOPIC,OFFSET,GROUP,OFFSET,CLUSTER_HOST,CLUSTER_PORT
```

The first client in the `payload` is shown. There are a number of clients. Note the format of the message from Kafka is controlled by the publisher, in this case semaphore `publish_clients.py`

```shell
2023-05-09 21:00:27,138 - ansible_rulebook.rule_set_runner - INFO - action args: {'pretty': True}
{'meta': {'received_at': '2023-05-09T21:00:26.965010Z',
          'source': {'name': 'netcraftsmen.kafka.consumer',
                     'type': 'netcraftsmen.kafka.consumer'},
          'uuid': '0d39a059-c748-41ae-9ddc-c104ca8cc587'},
 'network': 'L_629378047925028460',
 'networkName': 'SWISSWOOD',
 'payload': [{'adaptivePolicyGroup': None,
              'description': 'JOEL-HP-Win10',
              'deviceTypePrediction': None,
              'firstSeen': '2017-05-07T20:21:44Z',
              'groupPolicy8021x': None,
              'id': 'k71b918',
              'ip': '192.168.5.26',
              'ip6': '2600:1004:b0a1:b488:dd89:ffe6:92d6:c1c6',
              'ip6Local': 'fe80:0:0:0:5e87:4285:dbd0:2f6a',
              'lastSeen': '2023-05-09T17:42:36Z',
              'mac': '7c:b0:c2:ad:38:24',
              'manufacturer': 'Intel',
              'networkName': 'SWISSWOOD',
              'notes': None,
              'organizationId': '530205',
              'os': 'Windows 10',
              'pskGroup': None,
              'recentDeviceConnection': 'Wireless',
              'recentDeviceMac': 'e0:55:3d:25:38:60',
              'recentDeviceName': 'OFFICE_WP',
              'recentDeviceSerial': 'Q2JD-J78J-KF9E',
              'smInstalled': False,
              'ssid': 'SWISSWOOD-WiFi',
              'status': 'Offline',
              'switchport': None,
              'usage': {'recv': 197888, 'sent': 277040, 'total': 474928},
              'user': None,
              'vlan': '5'},
```

## Multievents

When running multiple_events, the output format is slightly different. Note the 'm_0' reference.

To reference `payload` in the rulebook, you need to reference `events.m_0.payload` if it matched the first conditional.

```shell
2023-05-09 21:06:12,307 - ansible_rulebook.rule_set_runner - INFO - action args: {'pretty': True}
{'m_0': {'meta': {'received_at': '2023-05-09T21:06:12.188843Z',
                  'source': {'name': 'netcraftsmen.kafka.consumer',
                             'type': 'netcraftsmen.kafka.consumer'},
                  'uuid': 'c59cdce1-872c-4535-ac50-3c7adb79747b'},
         'network': 'L_629378047925028460',
         'networkName': 'SWISSWOOD',
         'payload': [{'adaptivePolicyGroup': None,
                      'description': 'JOEL-HP-Win10',
                      'deviceTypePrediction': None,
                      'firstSeen': '2017-05-07T20:21:44Z',
                      'groupPolicy8021x': None,
                      'id': 'k71b918',
                      'ip': '192.168.5.26',
                      'ip6': '2600:1004:b0a1:b488:dd89:ffe6:92d6:c1c6',
                      'ip6Local': 'fe80:0:0:0:5e87:4285:dbd0:2f6a',
                      'lastSeen': '2023-05-09T17:42:36Z',
                      'mac': '7c:b0:c2:ad:38:24',
                      'manufacturer': 'Intel',
                      'networkName': 'SWISSWOOD',
                      'notes': None,
                      'organizationId': '530205',
                      'os': 'Windows 10',
                      'pskGroup': None,
                      'recentDeviceConnection': 'Wireless',
                      'recentDeviceMac': 'e0:55:3d:25:38:60',
                      'recentDeviceName': 'OFFICE_WP',
                      'recentDeviceSerial': 'Q2JD-J78J-KF9E',
                      'smInstalled': False,
                      'ssid': 'SWISSWOOD-WiFi',
                      'status': 'Offline',
                      'switchport': None,
                      'usage': {'recv': 197888,
                                'sent': 277040,
                                'total': 474928},
                      'user': None,
                      'vlan': '5'},
```