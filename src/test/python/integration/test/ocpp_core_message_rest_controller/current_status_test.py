#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import pytest
import time 
from app_dummy.app_dummy import AppDummy
from app_dummy.enums import HttpResponseStatusCodeType
from charge_point_dummy.charge_point_dummy import ChargePointDummy
from db_helper.db_helper import DatabaseHelper
from charge_point_dummy.v16.enums import (
    Action,
    AvailabilityStatus,
    ChargePointStatus,
    ChargePointErrorCode
)
class TestCurrentStatus:
    @property
    def operation(self) -> str:
        return "GET"

    @property
    def base_path(self) -> str:
        return "steve/api/v0/core"

    @property
    def path(self) -> str:
        return "currentStatus"

    @property
    def websocket_endpoint(self) -> str:
        return "ws://localhost:8180/steve/websocket/CentralSystemService"

    @pytest.fixture
    def add_a_charging_point_to_the_database(self):
        database = DatabaseHelper()

        database.connect()

        charge_box_id = "CP001"

        database.create_charge_point(charge_box_id)

        database.disconnect()

        yield

        database.connect()

        database.delete_all_charge_points()

        database.disconnect()

    def test_successful_available(self, add_a_charging_point_to_the_database):
        charge_box_id = "CP001"

        uri = f"{self.websocket_endpoint}/{charge_box_id}"

        charge_point = ChargePointDummy(uri)

        charge_point.init()

        api_host = f"/{self.base_path}/{self.path}/{charge_box_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        app.headers = {"api-key":"certi"}

        response = app.request()

        assert response.status_code == HttpResponseStatusCodeType.OK

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "connectorId": charge_box_id,
            "errorCode": ChargePointErrorCode.NO_ERROR.value,
            "info": None,
            "status": ChargePointStatus.AVAILABLE.value,
            "timestamp": "2024-05-15T19:11:30.518Z",
            "vendorId": None,
            "vendorErrorCode": None
        }
        expected.pop("timestamp")
        outcome = response.json()

        assert outcome.pop("timestamp") is not None


        assert outcome == expected

        charge_point.deinit()


    def test_successful_not_available(self, add_a_charging_point_to_the_database):
        charge_box_id = "CP001"

        uri = f"{self.websocket_endpoint}/{charge_box_id}"

        charge_point = ChargePointDummy(uri)

        charge_point.init()

        charge_point.update_status(ChargePointStatus.UNAVAILABLE.value,
                ChargePointErrorCode.INTERNAL_ERROR.value)

        api_host = f"/{self.base_path}/{self.path}/{charge_box_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        app.headers = {"api-key":"certi"}

        response = app.request()

        assert response.status_code == HttpResponseStatusCodeType.OK

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "connectorId": charge_box_id,
            "errorCode": ChargePointErrorCode.INTERNAL_ERROR.value,
            "info": None,
            "status": ChargePointStatus.UNAVAILABLE.value,
            "timestamp": "2024-05-15T19:11:30.518Z",
            "vendorId": None,
            "vendorErrorCode": None
        }

        time.sleep(30)
        outcome = response.json()

        assert outcome == expected

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
