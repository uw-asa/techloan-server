"""
Module to support direct communication to the STF SQL database
"""
from logging import getLogger

import pymssql
from django.conf import settings


class STFSQL(object):
    """STF MSSQL client
    """

    def __init__(self):
        self._log = getLogger('stf_sql')
        self._conn = pymssql.connect(
            settings.STF_SQL_SERVER,
            settings.STF_SQL_USERNAME,
            settings.STF_SQL_PASSWORD,
            getattr(settings, 'STF_SQL_DATABASE', 'stfequip'),
            charset="ISO-8859-1")

    def __del__(self):
        self._conn.close()

    def availability(self, start_date, end_date, type_id=None):
        """Return data from the availability cache

        type_id is optional, can be an int or a list of ints
        """

        cursor = self._conn.cursor(as_dict=True)

        if type_id is not None and (
                    isinstance(type_id, str) or
                    not hasattr(type_id, '__iter__')):
            type_id = [type_id]

        if type_id:
            cursor.execute(
                "SELECT * FROM availability"
                " WHERE equipment_type_id IN %(type_id)d"
                "   AND date_available BETWEEN %(start_date)s"
                "                          AND %(end_date)s", {
                    "type_id": type_id,
                    "start_date": start_date,
                    "end_date": end_date,
                })
        else:
            cursor.execute(
                "SELECT * FROM availability"
                " WHERE date_available BETWEEN %(start_date)s"
                "                          AND %(end_date)s", {
                    "start_date": start_date,
                    "end_date": end_date,
                })

        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            yield {
                'equipment_type_id': row['equipment_type_id'],
                'date_available': row['date_available'],
                'num_available': row['num_available'],
                'bookable': row['bookable'],
            }

    def equipment_class(self, class_id=None):
        """Return data from equipment classes

        class_id is optional, can be an int or a list of ints
        """

        cursor = self._conn.cursor(as_dict=True)

        if class_id is not None and (
                    isinstance(class_id, str) or
                    not hasattr(class_id, '__iter__')):
            class_id = [class_id]

        if class_id:
            cursor.execute(
                "SELECT * FROM equipment_classes"
                " WHERE id IN %(class_id)d",
                {"class_id": class_id})
        else:
            cursor.execute(
                "SELECT * FROM equipment_classes"
                " WHERE status = 'active'")

        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            yield {
                'id': row["id"],
                'name': row["description"],
                'category': row["category"],
                'last_modified': row["modify_time"],
            }

    def equipment_location(self, location_id=None):
        """Return data from equipment locations

        location_id is optional, can be an int or a list of ints
        """

        cursor = self._conn.cursor(as_dict=True)

        if location_id is not None and (
                    isinstance(location_id, str) or
                    not hasattr(location_id, '__iter__')):
            location_id = [location_id]

        if location_id:
            cursor.execute(
                "SELECT * FROM equipment_locations"
                " WHERE id IN %(location_id)d",
                {"location_id": location_id})
        else:
            cursor.execute(
                "SELECT * FROM equipment_locations"
                " WHERE status = 'active'")

        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            yield {
                'id': row["id"],
                'name': row["location"],
                'description': row["notes"],
                'last_modified': row["modify_time"],
            }

    def equipment_type(self, type_id=None, class_id=None, location_id=None):
        """Return data from equipment types

        type_id is optional, can be an int or a list of ints
        class_id is optional, can be an int or a list of ints
        location_id is optional, can be an int or a list of ints
        """

        cursor = self._conn.cursor(as_dict=True)

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
                " WHERE id IN %(type_id)d",
                {"type_id": type_id})
        elif class_id and location_id:
            cursor.execute(
                "SELECT * FROM active_equipment_types"
                " WHERE equipment_class_id IN %(class_id)d"
                "  AND equipment_location_id IN %(location_id)d",
                {"class_id": class_id, "location_id": location_id})
        elif class_id:
            cursor.execute(
                "SELECT * FROM active_equipment_types"
                " WHERE equipment_class_id IN %(class_id)d",
                {"class_id": class_id})
        elif location_id:
            cursor.execute(
                "SELECT * FROM active_equipment_types"
                " WHERE equipment_location_id IN %(location_id)d",
                {"location_id": location_id})
        else:
            cursor.execute(
                "SELECT * FROM active_equipment_types")

        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            yield {
                'id': row["id"],
                'equipment_class_id': row["equipment_class_id"],
                'equipment_location_id': row["equipment_location_id"],
                'name': row["name"],
                'make': row["make"],
                'model': row["model"],
                'check_out_days': row["check_out_days"],
                'reservable': row["reservable"],
                'description': row["description"],
                'image_url': row["image_url"],
                'manual_url': row["manual_url"],
                'last_modified': row["modify_time"],
                'stf_funded': row["stf_funded"],
                'num_active': row["num_active"],
            }

    def equipment(self, equipment_id=None, type_id=None):
        """Return data from equipment

        equipment_id is optional, can be an int or a list of ints
        type_id is optional, can be an int or a list of ints
        """

        cursor = self._conn.cursor(as_dict=True)

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
                " WHERE id IN %(equipment_id)d",
                {"equipment_id": equipment_id})
        elif type_id:
            cursor.execute(
                "SELECT * FROM equipment"
                " WHERE status = 'active'"
                "   AND equipment_type_id IN %(type_id)d",
                {"type_id": type_id})
        else:
            cursor.execute(
                "SELECT * FROM equipment"
                " WHERE status = 'active'")

        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            yield {
                'id': row["id"],
                'equipment_type_id': row["equipment_type_id"],
                'last_modified': row["modify_time"],
            }

    def customer_type(self, customer_type_id=None):
        """Return data from customer_types

        customer_type_id is optional, can be an int or a list of ints
        """

        cursor = self._conn.cursor(as_dict=True)

        if customer_type_id is not None and (
                    isinstance(customer_type_id, str) or
                    not hasattr(customer_type_id, '__iter__')):
            customer_type_id = [customer_type_id]

        if customer_type_id:
            cursor.execute(
                "SELECT * FROM customer_types"
                " WHERE id IN %(customer_type_id)d",
                {"customer_type_id": customer_type_id})
        else:
            cursor.execute(
                "SELECT * FROM customer_types")

        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            yield {
                'id': row["id"],
                'description': row["description"],
            }
