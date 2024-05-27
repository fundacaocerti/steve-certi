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
        return "POST"

    @property
    def base_path(self) -> str:
        return "steve/api/v0/smartCharging"

    @property
    def path(self) -> str:
        return "deleteChargingProfile"

    @property
    def websocket_endpoint(self) -> str:
        return "ws://localhost:8180/steve/websocket/CentralSystemService"

    @pytest.fixture
    def database_setup(self):
        database = DatabaseHelper()

        database.connect()

        database.create_charging_profile()

        database.disconnect()

        yield

        # No action is needed
    @pytest.mark.xfail(reason="Não implementado")
    def test_successful(self, database_setup):
        charging_profile_id = 1

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
