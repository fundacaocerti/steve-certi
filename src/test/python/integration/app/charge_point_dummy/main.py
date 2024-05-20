#!/usr/bin/env python3
#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import logging

import logging.config

from charge_point_dummy import ChargePointDummy

from pathlib import Path

def main() -> None:
    current_directory = Path.cwd()

    filename = 'logging_config.ini'

    full_path_name = '{}/{}'.format(current_directory.parent.parent, filename)

    logging.config.fileConfig(full_path_name)

    url = "ws://172.18.0.3:8180/steve/websocket/CentralSystemService/CP001"

    cp_dummy = ChargePointDummy(url)

    cp_dummy.init()

    ##
    # FIXME Replace this comment with the OCPP message to be tested
    # example: cp_dummy.change_availability_req()

    cp_dummy.deinit()

if __name__ == "__main__":
    main()
