#/******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import requests
import json

class AppDummy:
    def __init__(self, method, path):
        self.__method = method
        self.__path = path
        self.__payload = {}
        self.__headers = {}

    @property
    def header(self):
        return self.__headers

    @header.setter
    def header(self, v : str) -> None:
        self.__headers.update(v)

    @property
    def method(self) -> str:
        return self.__method

    @property
    def path(self) -> str:
        return self.__path

    @property
    def payload(self) -> str:
        return self.__payload

    @payload.setter
    def payload(self, payload) -> None:
        self.__payload = payload

    def url(self) -> str:
        return 'http://localhost:8180{}'.format(self.path)

    def request(self):
        return requests.request(self.method, self.url(), headers=self.headers,
                                json=self.payload)
