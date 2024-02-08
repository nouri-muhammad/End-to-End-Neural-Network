import os.path
import numpy as np
import pandas as pd
import pickle
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
from tensorflow.keras.models import load_model


preprocessor_file_path = os.path.join("data", "preprocessor.pkl")
model_file_path = os.path.join("data", "model.keras")


def preprocessor_loader(file_path):
    with open(file_path, "rb") as file:
        preprocessor = pickle.load(file)
    return preprocessor


def model_loader(file_path):
    model = load_model(file_path)
    return model


def delete_entry():
    building_type_entry.delete(0, tk.END)
    size_entry.delete(0, tk.END)
    maintenance_fee_entry.delete(0, tk.END)
    deposit_entry.delete(0, tk.END)
    security_deposit_entry.delete(0, tk.END)
    key_money_entry.delete(0, tk.END)
    agency_fee_entry.delete(0, tk.END)
    guarantor_fee_entry.delete(0, tk.END)
    fire_insurance_entry.delete(0, tk.END)
    other_entry.delete(0, tk.END)
    layout_entry.delete(0, tk.END)
    year_built_entry.delete(0, tk.END)
    transaction_type_entry.delete(0, tk.END)
    building_style_entry.delete(0, tk.END)
    short_term_stay_entry.delete(0, tk.END)
    direction_facing_entry.delete(0, tk.END)
    renewal_fee_entry.delete(0, tk.END)
    nearest_station_distance_entry.delete(0, tk.END)
    unit_floor_entry.delete(0, tk.END)
    total_floors_entry.delete(0, tk.END)
    city_entry.delete(0, tk.END)


def pass_values():
    building_type = building_type_entry.get()
    size = size_entry.get()
    maintenance_fee = maintenance_fee_entry.get()
    deposit = deposit_entry.get()
    security_deposit = security_deposit_entry.get()
    key_money = key_money_entry.get()
    agency_fee = agency_fee_entry.get()
    guarantor_fee = guarantor_fee_entry.get()
    fire_insurance = fire_insurance_entry.get()
    other = other_entry.get()
    layout = layout_entry.get()
    year_built = year_built_entry.get()
    transaction_type = transaction_type_entry.get()
    building_style = building_style_entry.get()
    short_term_stay = short_term_stay_entry.get()
    direction_facing = direction_facing_entry.get()
    renewal_fee = renewal_fee_entry.get()
    nearest_station_distance = nearest_station_distance_entry.get()
    unit_floor = unit_floor_entry.get()
    total_floors = total_floors_entry.get()
    city = city_entry.get()
    items = [building_type, size, maintenance_fee, deposit, security_deposit, key_money, agency_fee, guarantor_fee,
             fire_insurance, other, layout, year_built, transaction_type, building_style, short_term_stay,
             direction_facing, renewal_fee, nearest_station_distance, unit_floor, total_floors, city]

    if '' in items:
        messagebox.showwarning(title="Error", message="Please fill all the values")
    else:
        items = {"type": building_type, "size": size, "maintenance_fee": maintenance_fee, "deposit": deposit,
                 "security_deposit": security_deposit, "key_money": key_money, "agency_fee": agency_fee,
                 "guarantor_fee": guarantor_fee, "fire_insurance": fire_insurance, "other": other, "layout": layout,
                 "year_built": year_built, "transaction_type": transaction_type, "building_style": building_type,
                 "short_term_stay": short_term_stay, "direction_facing": direction_facing, "renewal_fee": renewal_fee,
                 "nearest_station_distance": nearest_station_distance, "unit_floor": unit_floor,
                 "total_floors": total_floors, "city": city}
        input_df = pd.DataFrame([items])
        preprocessor = preprocessor_loader(preprocessor_file_path)
        model = model_loader(model_file_path)
        input_features = preprocessor.transform(input_df)
        input_arr = input_features.toarray()
        prediction = model.predict(input_arr)
        result_price.delete("1.0", tk.END)
        result_price.insert("1.0", f"{prediction[0]}")


window = tk.Tk()
window.title("House Rent Price Prediction")
AppFont = font.Font(family='Helvetica', size=12)

frame = tk.Frame(window)
frame.pack()


# user input frame
input_frame = tk.LabelFrame(frame, text="House Properties")
input_frame.grid(row=0, column=0, padx=20, pady=20)


building_type_label = tk.Label(input_frame, text="Building Type", font=AppFont)
building_type_label.grid(row=0, column=0)
type_list = ['Mansion', 'Apartment', 'House', 'Guesthouse', 'Other', 'Office', 'Serviced Apartment']
building_type_entry = ttk.Combobox(input_frame, values=type_list)
building_type_entry.grid(row=0, column=1)

size_label = tk.Label(input_frame, text="Size", font=AppFont)
size_label.grid(row=1, column=0)
size_entry = tk.Spinbox(input_frame, from_=0, to=5000, increment=1.0)
size_entry.grid(row=1, column=1)

maintenance_fee_label = tk.Label(input_frame, text="Maintenance Fee")
maintenance_fee_label.grid(row=2, column=0)
maintenance_fee_entry = tk.Spinbox(input_frame, from_=0, to=5000, increment=1.0)
maintenance_fee_entry.grid(row=2, column=1)

deposit_label = tk.Label(input_frame, text="Deposit", font=AppFont)
deposit_label.grid(row=3, column=0)
deposit_entry = tk.Spinbox(input_frame, from_=0, to=5000, increment=1.0)
deposit_entry.grid(row=3, column=1)

security_deposit_label = tk.Label(input_frame, text="Security Deposit", font=AppFont)
security_deposit_label.grid(row=4, column=0)
security_deposit_entry = tk.Spinbox(input_frame, from_=0, to=5000, increment=1.0)
security_deposit_entry.grid(row=4, column=1)

key_money_label = tk.Label(input_frame, text="Key Money")
key_money_label.grid(row=5, column=0)
key_money_entry = tk.Spinbox(input_frame, from_=0, to=5000, increment=1.0)
key_money_entry.grid(row=5, column=1)

agency_fee_label = tk.Label(input_frame, text="Agency Fee", font=AppFont)
agency_fee_label.grid(row=6, column=0)
agency_fee_entry = tk.Spinbox(input_frame, from_=0, to=5000, increment=1.0)
agency_fee_entry.grid(row=6, column=1)


guarantor_fee_label = tk.Label(input_frame, text="Guarantor Fee", font=AppFont)
guarantor_fee_label.grid(row=0, column=2)
guarantor_fee_entry = tk.Spinbox(input_frame, from_=0, to=5000, increment=1.0)
guarantor_fee_entry.grid(row=0, column=3)

fire_insurance_label = tk.Label(input_frame, text="Fire Insurance", font=AppFont)
fire_insurance_label.grid(row=1, column=2)
fire_insurance_entry = tk.Spinbox(input_frame, from_=0, to=5000, increment=1.0)
fire_insurance_entry.grid(row=1, column=3)

other_label = tk.Label(input_frame, text="Other Costs", font=AppFont)
other_label.grid(row=2, column=2)
other_entry = tk.Spinbox(input_frame, from_=0, to=5000, increment=1.0)
other_entry.grid(row=2, column=3)


layout_label = tk.Label(input_frame, text="Layout")
layout_label.grid(row=3, column=2)
layout_list = ['1K', '1R', '1LDK', '2LDK', '2DK', '1DK', '3LDK', '3DK', '2K', '4LDK', '1SLDK', '2SLDK', 'Shared',
               '1SDK', '3SLDK', '1SK', '4K', '3K', '4SLDK', '4SDK', 'Office']
layout_entry = ttk.Combobox(input_frame, values=layout_list)
layout_entry.grid(row=3, column=3)

year_built_label = tk.Label(input_frame, text="Year Built", font=AppFont)
year_built_label.grid(row=4, column=2)
year_built_values = list(np.arange(1910, 2024))
year_built_entry = ttk.Combobox(input_frame, values=year_built_values)
year_built_entry.grid(row=4, column=3)

transaction_type_label = tk.Label(input_frame, text="Transaction Type", font=AppFont)
transaction_type_label.grid(row=5, column=2)
transaction_type_list = ['Direct', 'Brokerage', 'Non-Exclusive', 'Property Owner', 'Exclusive', 'Referral']
transaction_type_entry = ttk.Combobox(input_frame, values=transaction_type_list)
transaction_type_entry.grid(row=5, column=3)

building_style_label = tk.Label(input_frame, text="Building Style")
building_style_label.grid(row=6, column=2)
building_style_list = ['Normal', 'Designers', 'European']
building_style_entry = ttk.Combobox(input_frame, values=building_style_list)
building_style_entry.grid(row=6, column=3)


short_term_stay_label = tk.Label(input_frame, text="Short Term Stay", font=AppFont)
short_term_stay_label.grid(row=0, column=4)
short_term_stay_list = [0, 1]
short_term_stay_entry = ttk.Combobox(input_frame, values=short_term_stay_list)
short_term_stay_entry.grid(row=0, column=5)

direction_facing_label = tk.Label(input_frame, text="Building Direction", font=AppFont)
direction_facing_label.grid(row=1, column=4)
direction_facing_list = [
    'South', 'East, West', 'East', 'West', 'Southeast', 'Southwest', 'North', 'Northeast', 'Northwest',
    'South, Southwest', 'South, West', 'Southeast, South', 'East, South', 'Southeast, Northwest', 'East, Southeast',
    'Southwest, Northwest', 'North, West', 'Southeast, Southwest',
    'North, Northeast, East, Southeast, South, Southwest, West, Northwest', 'North, Northwest', 'North, South',
    'Northeast, Southwest', 'North, South, West', 'Northeast, Southeast, Southwest, Northwest', 'East, South, West',
    'Northeast, East, Southwest, West', 'West, Northwest', 'North, Southeast, Northwest', 'Southwest, West',
    'Northeast, Southeast, Southwest', 'Northeast, Northwest'
]
direction_facing_entry = ttk.Combobox(input_frame, values=direction_facing_list)
direction_facing_entry.grid(row=1, column=5)


renewal_fee_label = tk.Label(input_frame, text="Renewal Fee", font=AppFont)
renewal_fee_label.grid(row=2, column=4)
renewal_fee_entry = tk.Spinbox(input_frame, from_=0, to=5000, increment=1.0)
renewal_fee_entry.grid(row=2, column=5)

nearest_station_distance_label = tk.Label(input_frame, text="Nearest Station (min)", font=AppFont)
nearest_station_distance_label.grid(row=3, column=4)
nearest_station_distance_values = list(np.arange(1, 61))
nearest_station_distance_entry = ttk.Combobox(input_frame, values=nearest_station_distance_values)
nearest_station_distance_entry.grid(row=3, column=5)

unit_floor_label = tk.Label(input_frame, text="Unit Floor")
unit_floor_label.grid(row=4, column=4)
unit_floor_values = list(np.arange(1, 51))
unit_floor_entry = ttk.Combobox(input_frame, values=unit_floor_values)
unit_floor_entry.grid(row=4, column=5)

total_floors_label = tk.Label(input_frame, text="Total Floors", font=AppFont)
total_floors_label.grid(row=5, column=4)
total_floors_values = list(np.arange(1, 51))
total_floors_entry = ttk.Combobox(input_frame, values=total_floors_values)
total_floors_entry.grid(row=5, column=5)

city_label = tk.Label(input_frame, text="City", font=AppFont)
city_label.grid(row=6, column=4)
city_list = ['Tokyo', 'Kanagawa', 'Okinawa', 'Chiba', 'Saitama', 'Osaka', 'Fukuoka', 'Kyoto', 'Aichi', 'Nagasaki',
             'Hyogo', 'Hiroshima', 'Oita', 'Edogawa-ku', 'Hokkaido', 'Kochi', 'Kagawa', 'Tokushima']
city_entry = ttk.Combobox(input_frame, values=city_list)
city_entry.grid(row=6, column=5)

delete_button = tk.Button(
    input_frame,
    text="Clear Entry",
    width=15,
    font=("Arial", 14, "bold"),
    command=delete_entry
)
delete_button.grid(row=7, column=4)

prediction_button = tk.Button(
    input_frame,
    text="Predict Price",
    width=15,
    font=("Arial", 14, "bold"),
    command=pass_values
)
prediction_button.grid(row=7, column=5)

col_count, row_count = input_frame.grid_size()
for col in range(col_count):
    input_frame.grid_columnconfigure(col, minsize=200)
for row in range(row_count):
    input_frame.grid_rowconfigure(row, minsize=30)


# result frame
result_frame = tk.LabelFrame(frame, text="Price")
result_frame.grid(row=1, column=0, sticky="news", padx=20, pady=20)
result_price = tk.Text(result_frame, height=2, width=50, font=("Arial", "24"))
result_price.pack(expand=True, fill=tk.BOTH)

window.mainloop()
