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
    echo -e "${YELLOW}Usage: ${NC}run [option]"
    echo -e "${YELLOW}Options:${NC}"
    echo -e " -h\t--help\t\tDisplay this information"
    echo -e " -v\t--version\tDisplay the version information"
}

function version {
    echo -e "--"
    echo -e "${YELLOW}${0##*/} ${VERSION}${NC}"
    echo -e "Equatorial Project - SteVe (Rest API extension)"
    echo -e "Copyright © 2024 - Fundação CERTI"
    echo -e "All rights reserved."
}

function default {
    cd $ROOT_DIR && java -jar target/steve.jar
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
    -v | --version)
      version
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
