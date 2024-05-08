#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import logging
import mariadb
import sys

logger = logging.getLogger('DatabaseHelper')

class DatabaseHelper:
    def __init__(self):
        self.__user = 'steve'
        self.__password = 'changeme'
        self.__host = 'steve-certi-db'
        self.__port = 3306
        self.__database = 'stevedb'
        self.__conn = None

    @property
    def user(self):
        return self.__user

    @property
    def password(self):
        return self.__password

    @property
    def host(self):
        return self.__host

    @property
    def port(self):
        return self.__port

    @property
    def database(self):
        return self.__database

    @property
    def conn(self):
        return self.__conn

    @conn.setter
    def conn(self, conn):
        self.__conn = conn

    def connect(self):
        try:
            self.conn = mariadb.connect(
                user = self.user,
                password = self.password,
                host = self.host,
                port = self.port,
                database = self.database
            )

        except mariadb.Error as e:
            logger.error(f"Error connecting to MariaDB platform: {e}")

            sys.exit(1)

    def disconnect(self):
            self.__conn.close()

    def create_charge_point(self, charge_box_id):
        query = 'INSERT INTO charge_box (charge_box_id) VALUES (?)'

        cursor = self.conn.cursor()
        cursor.execute(query, (charge_box_id,))
        self.conn.commit()

    def delete_all_charge_points(self):
        query = 'DELETE FROM charge_box'

        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()

    def create_tag(self, id_tag):
        query = 'INSERT INTO ocpp_tag (id_tag) VALUES (?)'

        cursor = self.conn.cursor()
        cursor.execute(query, (id_tag,))
        self.conn.commit()

    def delete_all_tags(self):
        query = 'DELETE FROM ocpp_tag'

        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
