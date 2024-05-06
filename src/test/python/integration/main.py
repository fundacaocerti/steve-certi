#!/usr/bin/env python3
#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import logging
import logging.config

from charge_point_dummy.charge_point_dummy import ChargePointDummy

def main() -> None:
    logging.config.fileConfig('logging_config.ini')

    url = "ws://172.18.0.3:8180/steve/websocket/CentralSystemService/CP001"

    cp_dummy = ChargePointDummy(url)

    cp_dummy.init()

    cp_dummy.change_availability_req()

    cp_dummy.deinit()

if __name__ == "__main__":
    main()
