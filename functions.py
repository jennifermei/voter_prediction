import requests
import numpy as np
import PySimpleGUI as sg
from bs4 import BeautifulSoup

def extract_coords(coords, lats, lons):
    if isinstance(coords[0], list):
        for part in coords:
            extract_coords(part, lats, lons)
    else:
        lons.append(coords[0])
        lats.append(coords[1])

def calculate_center(coords):
    lats, lons = [], []
    extract_coords(coords, lats, lons)
    center_lat = sum(lats) / len(lats)
    center_lon = sum(lons) / len(lons)
    return center_lat, center_lon

def median(df):
    df = df.drop(['Year','State','State Abbr','State FIPS','District'], axis=1)
    median_values = df.median()
    median_dict = median_values.to_dict()
    return median_dict

def valid_100(category_name, values):
    total_percentage = sum(float(values[f'-IN-{key}'] or 0) for key in category_name)
    if total_percentage > 100:
        return False
    else:
        return True
    
def input_row(title, key_prefix, initial_value=None):
    return [
        sg.Text(f"{title}:", size=(25, 1)),
        sg.Text(size=(10, 1), key=f'-OUTPUT-{key_prefix}'),
        sg.Input(key=f'-IN-{key_prefix}', size=(10, 1), default_text=initial_value)
    ]
    
def get_districts(df, chosen_state):
    districts = []

    for index, row in df.iterrows():
        if row['State'] == chosen_state:
            districts.append(row['District'])

    return districts

def get_percentages(df, new_column, column, total):
    df[new_column] = (df[column] / df[total]) * 100
    df[new_column] = df[new_column].round(2)