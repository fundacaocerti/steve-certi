#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import json

from dataclasses import dataclass, asdict

from charge_point_dummy.types.enums import (
    AvailabilityStatus,
    ChargePointErrorCode,
    ChargePointStatus
)

from charge_point_dummy.util.string_handling import snake_to_camel

###
# call-type messages

class ToJson():
    def to_json(self) -> str:
        return snake_to_camel(json.dumps(asdict(self)))

@dataclass
class BootNotificationPayload(ToJson):
    charge_point_vendor: str
    charge_point_model: str

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
