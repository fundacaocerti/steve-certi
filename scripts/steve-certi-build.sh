#!/usr/bin/env bash
#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# *******************************************************************************/

VERSION=0.0.1

NC='\033[0m'
RED='\033[1;31m'
YELLOW='\033[1;33m'

ROOT_DIR="$(dirname $(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P ))"

function usage {
    echo -e "--"
    echo -e "${YELLOW}Usage: ${NC}build [option]"
    echo -e "${YELLOW}Options:${NC}"
    echo -e " -c\t--clean\t\tDelete target directory"
    echo -e " -h\t--help\t\tDisplay this information"
    echo -e " -v\t--version\tDisplay the version information"
    echo -e " -V\t--verbose\tActivate compilation with verbose output"
}

function clean {
    echo -e "--"
    echo -e "${YELLOW}Deleting target folder${NC}"
    cd $ROOT_DIR && rm -rf target/*
}

function version {
    echo -e "--"
    echo -e "${YELLOW}${0##*/} ${VERSION}${NC}"
    echo -e "Equatorial Project - SteVe (Rest API extension)"
    echo -e "Copyright © 2024 - Fundação CERTI"
    echo -e "All rights reserved."
}

function verbose {
    cd $ROOT_DIR && ./mvnw clean package -X -Pdocker \
        -Djdk.tls.client.protocols="TLSv1,TLSv1.1,TLSv1.2" \
        -Dmaven.plugin.validation=verbose
}

function default {
    cd $ROOT_DIR && ./mvnw clean package -Pdocker \
        -Djdk.tls.client.protocols="TLSv1,TLSv1.1,TLSv1.2" \
        -Dmaven.plugin.validation=brief
}

function error_msg {
    echo -e ""
    echo -e "${RED}ERROR: Invalid argument${NC}"
    echo -e "for more information try -h\n"
}

while [ $# -gt 0 ]; do
  case "$1" in
    -h | --help)
      usage
      exit 0
      ;;
    -c | --clean)
      clean
      exit 0
      ;;
    -v | --version)
      version
      exit 0
      ;;
    -V | --verbose)
      verbose
      exit 0
      ;;
    *)
      error_msg
      exit 1
      ;;
  esac
  shift
done

default
