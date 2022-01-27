"""
Module to support direct communication to the STF SQL database
"""
from logging import getLogger

import pyodbc
from django.conf import settings


class STFSQL(object):
    """STF MSSQL client
    """

    def __init__(self):
        self._log = getLogger('stf_sql')
        self._conn = pyodbc.connect(
            driver='{ODBC Driver 17 for SQL Server}',
            server="tcp:%s,1433" % (settings.STF_SQL_SERVER),
            database=getattr(settings, 'STF_SQL_DATABASE', 'stfequip'),
            uid=settings.STF_SQL_USERNAME,
            pwd=settings.STF_SQL_PASSWORD)

    def __del__(self):
        self._conn.close()

    def availability(self, start_date, end_date, type_id=None):
        """Return data from the availability cache

        type_id is optional, can be an int or a list of ints
        """

        cursor = self._conn.cursor()

        if type_id is not None and (
                    isinstance(type_id, str) or
                    not hasattr(type_id, '__iter__')):
            type_id = [type_id]

        if type_id:
            cursor.execute(
                "SELECT * FROM availability"
                " WHERE equipment_type_id IN (?)"
                "   AND date_available BETWEEN ?"
                "                          AND ?", (
                    ','.join(map(str, type_id)),
                    start_date,
                    end_date,
                ))
        else:
            cursor.execute(
                "SELECT * FROM availability"
                " WHERE date_available BETWEEN ?"
                "                          AND ?", (
                    start_date,
                    end_date,
                ))

        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        col = {k: v for k, v in zip(columns, range(len(columns)))}
        cursor.close()
        for row in rows:
            yield {
                'equipment_type_id': row[col['equipment_type_id']],
                'date_available': row[col['date_available']],
                'num_available': row[col['num_available']],
                'bookable': row[col['bookable']],
            }

    def equipment_class(self, class_id=None):
        """Return data from equipment classes

        class_id is optional, can be an int or a list of ints
        """

        cursor = self._conn.cursor()

        if class_id is not None and (
                    isinstance(class_id, str) or
                    not hasattr(class_id, '__iter__')):
            class_id = [class_id]

        if class_id:
            cursor.execute(
                "SELECT * FROM equipment_classes"
                " WHERE id IN (?)",
                ','.join(map(str, class_id)))
        else:
            cursor.execute(
                "SELECT * FROM equipment_classes"
                " WHERE status = 'active'")

        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        col = {k: v for k, v in zip(columns, range(len(columns)))}
        cursor.close()
        for row in rows:
            yield {
                'id': row[col['id']],
                'name': row[col['description']],
                'category': row[col['category']],
                'last_modified': row[col['modify_time']],
            }

    def equipment_location(self, location_id=None):
        """Return data from equipment locations

        location_id is optional, can be an int or a list of ints
        """

        cursor = self._conn.cursor()

        if location_id is not None and (
                    isinstance(location_id, str) or
                    not hasattr(location_id, '__iter__')):
            location_id = [location_id]

        if location_id:
            cursor.execute(
                "SELECT * FROM equipment_locations"
                " WHERE id IN (?)",
                ','.join(map(str, location_id)))
        else:
            cursor.execute(
                "SELECT * FROM equipment_locations"
                " WHERE status = 'active'")

        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        col = {k: v for k, v in zip(columns, range(len(columns)))}
        cursor.close()
        for row in rows:
            yield {
                'id': row[col['id']],
                'name': row[col['location']],
                'description': row[col['notes']],
                'last_modified': row[col['modify_time']],
            }

    def equipment_type(self, type_id=None, class_id=None, location_id=None):
        """Return data from equipment types

        type_id is optional, can be an int or a list of ints
        class_id is optional, can be an int or a list of ints
        location_id is optional, can be an int or a list of ints
        """

        cursor = self._conn.cursor()

        if type_id is not None and (
                    isinstance(type_id, str) or
                    not hasattr(type_id, '__iter__')):
            type_id = [type_id]

        if class_id is not None and (
                    isinstance(class_id, str) or
                    not hasattr(class_id, '__iter__')):
            class_id = [class_id]

        if location_id is not None and (
                    isinstance(location_id, str) or
                    not hasattr(location_id, '__iter__')):
            location_id = [location_id]

        if type_id:
            cursor.execute(
                "SELECT * FROM active_equipment_types"
                " WHERE id IN (?)",
                ','.join(map(str, type_id)))
        elif class_id and location_id:
            cursor.execute(
                "SELECT * FROM active_equipment_types"
                " WHERE equipment_class_id IN (?)"
                "  AND equipment_location_id IN (?)", (
                    ','.join(map(str, class_id)),
                    ','.join(map(str, location_id))))
        elif class_id:
            cursor.execute(
                "SELECT * FROM active_equipment_types"
                " WHERE equipment_class_id IN (?)",
                ','.join(map(str, class_id)))
        elif location_id:
            cursor.execute(
                "SELECT * FROM active_equipment_types"
                " WHERE equipment_location_id IN (?)",
                ','.join(map(str, location_id)))
        else:
            cursor.execute(
                "SELECT * FROM active_equipment_types")

        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        col = {k: v for k, v in zip(columns, range(len(columns)))}
        cursor.close()
        for row in rows:
            yield {
                'id': row[col['id']],
                'equipment_class_id': row[col['equipment_class_id']],
                'equipment_location_id': row[col['equipment_location_id']],
                'name': row[col['name']],
                'make': row[col['make']],
                'model': row[col['model']],
                'check_out_days': row[col['check_out_days']],
                'reservable': row[col['reservable']],
                'description': row[col['description']],
                'image_url': row[col['image_url']],
                'manual_url': row[col['manual_url']],
                'last_modified': row[col['modify_time']],
                'stf_funded': row[col['stf_funded']],
                'num_active': row[col['num_active']],
            }

    def equipment(self, equipment_id=None, type_id=None):
        """Return data from equipment

        equipment_id is optional, can be an int or a list of ints
        type_id is optional, can be an int or a list of ints
        """

        cursor = self._conn.cursor()

        if equipment_id is not None and (
                    isinstance(equipment_id, str) or
                    not hasattr(equipment_id, '__iter__')):
            equipment_id = [equipment_id]

        if type_id is not None and (
                    isinstance(type_id, str) or
                    not hasattr(type_id, '__iter__')):
            type_id = [type_id]

        if equipment_id:
            cursor.execute(
                "SELECT * FROM equipment"
                " WHERE id IN (?)",
                ','.join(map(str, equipment_id)))
        elif type_id:
            cursor.execute(
                "SELECT * FROM equipment"
                " WHERE status = 'active'"
                "   AND equipment_type_id IN (?)",
                ','.join(map(str, type_id)))
        else:
            cursor.execute(
                "SELECT * FROM equipment"
                " WHERE status = 'active'")

        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        col = {k: v for k, v in zip(columns, range(len(columns)))}
        cursor.close()
        for row in rows:
            yield {
                'id': row[col['id']],
                'equipment_type_id': row[col['equipment_type_id']],
                'last_modified': row[col['modify_time']],
            }

    def customer_type(self, customer_type_id=None):
        """Return data from customer_types

        customer_type_id is optional, can be an int or a list of ints
        """

        cursor = self._conn.cursor()

        if customer_type_id is not None and (
                    isinstance(customer_type_id, str) or
                    not hasattr(customer_type_id, '__iter__')):
            customer_type_id = [customer_type_id]

        if customer_type_id:
            cursor.execute(
                "SELECT * FROM customer_types"
                " WHERE id IN (?)",
                ','.join(map(str, customer_type_id)))
        else:
            cursor.execute(
                "SELECT * FROM customer_types")

        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        col = {k: v for k, v in zip(columns, range(len(columns)))}
        cursor.close()
        for row in rows:
            yield {
                'id': row[col['id']],
                'description': row[col['description']],
            }
