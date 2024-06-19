#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

from enum import Enum

class Action(Enum):
    '''
    An Action is a required part of a Call message.
    '''
    BOOT_NOTIFICATION = 'BootNotification'
    HEARTBEAT = 'Heartbeat'
    STATUS_NOTIFICATION = 'StatusNotification'
    METER_VALUES = 'MeterValues'
    START_TRANSACTION = 'StartTransaction'
    STOP_TRANSACTION = 'StopTransaction'

class AvailabilityStatus(Enum):
    '''
    Status returned in response to ChangeAvailability.req.
    '''
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    SCHEDULED = 'Scheduled'

class ChargePointStatus(Enum):
    '''
    Status reported in StatusNotification.req. A status can be reported for the
    Charge Point main controller (connectorId = 0) or for a specific connector.
    Status for the Charge Point main controller is a subset of the enumeration:
    Available, Unavailable or Faulted.

    States considered Operative are: Available, Preparing, Charging, SuspendedEVSE,
    SuspendedEV, Finishing, Reserved.

    States considered Inoperative are: Unavailable, Faulted.
    '''
    AVAILABLE = 'Available'
    PREPARING = 'Preparing'
    CHARGING = 'Charging'
    SUSPENDED_EVSE = 'SuspendedEVSE'
    SUSPENDED_EV = 'SuspendedEV'
    FINISHING = 'Finishing'
    RESERVED = 'Reserved'
    UNAVAILABLE = 'Unavailable'
    FAULTED = 'Faulted'

class ChargePointErrorCode(Enum):
    '''
    Charge Point status reported in StatusNotification.req.
    '''
    CONNECTOR_LOCK_FAILURE = 'ConnectorLockFailure'
    EV_COMMUNICATION_ERROR = 'EVCommunicationError'
    GROUND_FAILURE = 'GroundFailure'
    HIGH_TEMPERATURE = 'HighTemperature'
    INTERNAL_ERROR = 'InternalError'
    LOCAL_LIST_CONFLICT = 'LocalListConflict'
    NO_ERROR = 'NoError'

class ChargingProfileStatus(Enum):
    '''
    Status returned in response to SetChargingProfile.req
    '''
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    NOT_SUPPORTED = 'NotSupported'

class ClearChargingProfileStatus(Enum):
    '''
    Status returned in response to ClearChargingProfile.req
    '''
    ACCEPTED = 'Accepted'
    UNKNOWN = 'Unknown'

class ReadingContext(Enum):
    '''
    Values of the context field of a value in SampledValue.
    '''
    interruption_begin = 'Interruption.Begin'
    interruption_end = 'Interruption.End'
    other = 'Other'
    sample_clock = 'Sample.Clock'
    sample_periodic = 'Sample.Periodic'
    transaction_begin = 'Transaction.Begin'
    transaction_end = 'Transaction.End'
    trigger = 'Trigger'

class ValueFormat(Enum):
    '''
    Format that specifies how the value element in SampledValue is to be
    interpreted.
    '''
    raw = 'Raw'
    signed_data = 'SignedData'

class Measurand(Enum):
    '''
    Allowable values of the optional "measurand" field of a Value element, as
    used in MeterValues.req and StopTransaction.req messages. Default value of
    "measurand" is always "Energy.Active.Import.Register"
    '''
    current_export = 'Current.Export'
    current_import = 'Current.Import'
    current_offered = 'Current.Offered'
    energy_active_export_register = 'Energy.Active.Export.Register'
    energy_active_import_register = 'Energy.Active.Import.Register'
    energy_reactive_export_register = 'Energy.Reactive.Export.Register'
    energy_reactive_import_register = 'Energy.Reactive.Import.Register'
    energy_active_export_interval = 'Energy.Active.Export.Interval'
    energy_active_import_interval = 'Energy.Active.Import.Interval'
    energy_reactive_export_interval = 'Energy.Reactive.Export.Interval'
    energy_reactive_import_interval = 'Energy.Reactive.Import.Interval'
    frequency = 'Frequency'
    power_active_export = 'Power.Active.Export'
    power_active_import = 'Power.Active.Import'
    power_factor = 'Power.Factor'
    power_offered = 'Power.Offered'
    power_reactive_export = 'Power.Reactive.Export'
    power_reactive_import = 'Power.Reactive.Import'
    rpm = 'RPM'
    soc = 'SoC'
    temperature = 'Temperature'
    voltage = 'Voltage'

class Phase(Enum):
    '''
    Phase as used in SampleValue. Phase specifies how a measured value is to
    be interpreted. Please note that not all values of Phase are applicable to
    all Measurands
    '''
    l1 = 'L1'
    l2 = 'L2'
    l3 = 'L3'
    n = 'N'
    l1_n = 'L1-N'
    l2_n = 'L2-N'
    l3_n = 'L3-N'
    l1_l2 = 'L1-L2'
    l2_l3 = 'L2-L3'
    l3_l1 = 'L3-L1'

class Location(Enum):
    '''
    Allowable values of the optional "location" field of a value element in
    SampledValue.
    '''
    inlet = 'Inlet'
    outlet = 'Outlet'
    body = 'Body'
    cable = 'Cable'
    ev = 'EV'

class Unit(Enum):
    '''
    Allowable values of the optional "unit" field of a Value element, as used
    in MeterValues.req and StopTransaction.req messages. Default value of "unit"
    is always "Wh"
    '''
    wh = 'Wh'
    kwh = 'kWh'
    varh = 'varh'
    kvarh = 'kvarh'
    w = 'W'
    kw = 'kW'
    va = 'VA'
    kva = 'kVA'
    var = 'var'
    kvar = 'kvar'
    a = 'A'
    v = 'V'
    celsius = 'Celsius'
    fahrenheit = 'Fahrenheit'
    k = 'K'
    percent = 'Percent'

class Reason(Enum):
    '''
    Reason for stopping a transaction in StopTransaction.req.
    '''
    emergency_stop = 'EmergencyStop'
    ev_disconnected = 'EVDisconnected'
    hard_reset = 'HardReset'
    local = 'Local'
    other = 'Other'
    power_loss = 'PowerLoss'
    reboot = 'Reboot'
    remote = 'Remote'
    soft_reset = 'SoftReset'
    unlock_command = 'UnlockCommand'
    de_authorized = 'DeAuthorized'
