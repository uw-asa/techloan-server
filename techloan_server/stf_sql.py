"""
Module to support direct communication to the STF SQL database
"""
from django.conf import settings
from django.utils.log import getLogger
import pymssql


class STFSQL(object):
    """STF MSSQL client
    """

    def __init__(self):
        self._log = getLogger('stf_sql')
        self._conn = pymssql.connect(
            settings.STF_SQL_SERVER,
            settings.STF_SQL_USERNAME,
            settings.STF_SQL_PASSWORD,
            getattr(settings, 'STF_SQL_DATABASE', 'stfequip'))
        self._cursor = self._conn.cursor(as_dict=True)

    def __del__(self):
        self._conn.close()

    def availability(self, start_date, end_date, type_id=None):
        if type_id:
            self._cursor.execute(
                "SELECT * FROM availability"
                " WHERE equipment_type_id = %(type_id)d"
                "   AND date_available BETWEEN %(start_date)s"
                "                          AND %(end_date)s", {
                    "type_id": type_id,
                    "start_date": start_date.strftime('%Y%m%d'),
                    "end_date": end_date.strftime('%Y%m%d'),
                })
        else:
            self._cursor.execute(
                "SELECT * FROM availability"
                " WHERE date_available BETWEEN %(start_date)s"
                "                          AND %(end_date)s", {
                    "start_date": start_date.strftime('%Y%m%d'),
                    "end_date": end_date.strftime('%Y%m%d'),
                })

        rows = self._cursor.fetchall()
        for row in rows:
            yield {
                'equipment_type_id': row['equipment_type_id'],
                'date_available': row['date_available'],
                'num_available': row['num_available'],
                'bookable': row['bookable'],
            }

    def equipment_class(self, class_id=None):
        if class_id:
            self._cursor.execute(
                "SELECT * FROM equipment_classes"
                " WHERE id = %(class_id)d",
                {"class_id": class_id})
        else:
            self._cursor.execute(
                "SELECT * FROM equipment_classes"
                " WHERE status = 'active'")

        rows = self._cursor.fetchall()
        for row in rows:
            yield {
                'id': row["id"],
                'name': row["description"],
                'category': row["category"],
                'last_modified': row["modify_time"],
            }

    def equipment_location(self, location_id=None):
        if location_id:
            self._cursor.execute(
                "SELECT * FROM equipment_locations"
                " WHERE id = %(location_id)d",
                {"location_id": location_id})
        else:
            self._cursor.execute(
                "SELECT * FROM equipment_locations"
                " WHERE status = 'active'")

        rows = self._cursor.fetchall()
        for row in rows:
            yield {
                'id': row["id"],
                'name': row["location"],
                'description': row["notes"],
                'last_modified': row["modify_time"],
            }

    def equipment_type(self, type_id=None, class_id=None, location_id=None):
        if type_id:
            self._cursor.execute(
                "SELECT * FROM active_equipment_types"
                " WHERE id = %(type_id)d",
                {"type_id": type_id})
        elif class_id and location_id:
            self._cursor.execute(
                "SELECT * FROM active_equipment_types"
                " WHERE equipment_class_id = %(class_id)d"
                "  AND equipment_location_id = %(location_id)d",
                {"class_id": class_id, "location_id": location_id})
        elif class_id:
            self._cursor.execute(
                "SELECT * FROM active_equipment_types"
                " WHERE equipment_class_id = %(class_id)d",
                {"class_id": class_id})
        elif location_id:
            self._cursor.execute(
                "SELECT * FROM active_equipment_types"
                " WHERE equipment_location_id = %(location_id)d",
                {"location_id": location_id})
        else:
            self._cursor.execute(
                "SELECT * FROM active_equipment_types")

        rows = self._cursor.fetchall()
        for row in rows:
            yield {
                'id': row["id"],
                'equipment_class_id': row["equipment_class_id"],
                'equipment_location_id': row["equipment_location_id"],
                'name': row["name"],
                'make': row["make"],
                'model': row["model"],
                'check_out_days': row["check_out_days"],
                'customer_type_id': row["customer_type_id"],
                'description': row["description"],
                'image_url': row["image_url"],
                'manual_url': row["manual_url"],
                'last_modified': row["modify_time"],
                'stf_funded': row["stf_funded"],
                'num_active': row["num_active"],
            }

    def equipment(self, equipment_id=None, type_id=None):
        if equipment_id:
            self._cursor.execute(
                "SELECT * FROM equipment"
                " WHERE id = %(equipment_id)d",
                {"equipment_id": equipment_id})
        elif type_id:
            self._cursor.execute(
                "SELECT * FROM equipment"
                " WHERE status = 'active' AND equipment_type_id = %(type_id)d",
                {"type_id": type_id})
        else:
            self._cursor.execute(
                "SELECT * FROM equipment"
                " WHERE status = 'active'")

        rows = self._cursor.fetchall()
        for row in rows:
            yield {
                'id': row["id"],
                'equipment_type_id': row["equipment_type_id"],
                'last_modified': row["modify_time"],
            }

    def customer_type(self, customer_type_id=None):
        if customer_type_id:
            self._cursor.execute(
                "SELECT * FROM customer_types"
                " WHERE id = %(customer_type_id)d",
                {"customer_type_id": customer_type_id})
        else:
            self._cursor.execute(
                "SELECT * FROM customer_types")

        rows = self._cursor.fetchall()
        for row in rows:
            yield {
                'id': row["id"],
                'description': row["description"],
            }
