# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


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
