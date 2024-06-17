#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import json

from dataclasses import (
    dataclass,
    asdict,
    field
)

from v16.enums import (
    AvailabilityStatus,
    ChargePointErrorCode,
    ChargePointStatus,
    ChargingProfileStatus,
    ClearChargingProfileStatus,
    ReadingContext,
    ValueFormat,
    Measurand,
    Phase,
    Location,
    Unit
)

from util.string_handling import snake_to_camel

from typing import Optional, List

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

@dataclass
class SampledValue(ToJson):
    value: str
    context: Optional[ReadingContext] = None
    format: Optional[ValueFormat] = None
    measurand: Optional[Measurand] = None
    phase: Optional[Phase] = None
    location: Optional[Location] = None
    unit: Optional[Unit] = None

@dataclass
class MeterValue(ToJson):
    timestamp: str
    sampled_value: List[SampledValue]

@dataclass
class MeterValuesPayload(ToJson):
    connector_id: int
    transaction_id: Optional[int] = None
    meter_value: MeterValue = field(default_factory=list)

###
# call-result-type messages

@dataclass
class ChangeAvailabilityPayload(ToJson):
    status: AvailabilityStatus

@dataclass
class SetChargingProfilePayload(ToJson):
    status: ChargingProfileStatus

@dataclass
class ClearChargingProfilePayload(ToJson):
    status: ClearChargingProfileStatus
