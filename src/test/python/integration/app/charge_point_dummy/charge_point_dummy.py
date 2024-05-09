#/******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import uuid

from v16.payload import (
    BootNotificationPayload,
    StatusNotificationPayload,
    HeartbeatPayload,
    ChangeAvailabilityPayload
)

from v16.enums import (
    Action,
    AvailabilityStatus,
    ChargePointStatus,
    ChargePointErrorCode
)

from protocol.websocket import WebSocketHelper

class ChargePointDummy:
    def __init__(self, url):
        self.__ws = WebSocketHelper(False)
        self.__url = url
        self.__interval = None

    def init(self) -> None:
        '''
        This method is responsible for establishing the connection with the endpoint
        and transmitting messages that will prompt the central system to recognize
        resources from our fictional station.
        '''
        self.__ws.connect(self.__url)

        self.boot_notification_req()

        self.heartbeat_req()

        NUMBER_OF_CONNECTORS = 2

        for index in range(NUMBER_OF_CONNECTORS):
            connector_id = index + 1;

            self.status_notification_req(
                connector_id,
                ChargePointStatus.AVAILABLE.value,
                ChargePointErrorCode.NO_ERROR.value
            )

    def deinit(self) -> None:
        '''
        This method is responsible for disconnecting from the endpoint and also for
        deallocating resources.
        '''
        self.__ws.disconnect()

    @property
    def url(self) -> str:
        '''
        This method is responsible for returning the WebSocket/JSON connection URL

        @return endpoint
        '''
        return self.__url

    @property
    def interval(self) -> str:
        '''
        This method is responsible for returning the heartbeat interval in seconds

        @return heartbeat interval
        '''
        return self.__interval

    def generate_uuid_number(self) -> str:
        '''
        This method is responsible for generating a uuid number, which symbolizes
        a unique identifier to be used in call-type messages
        '''
        return str(uuid.uuid1())

    def get_uuid_from_call_message(self, call_message) -> str:
        '''
        This method is responsible for taking in a string representing a call message
        as input and parsing it to extract the unique identifier

        @param call_message Call-type message from the central system
        @return uuid Unique identifier received from the central system.
        '''
        words = call_message.split(',')

        SECOND_POSITION_INDEX = 1

        return words[SECOND_POSITION_INDEX].replace('"','')

    def create_call_message(self, action, payload) -> str:
        '''
        This method is responsible for creating call-type messages in accordance with
        the OCPP 1.6j specification.

        The syntax of call looks like this:

        [<MessageTypeNumber>, "<UniqueId>", "<Action>", {<Payload>}]

        @param uuid This is a unique id that will be used to match request and result.
        @param action The name of the remote procedure or action.
        @param payload Payload is a JSON object containing the arguments relevant to
        the Action.
        @return call message.
        '''
        MESSAGE_TYPE_NUMBER = str(2)

        uuid = self.generate_uuid_number()

        return '[{},"{}","{}",{}]'.format(MESSAGE_TYPE_NUMBER, uuid, action, payload)

    def create_call_result_message(self, uuid, payload) -> str:
        '''
        This method is responsible for creating call-result-type messages in accordance
        with the OCPP 1.6j specification

        The syntax of call looks like this:

        [<MessageTypeNumber>, "<UniqueId>", {<Payload>}]

        @param uuid This is a unique id that will be used to match request and result. It
        must be acquired from a call message sent by central system
        @param payload Payload is a JSON object containing the arguments relevant to
        the Action.
        @return call result message.
        '''
        MESSAGE_TYPE_NUMBER = str(3)

        return '[{},"{}",{}]'.format(MESSAGE_TYPE_NUMBER, uuid, payload)

    ##
    # Direction: Client-to-Server

    def boot_notification_req(self) -> None:
        '''
        This method is responsible for sending the BootNotification call message and
        awaiting the response in order to capture the heartbeat interval
        '''
        payload = BootNotificationPayload(charge_point_vendor = 'CERTI',
                                          charge_point_model = 'Type2')

        call = self.create_call_message(Action.BOOT_NOTIFICATION.value,
                                        payload.to_json())

        self.__ws.send(call)

        call_result = self.__ws.receive()

        self.__interval = call_result[98:105]

    def heartbeat_req(self) -> None:
        '''
        This method is responsible for sending the Heartbeat call message, which
        notifies the central system that the charging point is still connected.
        '''
        payload = HeartbeatPayload()

        call = self.create_call_message(Action.HEARTBEAT.value, payload.to_json())

        self.__ws.send(call)

        self.__ws.receive()

    def status_notification_req(self, connector_id, status, error_code) -> None:
        '''
        This method is responsible for sending notifications to the central system
        to inform about state changes or errors in a charging point.

        @param connector_id This identifies which connector of the charge point is used.
        @param status This contains the current status of the charge point.
        @param error_code This contains the error code reported by the charge point
        '''
        payload = StatusNotificationPayload(connector_id, status, error_code)

        call = self.create_call_message(Action.STATUS_NOTIFICATION.value,
                                        payload.to_json())

        self.__ws.send(call)

        self.__ws.receive()

    ##
    # Direction: Server-to-Client

    def change_availability_req(self) -> None:
        '''
        This method is responsible for waiting for the arrival of the ChangeAvailability
        call message and returning the call_result message with the status of accepted.
        '''
        call = self.__ws.receive()

        uuid = self.get_uuid_from_call_message(call)

        payload = ChangeAvailabilityPayload(AvailabilityStatus.ACCEPTED.value)

        call_result = self.create_call_result_message(uuid, payload.to_json())

        self.__ws.send(call_result)
