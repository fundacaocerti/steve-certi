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

class TestClearChargingProfile:
    @property
    def operation(self) -> str:
        return "POST"

    @property
    def base_path(self) -> str:
        return "steve/api/v0/smartCharging"

    @property
    def path(self) -> str:
        return "clearChargingProfile"

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

        database.re_start_the_automatic_increment_in_the_charging_profile_table()

        database.delete_all_charge_points()

        database.disconnect()

    def test_successful(self, database_setup):
        charge_box_id = "CP001"

        uri = f"{self.websocket_endpoint}/{charge_box_id}"

        charge_point = ChargePointDummy(uri)

        charge_point.init()

        asyncio.run(charge_point.clear_charging_profile_conf())

        api_host = f"/{self.base_path}/{self.path}/{charge_box_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type": "application/json"}

        app.headers = {"api-key": "certi"}

        body = {
            "id" : 1,
            "connectorId" : 0,
            "chargingProfilePurpose": "CHARGE_POINT_MAX_PROFILE"
        }

        app.payload = body

        response = app.request()

        assert response.status_code == HttpResponseStatusCodeType.OK

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "status": "Accepted",
        }

        outcome = response.json()

        assert outcome == expected


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

    def test_not_found(self) -> None:
        charging_profile_id = 2

        api_host = f"/{self.base_path}/{self.path}/{charging_profile_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        app.headers = {"api-key":"certi"}

        response = app.request()

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "error": "Not Found",
            "message": "Could not find this chargingProfileId",
            "path": f"http://localhost:8180/{self.base_path}/{self.path}/{charging_profile_id}",
            "status": HttpResponseStatusCodeType.NOT_FOUND
        }

        outcome = response.json()

        assert outcome.pop("timestamp") is not None

        assert outcome == expected
