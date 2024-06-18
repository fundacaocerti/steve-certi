#/******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import logging
import time
import uuid
import threading
import websocket
import datetime
import json

from v16.payload import (
    BootNotificationPayload,
    StatusNotificationPayload,
    HeartbeatPayload,
    ClearChargingProfilePayload,
    SetChargingProfilePayload,
    MeterValuesPayload,
    SampledValue,
    MeterValue,
    StartTransactionPayload,
    StopTransactionPayload
)

from v16.enums import (
    Action,
    ChargePointStatus,
    ChargePointErrorCode,
    ClearChargingProfileStatus,
    ReadingContext,
    ValueFormat,
    Measurand,
    Phase,
    Location,
    Unit,
    Reason
)

from protocol.websocket import WebSocketHelper

logger = logging.getLogger('ChargePointDummy')

class ChargePointDummy:
    def __init__(self, url):
        self.__ws = WebSocketHelper(False)
        self.__url = url
        self.__interval = None
        self.__set_charging_profile_thread = None
        self.__clear_charging_profile_thread = None

    def init(self, status_notification_delay = 0) -> None:
        '''
        This method is responsible for establishing the connection with the endpoint
        and transmitting messages that will prompt the central system to recognize
        resources from our fictional station.

        Optional kwarg:
        status_notification_delay - Integer: seconds to wait after producing first status notification
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
        time.sleep(status_notification_delay)

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

    def timestamp(self) -> None:
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    ##
    # Direction: Client-to-Server

    def boot_notification_req(self) -> None:
        '''
        This method is responsible for sending the BootNotification call message and
        awaiting the response in order to capture the heartbeat interval
        '''
        payload = BootNotificationPayload('CERTI', 'Type2')
        payload.charge_box_serial_number = 'SN/CB001'
        payload.charge_point_serial_number = 'SN/CP001'
        payload.firmware_version = '1.0.23v'
        payload.iccid = '891460 0000 0000 0012'
        payload.imsi = '234 15 0829435109'
        payload.meter_serial_number = 'SN/MT001'
        payload.meter_type = 'Analog meters'

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

    def start_transaction_req(self, connector_id, id_tag) -> int:
        '''
        This method is responsible for inform about a transaction that has been started.

        @param connector_id This contains a number (>0) designating a connector of the
        Charge Point.
        @param id_tag This contains the identifier for which a transaction has to be started.
        @return This contains the transaction id supplied by the Central System.
        '''
        payload = StartTransactionPayload(
            connector_id=connector_id,
            id_tag=id_tag,
            meter_start=0,
            timestamp=self.timestamp()
        )

        call = self.create_call_message(Action.START_TRANSACTION.value, payload.to_json())

        self.__ws.send(call)

        call_result = self.__ws.receive()

        objects = json.loads(call_result)

        payload = objects[2];

        return payload['transactionId']

    def stop_transaction_req(self, transaction_id, id_tag = None) -> None:
        '''
        This method is responsible for notifying to the Central System that the transaction has stopped.

        @param transaction_id This contains the transaction-id as received by the StartTransaction.conf.
        @param id_tag This contains the identifier which requested to stop the charging. It is optional
        because a Charge Point may terminate charging without the presence of an idTag, e.g. in case of
        a reset. A Charge Point SHALL send the idTag if known.
        '''
        payload = StopTransactionPayload(
            meter_stop=1000,
            timestamp=self.timestamp(),
            transaction_id=transaction_id,
            reason=Reason.ev_disconnected.value,
            id_tag=id_tag
        )

        call = self.create_call_message(Action.STOP_TRANSACTION.value, payload.to_json())

        self.__ws.send(call)

        self.__ws.receive()

    def meter_values_req(self, connector_id, voltage, current, power, soc, transaction_id = None) -> None:
        '''
        This method is responsible for sampling the electric meter or other sensor/transducer
        hardware to provide information about your meter values.

        @param connector_id This contains a number (>0) designating a connector of the
        Charge Point.‘0’ (zero) is used to designate the main powermeter.
        @param voltage Represents simulated voltage under a connector of the charging station.
        @param current Represents simulated current under a connector of the charging station.
        @param power Represents simulated power under a connector of the charging station.
        @param soc Represents a percentage of the state of charge of the battery
        of the vehicle being recharged.
        @param transaction_id The transaction to which these meter samples are related.
        '''
        voltage_samples = [
            SampledValue(
                value=voltage,
                context=ReadingContext.transaction_begin.value,
                format=ValueFormat.raw.value,
                measurand=Measurand.voltage.value,
                phase=Phase.l1.value,
                location=Location.cable.value,
                unit=Unit.v.value
            )
        ]

        current_samples = [
            SampledValue(
                value=current,
                context=ReadingContext.transaction_begin.value,
                format=ValueFormat.signed_data.value,
                measurand=Measurand.current_import.value,
                phase=Phase.l1.value,
                location=Location.cable.value,
                unit=Unit.a.value
            )
        ]

        power_samples = [
            SampledValue(
                value=power,
                context=ReadingContext.transaction_begin.value,
                format=ValueFormat.raw.value,
                measurand=Measurand.power_active_import.value,
                phase=Phase.l1.value,
                location=Location.cable.value,
                unit=Unit.w.value
            )
        ]

        soc_samples = [
            SampledValue(
                value=soc,
                context=ReadingContext.transaction_begin.value,
                format=ValueFormat.raw.value,
                measurand=Measurand.soc.value,
                phase=Phase.l1.value,
                location=Location.ev.value,
                unit=Unit.percent.value
            )
        ]

        meter_values = [
            MeterValue(self.timestamp(), voltage_samples),
            MeterValue(self.timestamp(), current_samples),
            MeterValue(self.timestamp(), power_samples),
            MeterValue(self.timestamp(), soc_samples)
        ]

        payload = MeterValuesPayload(connector_id, transaction_id, meter_values)

        call = self.create_call_message(Action.METER_VALUES.value, payload.to_json())

        self.__ws.send(call)

        self.__ws.receive()

    ##
    # Direction: Server-to-Client

    def set_charging_profile_conf(self, status) -> None:
        self.__set_charging_profile_thread = \
            threading.Thread(target=self.set_charging_profile_conf_internal, args=(status,))

        self.__set_charging_profile_thread.start()

    def await_set_charging_profile_thread(self, timeout = 5) -> None:
        self.__set_charging_profile_thread.join(timeout)

    def set_charging_profile_conf_internal(self, status) -> None:
        self.__ws.settimeout(3)

        try:
            call = self.__ws.receive()

            uuid = self.get_uuid_from_call_message(call)

            payload = SetChargingProfilePayload(status)

            call_result = self.create_call_result_message(uuid, payload.to_json())

            self.__ws.send(call_result)

        except websocket._exceptions.WebSocketTimeoutException as e:
            logger.error(e)

    def clear_charging_profile_conf(self, status):
        self.__clear_charging_profile_thread = \
            threading.Thread(target=self.clear_charging_profile_conf_internal, args=(status,))

        self.__clear_charging_profile_thread.start()

    def await_clear_charging_profile_thread(self, timeout = 5) -> None:
        self.__clear_charging_profile_thread.join(timeout)

    def clear_charging_profile_conf_internal(self, status) -> None:
        self.__ws.settimeout(5)

        try:
            call = self.__ws.receive()

            uuid = self.get_uuid_from_call_message(call)

            payload = ClearChargingProfilePayload(status)

            call_result = self.create_call_result_message(uuid, payload.to_json())

            self.__ws.send(call_result)

        except websocket._exceptions.WebSocketTimeoutException as e:
            logger.error(e)
