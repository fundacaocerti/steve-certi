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
