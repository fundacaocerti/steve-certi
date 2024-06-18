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

    @pytest.mark.xfail
    def test_successful(self, add_a_charging_point_to_the_database):
        pytest.xfail("This feature is not yet implemented")

        charge_box_id = "CP001"

        id_tag = "TAG001"

        uri = f"{self.websocket_endpoint}/{charge_box_id}"

        charge_point = ChargePointDummy(uri)

        charge_point.init()

        connector_id = 1

        transaction_id_1 = charge_point.start_transaction_req(connector_id, id_tag)

        voltage = "380" # V
        current = "80" # A
        power = "30400" # W
        soc = "25" # %

        charge_point.meter_values_req(connector_id, voltage, current, power, soc, transaction_id_1)

        connector_id = 2

        transaction_id_2 = charge_point.start_transaction_req(connector_id, id_tag)

        voltage = "900" # V
        current = "110" # A
        power = "99000" # W
        soc = "35" # %

        charge_point.meter_values_req(connector_id, voltage, current, power, soc, transaction_id_2)

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
                            "sampledValue" : [
                                {
                                    "value" : "380",
                                    "context" : "Transaction.Begin",
                                    "format" : "Raw",
                                    "measurand": "Voltage",
                                    "phase" : "L1",
                                    "location" : "Cable",
                                    "unit" : "V"
                                }
                            ]
                        },
                        {
                            "sampledValue" : [
                                {
                                    "value" : "80",
                                    "context" : "Transaction.Begin",
                                    "format" : "SignedData",
                                    "measurand" : "Current.Import",
                                    "phase" : "L1",
                                    "location" : "Cable",
                                    "unit" : "A"
                                }
                            ]
                        },
                        {
                            "sampledValue" : [
                                {
                                    "value" : "30400",
                                    "context" : "Transaction.Begin",
                                    "format" : "Raw",
                                    "measurand" : "Power.Active.Import",
                                    "phase" : "L1",
                                    "location" : "Cable",
                                    "unit" : "W"
                                }
                            ]
                        },
                        {
                            "sampledValue" : [
                                {
                                    "value" : "25",
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
                            "sampledValue" : [
                                {
                                    "value" : "900",
                                    "context" : "Transaction.Begin",
                                    "format" : "Raw",
                                    "measurand" : "Voltage",
                                    "phase" : "L1",
                                    "location" : "Cable",
                                    "unit" : "V"
                                }
                            ]
                        },
                        {
                            "sampledValue" : [
                                {
                                    "value" : "110",
                                    "context" : "Transaction.Begin",
                                    "format" : "SignedData",
                                    "measurand" : "Current.Import",
                                    "phase" : "L1",
                                    "location" : "Cable",
                                    "unit" : "A"
                                }
                            ]
                        },
                        {
                            "sampledValue" : [
                                {
                                    "value" : "99000",
                                    "context" : "Transaction.Begin",
                                    "format" : "Raw",
                                    "measurand" : "Power.Active.Import",
                                    "phase" : "L1",
                                    "location" : "Cable",
                                    "unit" : "W"
                                }
                            ]
                        },
                        {
                            "sampledValue" : [
                                {
                                    "value" : "35",
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

        for i in range(1,3):
            for j in range(0,4):
                assert outcome[str(i)][0]["meterValue"][j].pop("timestamp") \
                    is not None

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

    @pytest.mark.xfail
    def test_not_found(self, add_a_charging_point_to_the_database):
        pytest.xfail("This feature is not yet implemented")

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
