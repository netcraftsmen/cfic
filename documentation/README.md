# Cisco Federal Innovation Challenge

This repository contains installation instructions and operational instructions for an Event-Driven Ansible (EDA) deployment using Kafka running on Confluent Cloud. Included is a Kafka Publisher that queries the Meraki Cloud for network clients, and publishes the result to Kafka.

The Ansible Rulebook consumes messages from the Kafka Topic, then invokes a Playbook to create a Splunk SOAR event (container and artifacts) with the client data defined in the Common Event Format (CEF) standard format. CEF defines a syntax used as an interoperability standard for data sharing among security products.

## Demonstration Environment

The demonstration environment consists of virtual machine (a DigitalOcean Droplet) supporting publishing and consumption of Kafka messages. The code to publish events is public and available on Cisco DevNet Code Exchange as [semaphore](https://developer.cisco.com/codeexchange/github/repo/netcraftsmen/semaphore/). This repository contains the remaining solution artifacts.

The Splunk SOAR instance is deployed from [AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-4ac4q4lzrhh4a) from an Amazon Machine Image (AMI). Splunk SOAR offers a community edition of the product enabling developer access without incurring and license fees.

## Installation

These installation instructions use [DigitalOcean](https://www.digitalocean.com/) as a cloud service provider. The solution does not leverage any proprietary feature of DigitalOcean, other than simplicity, cost and ease of use.


### Create SSH key

When creating a Droplet, you must create a SSH key if one is not available in our account. Create a SSH key for the Droplet. Refer to [How to Set Up SSH Keys ...](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys-on-ubuntu-20-04) for more details.

Create a key pair on the client machine (your computer):

```shell
cd ~/.ssh
ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/joelking/.ssh/id_rsa): droplet_cfic
```

### Create a Droplet

From your DigitalOcean account, select the **Droplets** tab and create a Droplet. For texting and evaulation purposes, these machine resources are sufficient. 

```
cfic-s-2vcpu-2gb-nyc1-01 / 2 GB Memory / 60 GB Disk / NYC1 - Ubuntu 20.04 (LTS) x64
```

Follow the instructions to provide the SSH key during the setup.

### SSH to the Droplet

From your client machine, SSH to the Droplet. The IPv4 address is shown on the GUI after the Droplet is created. Use the `-i` switch to reference the SSH identity file.

```shell
ssh root@<droplet_ipv4_address> -i ~/.ssh/droplet_cfic
```

### Create a directory for the installation

Create a directory for the installation.

```shell
mkdir cfic
cd cfic
```

### Update and Install necessary packages

Update and install the necessary packages.

```shell
sudo apt update
sudo apt-get upgrade
sudo apt install git
sudo apt install python3-pip
sudo apt install python3.8-venv
sudo apt install pkgconf
sudo apt install build-essential
sudo apt install libsystemd-dev
pip3 install --upgrade pip
```

### Create a virtual environment

Create a virtual environment for the Event-Driven Ansible installation.

```shell
python3 -m venv eda
source eda/bin/activate
```

### Install Java

Event-Driven Ansible requires Java. Download the JAVA package. Refer to <https://www.oracle.com/java/technologies/downloads/>. Java version 20.0.1 is used.

```shell
wget https://download.oracle.com/java/20/latest/jdk-20_linux-x64_bin.deb
sudo apt-get -qqy install ./jdk-20_linux-x64_bin.deb
ls /usr/lib/jvm
sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk-20/bin/java 2020
```

Verify the installation and version of Java.

```shell
java --version
java 20.0.1 2023-04-18
Java(TM) SE Runtime Environment (build 20.0.1+9-29)
Java HotSpot(TM) 64-Bit Server VM (build 20.0.1+9-29, mixed mode, sharing)
```

### Install Ansible and Ansible Rulebook

While in the Python virtual environment `eda`, install Ansible and Ansible Rulebook.

```shell
pip install testresources
pip install ansible
```

Create a file [requirements.txt](https://raw.githubusercontent.com/ansible/event-driven-ansible/main/requirements.txt) with these entries:

```
azure-servicebus
aiobotocore
aiohttp
aiokafka
watchdog
dpath
importlib-resources
```

Use pip to install the above requirements.

```shell
pip install -r requirements.txt
pip install systemd-python
```
>Note: installing `systemd-python` from the `requirements.txt` file is a problem, install separately.

Install Ansible Rulebook:

```shell
pip install ansible-rulebook
```

Verify the installation and version.

```shell
ansible-rulebook --version
__version__ = '0.13.0'
  Executable location = /usr/local/bin/ansible-rulebook
  Drools_jpy version = 0.3.1
  Java home = /usr/lib/jvm/jdk-20
  Java version = 20.0.1
  Python version = 3.8.10 (default, Mar 13 2023, 10:26:41) [GCC 9.4.0]
```

Install the Event-Driven Ansible collection. By default it will install in `/root/.ansible/collections/ansible_collections`.

```shell
ansible-galaxy collection install ansible.eda
```

>Note: use `ansible-galaxy collection list` to view the installed collections and their locations.

### Install Docker

The Kafka publisher in [semaphore](https://developer.cisco.com/codeexchange/github/repo/netcraftsmen/semaphore/) can run in a container. Install Docker.

These are the recommended instructions <https://docs.docker.com/engine/install/ubuntu/>, or use these notes.

```shell
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```
Verify the installation.

```shell
sudo docker run hello-world
```

### Clone this repository

This repository is private (currently). You need permissions to read the private repository and a [personal access token](https://github.com/settings/tokens) on your GitHub account. 

Create a **personal access token** in GitHub and then clone the repository using the token. 

```shell
cd ~/cfic
git clone https://<personal_access_token_here>@github.com/netcraftsmen/cfic.git
```

### Clone the Kafka publisher, Semaphore

Create a Python virtual environment for the `semaphore` code.

```shell
cd ~/cfic
python3 -m venv publisher
source publisher/bin/activate
```

This repository is public, there is no need for a **personal access token**.

```shell
git clone https://github.com/netcraftsmen/semaphore.git
```

Install the Python packages required.

```shell
cd ~/cfic/semaphore/
pip install -r requirements.txt
```

### Create a snapshot of the Droplet

All software and packages are installed, optionally shutdown the Droplet create a snapshot. Use the **images** tab on the DigitalOcean GUI to create a snapshot with the Droplet **OFF**.

```shell
sudo shutdown now -h
```

After the snapshot is complete, turn the Droplet **ON** and log (SSH) back to the Droplet.

### Start publishing to Kafka in Confluent Cloud

If you are unfamiliar with configuring Kafka in Confluent Cloud, review this Meetup session:
[Programmability and Automation Meetup - Introduction to network telemetry using Apache Kafka]
(https://www.youtube.com/watch?v=ABMcflO1ix8)

From the Kafka implementation, the Bootstrap server FQDN, port, API Key and Secret, along with the name of the Kafka Topic is required. These values are specified in environment variables. Make a note of them.

### Publish messages to Kafka

Enter the `library` directory with the Python **publisher** virtual environment active.

```shell
cd ~/cfic/semaphore/library
```

#### Meraki Dashboard API key

The **semaphore** program requires the Meraki dashboard API key and a timer. These values are provided using environment variables.

```shell
export MERAKI_DASHBOARD_API_KEY=1c6fc04dd872a2redacted10275f5aaa17d34a
export MERAKI_TIMESPAN=43200
```

#### Confluent Cloud configuration

It also needs the Confluent Cloud variables. In the follow, replace the FQDN of the Kafka Bootstrap server, the cluster API secret and key, and the name of the Kafka topic. Then specify these using environment variables.

```bash
export BOOTSTRAP_SERVER=pkc-n00kk.us-east-1.aws.confluent.cloud:9092
IFS=':'    # Set colon as delimiter
read -a cluster <<< "$BOOTSTRAP_SERVER"
export CLUSTER_HOST=${cluster[0]}
export CLUSTER_PORT=${cluster[1]}
#
export CLUSTER_API_SECRET=KTI3pZBFYs4Xp91WuFSY3yrKDredactedkmS7fCeZPzO/6IR9B3RU
export CLUSTER_API_KEY=UV3UB3YBIMAGAYIQR4J
#
export TOPIC=cfic_0
#
export OFFSET=latest
export GROUP=semaphore_1
```

#### Verify network connectivity to the Kafka Broker

Verify the Kafka Broker is listening on TCP port 9092 (port 9092 is the default value) and the environment variables are configured by using `netcat`.

```shell
nc -zv $CLUSTER_HOST $CLUSTER_PORT
Connection to pkc-n00kk.us-east-1.aws.confluent.cloud 9092 port [tcp/*] succeeded!
```

### Publish Messages

The Bash script runs the program every `n` seconds. Configure the name of the program and a timer value, then execute the script.

```shell
export PUBLISHER_PROGRAM=./publish_clients.py
export PUBLISHER_TIMER=300
./start_publishing.sh
```

After a few seconds, you should see the confirmation that a message is produced. 

```shell
Produced record | topic: cfic_0, partition: [5], @offset: 1007 | key: L_629378047925028460, value: {"payload": [{"id": "k0c97c9", "mac": "26:f5:a2:3c
```

>Note: Use CTL + C to stop the shell script. If you leave the publisher running too long before you consume messages, you may exhaust the CPU and memory of this minimally configured Droplet.

### Testing an event source program

You can test an Ansible event_source plugin (standalone, separate from being called by a Runbook) by running from a Python interpreter. Activate the Python virtual environment.

```shell
cd ~/cfic 
source eda/bin/activate
```
Enter the directory where your Ansible event_source plugin resides.

```shell
cd ~/cfic/cfic/collections/ansible_collections/netcraftsmen/kafka/plugins/event_source
python3 consumer.py
```

>Note: This is used for debugging purposes in [developing](https://ansible-rulebook.readthedocs.io/en/stable/sources.html#how-to-develop-a-custom-plugin) event_source plugins, it may expose credentials to the terminal. Only use in a development environment.

This program displays the arguments and waits to receive Kafka messages.

```
{'password': 'KTI3pZBFYs4Xp9agredactedEi8rkEOd0kmS7fCeZPzO/6IR9B3RU', 'username': 'UV3UB3YIAMGAYIQR4J', 'topic': 'cfic_0', 'host': 'pkc-n00kk.us-east-1.aws.confluent.cloud', 'port': '9092', 'cafile': None, 'certfile': None, 'keyfile': None, 'check_hostname': False, 'offset': 'latest'}
```

Use CTL + C to exit the program.

## Splunk SOAR

In this solution messages published to Kafka are consumed by the Event-Driven Ansible Rulebook `playbooks/rb.kafka.yml`, and passed to the associate playbook `playbooks/pb.soar.yml` for processing. The playbook invokes a custom Ansible module to create security events (containers and artifacts) in SPLUNK SOAR.

### Installation

Refer to the [Installation instructions for Splunk SOAR](https://docs.splunk.com/Documentation/SOARonprem/6.0.0/Install/InstallAMI) and the *usage* instructions associated with the AMI documentation. The are summarized here.

 * Allow 5-10 minutes after launching the Splunk SOAR On-premises server for the setup process to complete.
 * In your EC2 Management Console, find your instance running Splunk SOAR On-premises. Copy its public IP and Paste the public IP into a new browser tab.
 * Log into Splunk SOAR On-premises with the following credentials: **username: soarlocaladmin** password: the AWS instance id ex: **i-04ad4f23eaje76530**.

>Note: The version tested is `6.0.0.114895`.

Instructions for installing SOAR OnPrem are at: <https://docs.splunk.com/Documentation/SOARonprem/latest/Install/Login>

Following launching of the instance, create a security group and apply to the instance. Allow SSH and HTTPS, HTTP and TCP port 9999 from your source IP address (or include your team's IP address.)

#### SSH access (optional)

The SSH username: is **phantom**. If you need root access, use `sudo su -`. You should be able to connect to the instance via SSH using the key-pair assigned at launch.

```shell
ssh -i ~/.ssh/id_ed25519 phantom@52.3.242.131
```

>NOTE: SSH access is used to develop custom applications and to gracefully shutdown the system.

#### Web UI access

Login to the web UI using `soar_local_admin` and the instance ID (e.g. `i-04647a8ebf382b26a`) change the password of the `soar_local_admin` account. 

#### Obtain the API Key

The Splunk SOAR API uses a bearer token for authentication. You must copy (or create) an Auth Token under the user configuration screen for user `automation`. The token can be downloaded and is presented as JSON.

```json
{ "ph-auth-token": "1GvdkA220zFlbJMjIredactedRXmhmm9QANjCg0k=","server": "https://54.144.142.30" }
```

From your terminal session on the Droplet, provide these values in environment variables.

```shell
export SOAR_AUTHTOKEN="1GvdkA220zFlbJMjISwCl9NredactedXmhmm9QANjCg0k="
export SOAR_SERVER=ec2-54-144-142-30.compute-1.amazonaws.com
```

## Executing an Ansible Rulebook

To facilitate publishing messages and consuming them with Event-Driven Ansible, logon the Droplet with a second terminal session. Activate the Python virtual environment and enter the `cfic/playbook` directory. 

```shell
cd ~/cfic
source eda/bin/activate
cd ~/cfic/cfic/playbooks
```

### Ansible Config file

By default, Ansible looks in the playbook directory for an [ansible.cfg](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#the-configuration-file) configuration file. However, this convention does not appear to be honored by `ansible-rulebook`.  You need to set the ENV variable for ansible-rulebook to locate the configuration file.

To circumvent the issue, create an environment variable, **ANSIBLE_CONFIG**. Do not use a relative path.

```shell
export ANSIBLE_CONFIG=/root/cfic/cfic/playbooks/ansible.cfg
```

Optionally, from the home directory, create a symbolic link `ln -s  /root/cfic/cfic/playbooks/ansible.cfg .ansible.cfg`

```shell
(eda) root@cfic-s-2vcpu-2gb-nyc1-01:~# ls -salt .ansible.cfg
0 lrwxrwxrwx 1 root root 37 May 11 17:00 .ansible.cfg -> /root/cfic/cfic/playbooks/ansible.cfg
```

### View the messages from Kafka

You will need to set the environment variables for Splunk SOAR and Kafka! Refer to the section `Publish Messages`. From your alternate terminal session, publish messages to Kafka using the `./start_publishing.sh` shell script.

Run rulebook `rb.pretty.yml` to determine what (if any) messages are returned from Kafka.

```shell
ansible-rulebook -r rb.pretty.yml -i inventory.yml -v --env-vars CLUSTER_API_KEY,CLUSTER_API_SECRET,TOPIC,OFFSET,GROUP,OFFSET,CLUSTER_HOST,CLUSTER_PORT
```

The output from this rulebook provides a view of the message schema. It is useful for referencing variables from a playbook invoked by the rulebook. Variable `meta` is created by **ansible-rulebook**, while `network`, `networkName` and `payload` are generated by the Kafka publisher, in this case **semaphore** program `publish_clients.py`

The first client in the `payload` is shown. There are a number of clients. 

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

### Execute the Rulebook and Playbook

The rulebook `playbooks/rb.kafka.yml` receives messages from Kafka and invokes an Ansible playbook to load the data into Splunk SOAR.

Execute it.

```shell
ansible-rulebook -r rb.kafka.yml -i inventory.yml -v --env-vars CLUSTER_API_KEY,CLUSTER_API_SECRET,TOPIC,OFFSET,GROUP,CLUSTER_HOST,CLUSTER_PORT
```

Provided all environment variables are properly set, data from the Meraki dashboard is posted as an event (container and artifact(s)) in Splunk SOAR.

## How variables are passed (and referenced) in a playbook

The playbook `playbooks/pb.debug.yml` illustrates how variables are passed and referenced by a playbook for singular events. In the reference schema *payload* `'{{ ansible_eda.event.payload }}'` is a list and can be used in a loop.

Rulebooks with **multi-events** have a slightly different format.

## Multi-Events

When configuring a Rulebook for [multiple_events](https://ansible-rulebook.readthedocs.io/en/stable/multi_events.html), the output format is slightly different.

>Note: the 'm_0', 'm_1', etc. reference and `events` is plural rather than `event`. 

To reference `payload` in the rulebook, you need to reference `events.m_0.payload` if it matched the first conditional, `events.m_1.payload`.

Execute the `playbooks/rb.multi_events.yml`

```shell
ansible-rulebook -r rb.multi_events.yml -i inventory.yml -v --env-vars CLUSTER_API_KEY,CLUSTER_API_SECRET,TOPIC,GROUP,OFFSET,CLUSTER_HOST,CLUSTER_PORT
```

Abbreviated sample output is shown:

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

## References

Useful references for Event Driven Ansible:

 * 6 Guidelines for creating custom source plugins for Event-Driven Ansible! <https://www.youtube.com/watch?v=4f7ARUnVZmY>
 * AIOKafka <https://aiokafka.readthedocs.io/en/stable/api.html>
 * Installing Java on Ubuntu <https://askubuntu.com/questions/1430509/how-to-install-jdk-19-on-ubuntu-22-04-lts>
 * Creating custom event plugins <https://www.ansible.com/blog/creating-custom-event-driven-ansible-source-plugins>

## Author

Joel W. King @joelwking

