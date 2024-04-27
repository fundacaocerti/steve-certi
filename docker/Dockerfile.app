#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# *******************************************************************************/

FROM ubuntu:22.04

MAINTAINER certi.org.br

EXPOSE 8180

EXPOSE 8443

ENV LANG=C.UTF-8

ENV LC_ALL=C.UTF-8

ENV PATH=$PATH:/code/scripts/shortcuts

ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/

RUN export JAVA_HOME

RUN apt update && \
    apt install -y openjdk-17-jdk && \
    apt install -y ant && \
    apt clean && \
    rm -rf /var/lib/apt/lists/ && \
    rm -rf /var/cache/oracle-jdk17-installer

RUN apt update && \
    apt install --no-install-recommends -y python3.11 && \
    apt install -y python3.11-dev && \
    apt install -y python3.11-venv && \
    apt install -y python3-pip && \
    apt install -y python3-wheel && \
    apt install -y build-essential && \
	apt clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install --no-cache-dir wheel

RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /code
