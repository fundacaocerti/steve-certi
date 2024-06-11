#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import pytest

from app_dummy import AppDummy
from enums import HttpResponseStatusCodeType
from charge_point_dummy import ChargePointDummy
from db_helper import DatabaseHelper

from v16.enums import ClearChargingProfileStatus

class TestTaskStatus:
    @property
    def operation(self) -> str:
        return "GET"

    @property
    def task_initiator_operation(self) -> str:
        return "POST"

    @property
    def task_initiator_base_path(self) -> str:
        return "steve/api/v0/smartCharging"

    @property
    def task_initiator_path(self) -> str:
        return "clearChargingProfile"

    @property
    def base_path(self) -> str:
        return "steve/api/v0/task"

    @property
    def path(self) -> str:
        return "status"

    @property
    def websocket_endpoint(self) -> str:
        return "ws://localhost:8180/steve/websocket/CentralSystemService"

    @pytest.fixture
    def database_setup(self) -> None:
        database = DatabaseHelper()

        database.connect()

        database.delete_all_charge_points()

        database.delete_all_profiles()

        charge_box_id = "CP001"

        database.create_charge_point(charge_box_id)

        database.create_daily_default_profile()

        database.disconnect()

        yield

        database.connect()

        database.delete_all_profiles()

        database.delete_all_charge_points()

        database.disconnect()

    def task_initiate_clear_charging_profile(self, charge_box_id) -> bool:
        api_host = f"/{self.task_initiator_base_path}/{self.task_initiator_path}/{charge_box_id}"

        app = AppDummy(self.task_initiator_operation, api_host)

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

        outcome = response.json()

        assert isinstance(outcome["taskId"], int)

        return outcome["taskId"]

    def test_successful_createdTask_unknown(self, database_setup):
        charge_box_id = "CP001"

        uri = f"{self.websocket_endpoint}/{charge_box_id}"

        charge_point = ChargePointDummy(uri)

        charge_point.init()

        charge_point.clear_charging_profile_conf(ClearChargingProfileStatus.UNKNOWN.value)

        taskId = self.task_initiate_clear_charging_profile(charge_box_id)

        api_host = f"/{self.base_path}/{self.path}/{taskId}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type": "application/json"}

        app.headers = {"api-key": "certi"}

        response = app.request()

        assert response.status_code == HttpResponseStatusCodeType.OK

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "response:": "Unknown",
            "errors:": None,
            "chargeBox:": f'{charge_box_id}'
        }

        outcome = response.json()

        assert outcome == expected

        charge_point.deinit()

    def test_successful_createdTask_accepted(self, database_setup):
        charge_box_id = "CP001"

        uri = f"{self.websocket_endpoint}/{charge_box_id}"

        charge_point = ChargePointDummy(uri)

        charge_point.init()

        charge_point.clear_charging_profile_conf(ClearChargingProfileStatus.ACCEPTED.value)

        taskId = self.task_initiate_clear_charging_profile(charge_box_id)

        api_host = f"/{self.base_path}/{self.path}/{taskId}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type": "application/json"}

        app.headers = {"api-key": "certi"}

        response = app.request()

        assert response.status_code == HttpResponseStatusCodeType.OK

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "response:": "Accepted",
            "errors:": None,
            "chargeBox:": f'{charge_box_id}'
        }

        outcome = response.json()

        assert outcome == expected

        charge_point.deinit()

    def test_successful_createdTask_chargepoint_offline_error(self, database_setup):
        charge_box_id = "CP001"

        taskId = self.task_initiate_clear_charging_profile(charge_box_id)

        api_host = f"/{self.base_path}/{self.path}/{taskId}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type": "application/json"}

        app.headers = {"api-key": "certi"}

        response = app.request()

        assert response.status_code == HttpResponseStatusCodeType.OK

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "response:": None,
            "errors:": f"No session context for chargeBoxId '{charge_box_id}'",
            "chargeBox:": f'{charge_box_id}'
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

    def test_task_not_found(self) -> None:
        charging_profile_id = 0

        api_host = f"/{self.base_path}/{self.path}/{charging_profile_id}"

        app = AppDummy(self.operation, api_host)

        app.headers = {"Content-Type":"application/json"}

        app.headers = {"api-key":"certi"}

        response = app.request()

        assert response.headers["Content-Type"] == "application/json"

        expected = {
            "error": "Not Found",
            "message": f"Could not find taskId {charging_profile_id}",
            "path": f"http://localhost:8180/{self.base_path}/{self.path}/{charging_profile_id}",
            "status": HttpResponseStatusCodeType.NOT_FOUND
        }

        outcome = response.json()

        assert outcome.pop("timestamp") is not None

        assert outcome == expected
