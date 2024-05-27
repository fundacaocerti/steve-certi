#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import pytest

from app_dummy import AppDummy
from enums import HttpResponseStatusCodeType
from charge_point_dummy import ChargePointDummy
from db_helper import DatabaseHelper
import json

class TestAddChargingProfile:
    @property
    def operation(self) -> str:
        return "POST"

    @property
    def base_path(self) -> str:
        return "/steve/api/v0/smartCharging"

    @property
    def path(self) -> str:
        return "ChargingProfile"

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

    def test_successful(self):

        database = DatabaseHelper()

        database.connect()

        api_host = f"/{self.base_path}/{self.path}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        app.headers = {"api-key":"certi"}

        body = {
            "description": "Test Charging Profile",
            "note": "This is a note",
            "stackLevel": 0,
            "chargingProfilePurpose": "CHARGE_POINT_MAX_PROFILE",
            "chargingProfileKind": "ABSOLUTE",
            "recurrencyKind": "DAILY",
            "validFrom": "2024-05-20T10:00:00",
            "validTo": "2024-06-20T10:00:00",
            "durationInSeconds": 3600,
            "startSchedule": "2024-05-21T10:00:00",
            "chargingRateUnit": "W",
            "minChargingRate": 10.0,
            "schedulePeriodMap": {
                "period1": {
                "startPeriodInSeconds": 0,
                "powerLimit": 20.0,
                "numberPhases": 3
                },
                "period2": {
                "startPeriodInSeconds": 1800,
                "powerLimit": 25.0,
                "numberPhases": 3
                }
            }
        }

        app.payload = body

        response = app.request()
        new_charging_profile_id = response.json()['chargingProfileId']
        assert response.status_code == HttpResponseStatusCodeType.CREATED
        assert new_charging_profile_id
        charging_profiles = database.get_charging_profile(new_charging_profile_id)
        assert charging_profiles[0] == new_charging_profile_id
        assert charging_profiles[1] == body['stackLevel']

    def test_unauthorized(self, add_a_charging_point_to_the_database):

        api_host = f"/{self.base_path}/{self.path}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        response = app.request()

        assert response.status_code == HttpResponseStatusCodeType.UNAUTHORIZED

