#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import pytest
import json

from app_dummy.app_dummy import AppDummy
from app_dummy.enums import HttpResponseStatusCodeType
from db_helper.db_helper import DatabaseHelper

@pytest.fixture
def setup_database():
    database = DatabaseHelper()

    database.connect()
    database.create_charge_point('CP001')
    database.create_tag('TAG001')
    database.create_tag('TAG002')
    database.disconnect()

    yield

    database.connect()
    database.delete_all_tags()
    database.delete_all_charge_points()
    database.disconnect()

@pytest.fixture
def setup_get_ocpp_tags():
    return AppDummy('GET', '/steve/api/v1/ocppTags')

def test_get_ocpp_tags_successful(setup_database, setup_get_ocpp_tags):
    response = setup_get_ocpp_tags.request()

    assert response.status_code == HttpResponseStatusCodeType.OK

    assert response.headers['Content-Type'] == 'application/json'

    assert isinstance(response.json(), list)

    assert len(response.json()) > 0

    expected = {
        "activeTransactionCount":0,
        "blocked": False,
        "expiryDate": None,
        "idTag": "TAG001",
        "inTransaction": False,
        "maxActiveTransactionCount": 1,
        "note": None,
        "parentIdTag": None,
        "parentOcppTagPk": None
    }

    outcome = response.json()[0]

    assert outcome.pop('ocppTagPk') is not None

    assert outcome == expected

    expected = {
        "activeTransactionCount":0,
        "blocked": False,
        "expiryDate": None,
        "idTag": "TAG002",
        "inTransaction": False,
        "maxActiveTransactionCount": 1,
        "note": None,
        "parentIdTag": None,
        "parentOcppTagPk": None
    }

    outcome = response.json()[1]

    assert outcome.pop('ocppTagPk') is not None

    assert outcome == expected

def test_get_ocpp_tags_unauthorized(setup_database, setup_get_ocpp_tags):
    WRONG_KEY = '"!@#$'

    setup_get_ocpp_tags.key = WRONG_KEY

    response = setup_get_ocpp_tags.request()

    expected = {
        "error": "Unauthorized",
        "message": "Full authentication is required to access this resource",
        "path": "http://localhost:8180/steve/api/v1/ocppTags",
        "status": 401
    }

    outcome = response.json()

    assert outcome.pop('timestamp') is not None

    assert outcome == expected

@pytest.fixture
def setup_post_ocpp_tags():
    return AppDummy('POST', '/steve/api/v1/ocppTags')

def test_post_ocpp_tags_successful(setup_database, setup_post_ocpp_tags):
    setup_post_ocpp_tags.payload = {
        "idTag":"TAG003",
        "maxActiveTransactionCount": 2,
        "note": "just for testing"
    }

    response = setup_post_ocpp_tags.request()

    assert response.status_code == HttpResponseStatusCodeType.CREATED

    expected = {
        "activeTransactionCount":0,
        "blocked": False,
        "expiryDate": None,
        "idTag": "TAG003",
        "inTransaction": False,
        "maxActiveTransactionCount": 2,
        "note": "just for testing",
        "parentIdTag": None,
        "parentOcppTagPk": None
    }

    outcome = response.json()

    assert outcome.pop('ocppTagPk') is not None

    assert outcome == expected

def test_post_ocpp_tags_unauthorized(setup_database, setup_post_ocpp_tags):
    WRONG_KEY = '+_)(*'

    setup_post_ocpp_tags.key = WRONG_KEY

    response = setup_post_ocpp_tags.request()

    expected = {
        "error": "Unauthorized",
        "message": "Full authentication is required to access this resource",
        "path": "http://localhost:8180/steve/api/v1/ocppTags",
        "status": 401
    }

    outcome = response.json()

    assert outcome.pop('timestamp') is not None

    assert outcome == expected
