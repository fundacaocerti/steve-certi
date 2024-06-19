#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import pytest

from app_dummy import AppDummy
from enums import HttpResponseStatusCodeType
from charge_point_dummy import ChargePointDummy
from db_helper import DatabaseHelper

class TestMeterValues:
    @property
    def operation(self) -> str:
        return "GET"

    @property
    def base_path(self) -> str:
        return "steve/api/v0/core"

    @property
    def path(self) -> str:
        return "meterValues"

    @property
    def websocket_endpoint(self) -> str:
        return "ws://localhost:8180/steve/websocket/CentralSystemService"

    @pytest.fixture
    def add_a_charging_point_to_the_database(self):
        database = DatabaseHelper()

        database.connect()

        charge_box_id = "CP001"

        database.create_charge_point(charge_box_id)

        id_tag = "TAG001"

        database.create_tag(id_tag)

        database.disconnect()

        yield

        database.connect()

        database.delete_all_tags()

        database.delete_all_charge_points()

        database.disconnect()

    def test_successful(self, add_a_charging_point_to_the_database):
        charge_box_id = "CP001"

        id_tag = "TAG001"

        uri = f"{self.websocket_endpoint}/{charge_box_id}"

        charge_point = ChargePointDummy(uri)

        charge_point.init()

        connector_id = 1

        transaction_id_1 = charge_point.start_transaction_req(connector_id, id_tag)

        charge_point.meter_values_req(
            1, # Connector ID
            "2024-06-19T16:50:02Z", # Timestamp (ISO8601)
            "380", # Voltage Sample (V)
            "80", # Current Sample (A)
            "30400", # Power Sample (W)
            "25", # SoC Sample (%)
            transaction_id_1
        )

        charge_point.meter_values_req(
            1, # Connector ID
            "2024-06-19T16:55:02Z", # Timestamp (ISO8601)
            "382", # Voltage Sample (V)
            "100", # Current Sample (A)
            "38200", # Power Sample (W)
            "35", # SoC Sample (%)
            transaction_id_1
        )

        charge_point.meter_values_req(
            1, # Connector ID
            "2024-06-19T17:00:02Z", # Timestamp (ISO8601)
            "400", # Voltage Sample (V)
            "100", # Current Sample (A)
            "40000", # Power Sample (W)
            "55", # SoC Sample (%)
            transaction_id_1
        )

        connector_id = 2

        transaction_id_2 = charge_point.start_transaction_req(connector_id, id_tag)

        charge_point.meter_values_req(
            2, # Connector ID
            "2024-06-20T13:00:02Z", # Timestamp (ISO8601)
            "1000", # Voltage Sample (V)
            "100", # Current Sample (A)
            "100000", # Power Sample (W)
            "30", # SoC Sample (%)
            transaction_id_1
        )

        charge_point.meter_values_req(
            2, # Connector ID
            "2024-06-20T13:05:02Z", # Timestamp (ISO8601)
            "982", # Voltage Sample (V)
            "92", # Current Sample (A)
            "90344", # Power Sample (W)
            "57", # SoC Sample (%)
            transaction_id_1
        )

        charge_point.meter_values_req(
            2, # Connector ID
            "2024-06-20T13:10:02Z", # Timestamp (ISO8601)
            "980", # Voltage Sample (V)
            "150", # Current Sample (A)
            "147000", # Power Sample (W)
            "72", # SoC Sample (%)
            transaction_id_1
        )

        api_host = f"/{self.base_path}/{self.path}/{charge_box_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        app.headers = {"api-key":"certi"}

        response = app.request()

        assert response.status_code == HttpResponseStatusCodeType.OK

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "1": [
                {
                    "transactionId" : transaction_id_1,
                    "meterValue" : [
                        {
                            "timestamp": "2024-06-19T17:00:02Z",
                            "sampledValue" : [
                                {
                                    "value" : "400",
                                    "context" : "Transaction.Begin",
                                    "format" : "Raw",
                                    "measurand": "Voltage",
                                    "phase" : "L1",
                                    "location" : "Cable",
                                    "unit" : "V"
                                },
                                {
                                    "value" : "100",
                                    "context" : "Transaction.Begin",
                                    "format" : "SignedData",
                                    "measurand" : "Current.Import",
                                    "phase" : "L1",
                                    "location" : "Cable",
                                    "unit" : "A"
                                },
                                {
                                    "value" : "40000",
                                    "context" : "Transaction.Begin",
                                    "format" : "Raw",
                                    "measurand" : "Power.Active.Import",
                                    "phase" : "L1",
                                    "location" : "Cable",
                                    "unit" : "W"
                                },
                                {
                                    "value" : "55",
                                    "context" : "Transaction.Begin",
                                    "format" : "Raw",
                                    "measurand" : "SoC",
                                    "phase" : "L1",
                                    "location" : "EV",
                                    "unit" : "Percent"
                                }
                            ]
                        }
                    ]
                }
            ],
            "2": [
                {
                    "transactionId" : transaction_id_2,
                    "meterValue" : [
                        {
                            "timestamp": "2024-06-20T13:10:02Z",
                            "sampledValue" : [
                                {
                                    "value" : "980",
                                    "context" : "Transaction.Begin",
                                    "format" : "Raw",
                                    "measurand" : "Voltage",
                                    "phase" : "L1",
                                    "location" : "Cable",
                                    "unit" : "V"
                                },
                                {
                                    "value" : "150",
                                    "context" : "Transaction.Begin",
                                    "format" : "SignedData",
                                    "measurand" : "Current.Import",
                                    "phase" : "L1",
                                    "location" : "Cable",
                                    "unit" : "A"
                                },
                                {
                                    "value" : "147000",
                                    "context" : "Transaction.Begin",
                                    "format" : "Raw",
                                    "measurand" : "Power.Active.Import",
                                    "phase" : "L1",
                                    "location" : "Cable",
                                    "unit" : "W"
                                },
                                {
                                    "value" : "72",
                                    "context" : "Transaction.Begin",
                                    "format" : "Raw",
                                    "measurand" : "SoC",
                                    "phase" : "L1",
                                    "location" : "EV",
                                    "unit" : "Percent"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        outcome = response.json()

        assert outcome == expected

        charge_point.stop_transaction_req(transaction_id_1, id_tag)

        charge_point.stop_transaction_req(transaction_id_2, id_tag)

        charge_point.deinit()

    def test_unauthorized(self, add_a_charging_point_to_the_database):
        charge_box_id = "CP001"

        uri = f"{self.websocket_endpoint}/{charge_box_id}"

        charge_point = ChargePointDummy(uri)

        charge_point.init()

        api_host = f"/{self.base_path}/{self.path}/{charge_box_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        response = app.request()

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "error": "Unauthorized",
            "message": "Full authentication is required to access this resource",
            "path": f"http://localhost:8180/{self.base_path}/{self.path}/{charge_box_id}",
            "status": HttpResponseStatusCodeType.UNAUTHORIZED
        }

        outcome = response.json()

        assert outcome.pop("timestamp") is not None

        assert outcome == expected

        charge_point.deinit()

    def test_not_found(self, add_a_charging_point_to_the_database):
        charge_box_id = "CP002"

        api_host = f"/{self.base_path}/{self.path}/{charge_box_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        app.headers = {"api-key":"certi"}

        response = app.request()

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "error": "Not Found",
            "message": "Could not find this chargeBoxId",
            "path": f"http://localhost:8180/{self.base_path}/{self.path}/{charge_box_id}",
            "status": HttpResponseStatusCodeType.NOT_FOUND
        }

        outcome = response.json()

        assert outcome.pop("timestamp") is not None

        assert outcome == expected
