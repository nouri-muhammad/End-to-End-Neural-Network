# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from datetime import datetime
import scrapy


class HouserentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class HouseItems(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    unit_number = scrapy.Field()
    building_name = scrapy.Field()
    floor = scrapy.Field()
    available = scrapy.Field()
    type = scrapy.Field()
    size = scrapy.Field()
    location = scrapy.Field()
    nearest_station = scrapy.Field()
    rent = scrapy.Field()
    maintenance_fee = scrapy.Field()
    other_costs = scrapy.Field()
    monthly_cost = scrapy.Field()
    deposit = scrapy.Field()
    security_deposit = scrapy.Field()
    key_money = scrapy.Field()
    agency_fee = scrapy.Field()
    guarantor_fee = scrapy.Field()
    fire_insurance = scrapy.Field()
    other = scrapy.Field()
    total_move_in_fee = scrapy.Field()
    layout = scrapy.Field()
    year_built = scrapy.Field()
    transaction_type = scrapy.Field()
    building_style = scrapy.Field()
    short_term_stay = scrapy.Field()
    direction_facing = scrapy.Field()
    building_description = scrapy.Field()
    other_expenses = scrapy.Field()
    renewal_fee = scrapy.Field()
    date_updated = scrapy.Field(
        input_processor=lambda x: datetime.strptime(x, '%b %d, %Y'),
        output_processor=lambda x: x.strftime('%Y-%m-%d')
    )
    next_update_schedule = scrapy.Field(
        input_processor=lambda x: datetime.strptime(x, '%b %d, %Y'),
        output_processor=lambda x: x.strftime('%Y-%m-%d')
    )
    property_description = scrapy.Field()
    features = scrapy.Field()
    stations = scrapy.Field()
    transportation = scrapy.Field()
