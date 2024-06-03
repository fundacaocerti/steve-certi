#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import pytest

from app_dummy import AppDummy
from enums import HttpResponseStatusCodeType
from db_helper import DatabaseHelper

class TestDeleteChargingProfile:
    @property
    def operation(self) -> str:
        return "DELETE"

    @property
    def base_path(self) -> str:
        return "steve/api/v0/smartCharging"

    @property
    def path(self) -> str:
        return "ChargingProfile"

    def test_successful(self):
        database = DatabaseHelper()

        database.connect()

        database.create_daily_default_profile()

        charging_profile = database.get_any_charging_profile()

        charging_profile_id = charging_profile[0]

        api_host = f"/{self.base_path}/{self.path}/{charging_profile_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        app.headers = {"api-key":"certi"}

        response = app.request()

        assert response.status_code == HttpResponseStatusCodeType.OK

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "status": "OK"
        }

        outcome = response.json()

        assert outcome == expected

        database.delete_all_profiles()

        database.disconnect()

    def test_unauthorized(self) -> None:
        charging_profile_id = 1

        api_host = f"/{self.base_path}/{self.path}/{charging_profile_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        response = app.request()

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "error": "Unauthorized",
            "message": "Full authentication is required to access this resource",
            "path": f"http://localhost:8180/{self.base_path}/{self.path}/{charging_profile_id}",
            "status": HttpResponseStatusCodeType.UNAUTHORIZED
        }

        outcome = response.json()

        assert outcome.pop("timestamp") is not None

        assert outcome == expected

    def test_not_found(self) -> None:
        charging_profile_id = 0

        api_host = f"/{self.base_path}/{self.path}/{charging_profile_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        app.headers = {"api-key":"certi"}

        response = app.request()

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "status": "Resource Not Found"
        }

        outcome = response.json()

        assert outcome == expected
