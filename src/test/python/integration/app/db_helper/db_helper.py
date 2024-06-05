#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import logging
import mariadb
import sys
import json

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

    def get_charging_profile(self, charging_profile_id):
        query = 'SELECT * FROM charging_profile WHERE charging_profile_pk=(?)'

        cursor = self.conn.cursor()
        cursor.execute(query, (charging_profile_id,))

        # Fetch the results
        result = cursor.fetchone()

        # Check if a result was found
        return result

    def get_any_charging_profile(self):
        query = 'SELECT * FROM charging_profile'

        cursor = self.conn.cursor()
        cursor.execute(query)

        # Fetch the results
        result = cursor.fetchone()

        # Check if a result was found
        return result

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

    def create_daily_default_profile(self):
        ##
        # The following data structure describes a daily default profile that
        # limits the power to 6 kW between 08:00h and 20:00h.

        cursor = self.conn.cursor()

        q1 = '''
             INSERT INTO charging_profile
                (
                 stack_level,
                 charging_profile_purpose,
                 charging_profile_kind,
                 recurrency_kind,
                 charging_rate_unit,
                 start_schedule,
                 duration_in_seconds
                )
             VALUES
                (0, 'TxDefaultProfile', 'Recurring', 'Daily', 'W', NOW(), 86400);
             '''
        cursor.execute(q1)

        q2 = "SET @charging_profile_pk = LAST_INSERT_ID();"
        cursor.execute(q2)

        q3 = '''
             INSERT INTO charging_schedule_period
                (
                 charging_profile_pk,
                 start_period_in_seconds,
                 power_limit
                )
             VALUES
                (@charging_profile_pk, 0, 11000),
                (@charging_profile_pk, 28800, 6000),
                (@charging_profile_pk, 72000, 11000);
             '''
        cursor.execute(q3)

        self.conn.commit()

    def delete_all_profiles(self):
        cursor = self.conn.cursor()

        q1 = "DELETE FROM charging_profile"
        cursor.execute(q1)

        q2 = "ALTER TABLE charging_profile AUTO_INCREMENT = 1"
        cursor.execute(q2)

        self.conn.commit()
