#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import json

from dataclasses import (
    dataclass,
    asdict
)

from v16.enums import (
    AvailabilityStatus,
    ChargePointErrorCode,
    ChargePointStatus
)

from util.string_handling import snake_to_camel

from typing import Optional

###
# call-type messages

class ToJson():
    def to_json(self) -> str:
        return snake_to_camel(json.dumps(asdict(self)))

@dataclass
class BootNotificationPayload(ToJson):
    charge_point_vendor: str
    charge_point_model: str
    charge_box_serial_number: Optional[str] = None
    charge_point_serial_number: Optional[str] = None
    firmware_version: Optional[str] = None
    iccid: Optional[str] = None
    imsi: Optional[str] = None
    meter_serial_number: Optional[str] = None
    meter_type: Optional[str] = None

@dataclass
class StatusNotificationPayload(ToJson):
    connector_id: int
    status: ChargePointStatus
    error_code: ChargePointErrorCode

@dataclass
class HeartbeatPayload(ToJson):
    pass

###
# call-result-type messages

@dataclass
class ChangeAvailabilityPayload(ToJson):
    status: AvailabilityStatus
