import os
import random
import scrapy
import time
from houseRent.items import HouseItems


class RentSpider(scrapy.Spider):
    name = "Rent"
    allowed_domains = ["apartments.gaijinpot.com"]
    start_urls = ["https://apartments.gaijinpot.com/en/rent/listing"]
    # start_urls = ["https://apartments.gaijinpot.com/en/rent/listing?page=9"]
    item = 0
    while True:
        try:
            count = int(input("Insert the number of items to scrape: "))
            break
        except ValueError:
            print("Invalid Entry")

    def parse(self, response):
        apartments = response.xpath("//div[@class='property-listing listing-special']")
        if len(apartments) == 0:
            apartments = response.xpath("//div[@class='property-listing']")

        for apartment in apartments:
            apartment_url = apartment.xpath(".//div[@class='listing-footer']//div[@class='listing-right-col']/a/@href").get()
            if apartment_url:
                apartment_url = 'https://apartments.gaijinpot.com' + apartment_url
                time.sleep(1)
                yield response.follow(apartment_url, callback=self.parse_apartment_page)

            self.item += 1
            if self.item == self.count:
                break

        next_page = response.xpath("//div[@class='clearfix mt-30 mb-30']//ul[@class='paginator']//li[@class='pagination-next']/a/@href").get()
        if next_page and self.item < self.count:
            time.sleep(random.uniform(1, 2))
            next_page_url = 'https://apartments.gaijinpot.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)

    @staticmethod
    def parse_apartment_page(response):
        house_item = HouseItems()
        house_item["name"] = response.xpath("//div[@class='property-details']//h1[@class='property-headline']//span[@itemprop='name']/text()").get()
        house_item["price"] = response.xpath("//div[@class='property-details']//h1[@class='property-headline']//strong[@class='price']/text()").get()
        house_item["unit_number"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][1]//dt[contains(text(), 'Unit Number')]/following-sibling::dd[1]/text()").get()
        house_item["building_name"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][1]//dt[contains(text(), 'Building Name')]/following-sibling::dd[1]/text()").get()
        house_item["floor"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][1]//dt[contains(text(), 'Floor')]/following-sibling::dd[1]/text()").get()
        house_item["available"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][1]//dt[contains(text(), 'Available From')]/following-sibling::dd[1]/text()").get()
        house_item["type"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][1]//dt[contains(text(), 'Type')]/following-sibling::dd[1]/text()").get()
        house_item["size"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][1]//dt[contains(text(), 'Size')]/following-sibling::dd[1]/text()").get()
        house_item["location"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][1]//dt[contains(text(), 'Location')]/following-sibling::dd[1]/text()").get()
        house_item["nearest_station"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][1]//dt[contains(text(), 'Nearest Station')]/following-sibling::dd[1]/text()").get()
        house_item["rent"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][2]//dl[@class='mb-0'][1]/dt[contains(text(), 'Rent')]/following-sibling::dd[1]/text()").get()
        house_item["maintenance_fee"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][2]//dl[@class='mb-0'][1]/dt[contains(text(), 'Maintenance Fee')]/following-sibling::dd[1]/text()").get()
        house_item["other_costs"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][2]//h5[contains(text(), 'Monthly')]/following-sibling::dl[@class='mb-0']//dt[contains(text(), 'Other')]/following-sibling::dd[1]/text()").get()
        house_item["monthly_cost"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][2]//h5[contains(text(), 'Monthly')]/following-sibling::dl[@class='mb-0']//dt[contains(text(), 'Total Monthly Cost')]/following-sibling::dd[1]/text()").get()
        house_item["deposit"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][2]//h5[contains(text(), 'Total to Move In')]/following-sibling::dl//dt[contains(text(), 'Deposit')][1]/following-sibling::dd[1]/text()").get()
        house_item["security_deposit"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][2]//h5[contains(text(), 'Total to Move In')]/following-sibling::dl//dt[contains(text(), 'Security Deposit')][1]/following-sibling::dd[1]/text()").get()
        house_item["key_money"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][2]//h5[contains(text(), 'Total to Move In')]/following-sibling::dl//dt[contains(text(), 'Key Money')][1]/following-sibling::dd[1]/text()").get()
        house_item["agency_fee"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][2]//h5[contains(text(), 'Total to Move In')]/following-sibling::dl//dt[contains(text(), 'Agency Fee')][1]/following-sibling::dd[1]/text()").get()
        house_item["guarantor_fee"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][2]//h5[contains(text(), 'Total to Move In')]/following-sibling::dl//dt[contains(text(), 'Guarantor Fee')][1]/following-sibling::dd[1]/text()").get()
        house_item["fire_insurance"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][2]//h5[contains(text(), 'Total to Move In')]/following-sibling::dl//dt[contains(text(), 'Fire Insurance')][1]/following-sibling::dd[1]/text()").get()
        house_item["other"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][2]//h5[contains(text(), 'Total to Move In')]/following-sibling::dl//dt[contains(text(), 'Other')][1]/following-sibling::dd[1]/text()").get()
        house_item["total_move_in_fee"] = response.xpath("//div[@class='property-details']//div[@class='clearfix'][1]//div[@class='col-sm-7 col-right'][2]//h5[contains(text(), 'Total to Move In')]/following-sibling::dl//dt[contains(text(), 'Total Move-In Fees')][1]/following-sibling::dd[1]/text()").get()
        house_item["layout"] = response.xpath("//div[@class='col-sm-7 col-right']//h4[contains(text(), 'Additional Details')]/following-sibling::dl//dt[contains(text(), 'Layout')]/following-sibling::dd[1]/text()").get()
        house_item["year_built"] = response.xpath("//div[@class='col-sm-7 col-right']//h4[contains(text(), 'Additional Details')]/following-sibling::dl//dt[contains(text(), 'Year Built')]/following-sibling::dd[1]/text()").get()
        house_item["transaction_type"] = response.xpath("//div[@class='col-sm-7 col-right']//h4[contains(text(), 'Additional Details')]/following-sibling::dl//dt[contains(text(), 'Transaction Type')]/following-sibling::dd[1]/text()").get()
        house_item["building_style"] = response.xpath("//div[@class='col-sm-7 col-right']//h4[contains(text(), 'Additional Details')]/following-sibling::dl//dt[contains(text(), 'Building Style')]/following-sibling::dd[1]/text()").get()
        house_item["short_term_stay"] = response.xpath("//div[@class='col-sm-7 col-right']//h4[contains(text(), 'Additional Details')]/following-sibling::dl//dt[contains(text(), 'Short Term Stay')]/following-sibling::dd[1]/text()").get()
        house_item["direction_facing"] = response.xpath("//div[@class='col-sm-7 col-right']//h4[contains(text(), 'Additional Details')]/following-sibling::dl//dt[contains(text(), 'Direction Facing')]/following-sibling::dd[1]/text()").get()
        house_item["building_description"] = response.xpath("//div[@class='col-sm-7 col-right']//h4[contains(text(), 'Additional Details')]/following-sibling::dl//dt[contains(text(), 'Building Description')]/following-sibling::dd[1]/text()").getall()
        house_item["other_expenses"] = response.xpath("//div[@class='col-sm-7 col-right']//h4[contains(text(), 'Additional Details')]/following-sibling::dl//dt[contains(text(), 'Other Expenses')]/following-sibling::dd[1]/text()").getall()
        house_item["renewal_fee"] = response.xpath("//div[@class='col-sm-7 col-right']//h4[contains(text(), 'Additional Details')]/following-sibling::dl//dt[contains(text(), 'Renewal Fee')]/following-sibling::dd[1]/text()").get()
        house_item["date_updated"] = response.xpath("//div[@class='col-sm-7 col-right']//h4[contains(text(), 'Additional Details')]/following-sibling::dl//dt[contains(text(), 'Date Updated')]/following-sibling::dd[1]/text()").get()
        house_item["next_update_schedule"] = response.xpath("//div[@class='col-sm-7 col-right']//h4[contains(text(), 'Additional Details')]/following-sibling::dl//dt[contains(text(), 'Next Update Schedule')]/following-sibling::dd[1]/text()").get()
        house_item["property_description"] = response.xpath("//div[@class='col-sm-7 col-right']//h4[contains(text(), 'Property Description')]/following-sibling::div[1]/text()").getall()
        house_item["features"] = response.xpath("//div[@class='col-sm-7 col-right']//h4[contains(text(), 'Features')]/following-sibling::div[@class='detail-item features-item']/text()").getall()
        house_item["stations"] = response.xpath("//div[@itemtype='http://schema.org/TrainStation']//span/text()").getall()
        house_item["transportation"] = response.xpath("//li[@class='has-icon']/text()").getall()

        yield house_item
