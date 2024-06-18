import datetime
import pytz
import enum
import json


class MongoCollections(enum.Enum):
    Restaurants = 'Restaurant'
    Orders = 'Orders'
    Clients = 'Clients'


class MongoProcessor:
    def __init__(self):
        self._update_time = datetime.datetime(1900, 1, 1, tzinfo=pytz.utc)

    def process_collection_entry_into_operation(
        self,
        collection: MongoCollections,
        entry: dict,
    ) -> str:
        upload_time: datetime.datetime = datetime.datetime.fromisoformat(entry['update_time'])
        if upload_time > self._update_time:
            self._update_time = upload_time

        if collection == MongoCollections.Restaurants:
            return f"""
                INSERT INTO staging.mongo_restaurant(obj_id, obj_val, when_created, when_updated, when_uploaded)
                VALUES ('{entry['_id']}', '{json.dumps(entry)}', '{entry['update_time']}', '{entry['update_time']}', '{str(datetime.datetime.now(tz=pytz.utc))}')
            """
        elif collection == MongoCollections.Orders:
            return f"""
                INSERT INTO staging.mongo_orders(obj_id, obj_val, when_created, when_updated, when_uploaded)
                VALUES ('{entry['_id']}', '{json.dumps(entry)}', '{entry['update_time']}', '{entry['update_time']}', '{str(datetime.datetime.now(tz=pytz.utc))}')
            """
        elif collection == MongoCollections.Clients:
            return f"""
                INSERT INTO staging.mongo_clients(obj_id, obj_val, when_created, when_updated, when_uploaded)
                VALUES ('{entry['_id']}', '{json.dumps(entry)}', '{entry['update_time']}', '{entry['update_time']}', '{str(datetime.datetime.now(tz=pytz.utc))}')
            """
        else:
            raise RuntimeError(f'Invalid collection: {collection}')

    def get_latest_update_time(self) -> datetime.datetime:
        return self._update_time
