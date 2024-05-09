#/******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import requests

class AppDummy:
    def __init__(self, method, path):
        self.__method = method
        self.__path = path
        self.__key = 'certi'
        self.__payload = None

    @property
    def method(self):
        return self.__method

    @property
    def path(self):
        return self.__path

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key):
        self.__key = key

    @property
    def payload(self):
        return self.__payload

    @payload.setter
    def payload(self, payload):
        self.__payload = payload

    def url(self):
        url = 'http://localhost:8180{}'.format(self.path)

        return url

    def header(self):
        header = {
            'Content-Type':'application/json',
            'api-key':self.key
        }

        return header

    def request(self):
        response = requests.request(
            self.method, self.url(), headers=self.header(), json=self.payload)

        return response
