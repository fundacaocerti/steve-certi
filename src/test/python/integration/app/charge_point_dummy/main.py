#!/usr/bin/env python3
#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import logging

import logging.config

from charge_point_dummy import ChargePointDummy

from v16.enums import ClearChargingProfileStatus

from pathlib import Path

import asyncio

def main() -> None:
    current_directory = Path.cwd()

    filename = 'logging_config.ini'

    full_path_name = '{}/{}'.format(current_directory.parent.parent, filename)

    logging.config.fileConfig(full_path_name)

    url = "ws://localhost:8180/steve/websocket/CentralSystemService/CP001"

    cp_dummy = ChargePointDummy(url)

    cp_dummy.init()

    ##
    # FIXME Replace this comment with the OCPP message to be tested
    status = ClearChargingProfileStatus.UNKNOWN.value
    asyncio.run(cp_dummy.clear_charging_profile_conf(status))

    cp_dummy.deinit()

if __name__ == "__main__":
    main()
