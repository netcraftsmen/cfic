#
#     Copyright (c) 2022 NetCraftsmen
#     All rights reserved.
#
#     author: @joelwking
#     written:  26 April 2023
#     references:
#       activate virtualenv: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
#
# FROM python:3.11.3-slim-buster
FROM ubuntu:20.04
# ENV VIRTUAL_ENV=/opt/cfic
LABEL maintainer="Joel W. King" email="programmable.networks@gmail.com"
RUN apt update && \
    apt -y install git && \
    apt -y install python3-pip && \
    apt -y install wget && \
    apt -y install default-jdk && \
    pip3 install --upgrade pip 
# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"
#
# We need the requirements.txt file for installation
#
RUN mkdir /vscode
COPY . /vscode
WORKDIR /vscode
# RUN pip install -r requirements.txt && \
#    ansible-galaxy collection install -r collections/requirements.yml --ignore-errors && \
#    ansible-galaxy role install -r roles/requirements.yml --ignore-errors
#
#   The virtual environment is /opt/janssen
#
#   The work directory is /vscode
#
#   And, finally, the underlying directory is /workspaces/janssen
#   JAVA Installation notes
#
# https://www.oracle.com/java/technologies/downloads/
# https://askubuntu.com/questions/1430509/how-to-install-jdk-19-on-ubuntu-22-04-lts
#
# wget https://download.oracle.com/java/20/latest/jdk-20_linux-x64_bin.deb