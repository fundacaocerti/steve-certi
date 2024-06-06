#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import pytest
import asyncio

from app_dummy import AppDummy
from enums import HttpResponseStatusCodeType
from charge_point_dummy import ChargePointDummy
from db_helper import DatabaseHelper

from v16.enums import ChargingProfileStatus

class TestSetChargingProfile:
    @property
    def operation(self) -> str:
        return "POST"

    @property
    def base_path(self) -> str:
        return "steve/api/v0/smartCharging"

    @property
    def path(self) -> str:
        return "setChargingProfile"

    @property
    def websocket_endpoint(self) -> str:
        return "ws://localhost:8180/steve/websocket/CentralSystemService"

    @pytest.fixture
    def database_setup(self) -> None:
        database = DatabaseHelper()

        database.connect()

        charge_box_id = "CP001"

        database.create_charge_point(charge_box_id)

        database.create_daily_default_profile()

        database.disconnect()

        yield

        database.connect()

        database.delete_all_profiles()

        database.delete_all_charge_points()

        database.disconnect()

    @pytest.mark.xfail
    def test_successful_accepted(self, database_setup):
        pytest.xfail("This feature is not yet implemented")

        charge_box_id = "CP001"

        uri = f"{self.websocket_endpoint}/{charge_box_id}"

        charge_point = ChargePointDummy(uri)

        charge_point.init()

        asyncio.run(
            charge_point.set_charging_profile_conf(ChargingProfileStatus.ACCEPTED.value)
        )

        api_host = f"/{self.base_path}/{self.path}/{charge_box_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type": "application/json"}

        app.headers = {"api-key": "certi"}

        body = {
            "chargingProfileId" : 1,
            "connectorId" : 0
        }

        app.payload = body

        response = app.request()

        assert response.status_code == HttpResponseStatusCodeType.OK

        expected = {
            "status": "Accepted"
        }

        outcome = response.json()

        assert outcome == expected

        charge_point.deinit()

    @pytest.mark.xfail
    def test_successful_rejected(self, database_setup):
        pytest.xfail("This feature is not yet implemented")

        charge_box_id = "CP001"

        uri = f"{self.websocket_endpoint}/{charge_box_id}"

        charge_point = ChargePointDummy(uri)

        charge_point.init()

        asyncio.run(
            charge_point.set_charging_profile_conf(ChargingProfileStatus.REJECTED.value)
        )

        api_host = f"/{self.base_path}/{self.path}/{charge_box_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type": "application/json"}

        app.headers = {"api-key": "certi"}

        body = {
            "chargingProfileId" : 1,
            "connectorId" : 0
        }

        app.payload = body

        response = app.request()

        assert response.status_code == HttpResponseStatusCodeType.OK

        expected = {
            "status": "Rejected"
        }

        outcome = response.json()

        assert outcome == expected

        charge_point.deinit()

    @pytest.mark.xfail
    def test_successful_not_supported(self, database_setup):
        pytest.xfail("This feature is not yet implemented")

        charge_box_id = "CP001"

        uri = f"{self.websocket_endpoint}/{charge_box_id}"

        charge_point = ChargePointDummy(uri)

        charge_point.init()

        asyncio.run(
            charge_point.set_charging_profile_conf(ChargingProfileStatus.NOT_SUPPORTED.value)
        )

        api_host = f"/{self.base_path}/{self.path}/{charge_box_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type": "application/json"}

        app.headers = {"api-key": "certi"}

        body = {
            "chargingProfileId" : 1,
            "connectorId" : 0
        }

        app.payload = body

        response = app.request()

        assert response.status_code == HttpResponseStatusCodeType.OK

        expected = {
            "status": "NotSupported"
        }

        outcome = response.json()

        assert outcome == expected

        charge_point.deinit()

    def test_unauthorized(self):
        api_host = f"/{self.base_path}/{self.path}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        response = app.request()

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "error": "Unauthorized",
            "message": "Full authentication is required to access this resource",
            "path": f"http://localhost:8180/{self.base_path}/{self.path}",
            "status": HttpResponseStatusCodeType.UNAUTHORIZED
        }

        outcome = response.json()

        assert outcome.pop("timestamp") is not None

        assert outcome == expected

    @pytest.mark.xfail
    def test_charge_box_id_not_found(self):
        pytest.xfail("This feature is not yet implemented")

        charge_box_id = 2

        api_host = f"/{self.base_path}/{self.path}/{charge_box_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        app.headers = {"api-key":"certi"}

        body = {
            "chargingProfileId" : 1,
            "connectorId": 0
        }

        app.payload = body

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

    @pytest.mark.xfail
    def test_charging_profile_id_not_found(self, database_setup):
        pytest.xfail("This feature is not yet implemented")

        charge_box_id = 1

        api_host = f"/{self.base_path}/{self.path}/{charge_box_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        app.headers = {"api-key":"certi"}

        body = {
            "chargingProfileId" : 2, # should not exist
            "connectorId": 0
        }

        app.payload = body

        response = app.request()

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "error": "Not Found",
            "message": "Could not find this chargingProfileId",
            "path": f"http://localhost:8180/{self.base_path}/{self.path}/{charge_box_id}",
            "status": HttpResponseStatusCodeType.NOT_FOUND
        }

        outcome = response.json()

        assert outcome.pop("timestamp") is not None

        assert outcome == expected
