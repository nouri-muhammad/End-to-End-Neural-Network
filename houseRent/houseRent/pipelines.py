# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class HouserentPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name == 'agency_fee':
                value = adapter.get(field_name)
                if value and '¥' in value:
                    adapter[field_name] = value[1:]

            elif field_name == 'building_description':
                value = adapter.get(field_name)
                if value:
                    adapter[field_name] = ''.join(value).replace('\n', '').replace('\t', '').replace('\r', '')

            elif field_name == 'deposit':
                value = adapter.get(field_name)
                if value and '¥' in value:
                    adapter[field_name] = value[1:]

            elif field_name == 'features':
                value = adapter.get(field_name)
                if value:
                    adapter[field_name] = ''.join(value).replace('\n', '').replace('\t', '').replace('\r', '')

            elif field_name == 'fire_insurance':
                value = adapter.get(field_name)
                if value and '¥' in value:
                    adapter[field_name] = value[1:]

            elif field_name == 'floor':
                value = adapter.get(field_name)
                if value:
                    first = value[:value.index('/')].strip()
                    second = value[value.index('/')+2:-1]
                    adapter[field_name] = f"{first},{second}"
                else:
                    adapter[field_name] = ''

            elif field_name == 'guarantor_fee':
                value = adapter.get(field_name)
                adapter[field_name] = value[1:]

            elif field_name == 'key_money':
                value = adapter.get(field_name)
                if value and '¥' in value:
                    value = value.replace('\n', '').replace('\t', '').replace('\r', '')
                    adapter[field_name] = value[1:]

            elif field_name == 'maintenance_fee':
                value = adapter.get(field_name)
                if value and '¥' in value:
                    adapter[field_name] = value[1:]

            elif field_name == 'monthly_cost':
                value = adapter.get(field_name)
                if value and '¥' in value:
                    adapter[field_name] = value[1:]

            elif field_name == 'nearest_station':
                value = adapter.get(field_name)
                if value:
                    adapter[field_name] = value.replace('\n', '').replace('\t', '').replace('\r', '')

            elif field_name == 'other':
                value = adapter.get(field_name)
                if value and '¥' in value:
                    adapter[field_name] = value[1:]

            elif field_name == 'other_costs':
                value = adapter.get(field_name)
                if value and '¥' in value:
                    adapter[field_name] = value[1:]

            elif field_name == 'other_expenses':
                value = adapter.get(field_name)
                if value:
                    value = ''.join(value).replace('\n', '').replace('\t', '').replace('\r', '')
                    adapter[field_name] = value

            elif field_name == 'price':
                value = adapter.get(field_name)
                if value and '¥' in value:
                    adapter[field_name] = value[1:]

            elif field_name == 'property_description':
                value = adapter.get(field_name)
                if value:
                    adapter[field_name] = ''.join(value).replace('\n', '').replace('\t', '').replace('\r', '')

            elif field_name == 'renewal_fee':
                value = adapter.get(field_name)
                if value and '¥' in value:
                    adapter[field_name] = value[1:]

            elif field_name == 'rent':
                value = adapter.get(field_name)
                if value and '¥' in value:
                    adapter[field_name] = value[1:]

            elif field_name == 'security_deposit':
                value = adapter.get(field_name)
                if value and '¥' in value:
                    adapter[field_name] = value[1:]

            elif field_name == 'size':
                value = adapter.get(field_name)
                if value and 'm²' in value:
                    adapter[field_name] = value[:-2]

            elif field_name == 'stations':
                value = adapter.get(field_name)
                if value:
                    adapter[field_name] = [station.strip() for station in value]

            elif field_name == 'total_move_in_fee':
                value = adapter.get(field_name)
                if value and '¥' in value:
                    adapter[field_name] = value[1:]

            elif field_name == 'transportation':
                value = adapter.get(field_name)
                if value:
                    adapter[field_name] = [transportation.strip() for transportation in value]

        return item


class MongoDBPipeline:
    def __init__(self, mongo_uri="mongodb://localhost:27017/", db_name="apartments"):
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]

    def open_spider(self, spider):
        self.db = self.client[spider.settings.get('DB_NAME', self.db_name)]
        if not self.db.name in self.client.list_database_names():
            self.client.drop_database(self.db.name)
            self.db = self.client[spider.settings.get('DB_NAME', self.db_name)]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = spider.settings.get('COLLECTION_NAME', 'items')
        self.db[collection_name].insert_one(dict(item))
        return item
