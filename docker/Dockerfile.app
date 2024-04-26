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

# Add shortcuts folder to PATH
ENV PATH="$PATH:/code/scripts/shortcuts"

ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/

RUN export JAVA_HOME

RUN apt update && \
    apt install -y openjdk-17-jdk && \
    apt install -y ant && \
    apt clean && \
    rm -rf /var/lib/apt/lists/ && \
    rm -rf /var/cache/oracle-jdk17-installer

WORKDIR /code
