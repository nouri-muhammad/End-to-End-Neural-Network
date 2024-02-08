import os 
import sys
from subprocess import run


def main(total_apartments):
    base_dir = os.getcwd()
    scrapy_path = os.path.join(base_dir, "houseRent", "houseRent")
    os.chdir(scrapy_path)
    run_scrapy_file(total_apartments)
    os.chdir(base_dir)
    run_model_file()
    os.chdir(base_dir)
    run_gui()


def run_scrapy_file(total_apartments):
    os.environ['TOTAL_APARTMENTS'] = str(total_apartments)
    command = f'scrapy crawl Rent -s TOTAL_APARTMENTS={total_apartments}'
    run(command , shell=True)


def run_model_file():
    base_dir = os.getcwd()
    file_path = os.path.join(base_dir, "houseRentANN", "components", "data_ingestion.py")
    run(['python', file_path])


def run_gui():
    base_dir = os.getcwd()
    file_path = os.path.join(base_dir, "GUI", "main.py")
    run(['python', file_path])


if __name__=='__main__':
    args = sys.argv
    if len(args) != 2 or not args[1].isdigit():
        raise Exception("You must pass the number of houses you wish to scrape")
    
    # global apartment_num
    apartment_num = args[1]
    main(total_apartments=apartment_num)
