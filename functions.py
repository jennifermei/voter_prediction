import requests
import numpy as np
import PySimpleGUI as sg
from bs4 import BeautifulSoup

def extract_coords(coords, lats, longs):
    '''
    Extracts latitude and longitude coordinates from GeoJSON coord structures

    Args:
    - coords (list): nested list of coordinates
    - lats (list): stored latitude values
    - longs (list): stored longitude values
    '''
    if isinstance(coords[0], list):
        for part in coords:
            extract_coords(part, lats, longs)
    else:
        longs.append(coords[0])
        lats.append(coords[1])


def calculate_center(coords):
    '''
    Calculates the center latitude and longitude for coordinates

    Args:
    - coords (list): nested list of coordinates
    Returns:
    - center_lat, center_lon (tuple): calculated center latitude and longitude
    '''
    lats, longs = [], []
    extract_coords(coords, lats, longs)
    center_lat = sum(lats) / len(lats)
    center_long = sum(longs) / len(longs)
    return center_lat, center_long


def median(df):
    '''
    Calculates median values for df 

    Args:
    - df (df): df with data
    Returns:
    - median_df (dict): column names as keys and median values as values
    '''
    df = df.drop(['Year','State','State Abbr','State FIPS','District'], axis=1)
    median_values = df.median()
    median_dict = median_values.to_dict()
    return median_dict


def valid_100(category_name, values):
    '''
    Checks if sum of percentages does not exceed 100%

    Args:
    - category_name (list): list of keys of percentage columns
    - values (dict): dictionary with input values
    Returns:
    - bool: True if sum does not exceed 100%, False if it does
    '''
    total_percentage = sum(float(values[f'-IN-{key}'] or 0) for key in category_name)
    if total_percentage > 100:
        return False
    else:
        return True
    

def input_row(title, key_prefix, initial_value=None):
    '''
    Creates a GUI input row with label, output, and input 

    Args: 
    - title (str): label text
    - key_prefix (str): key prefix for elements
    - initial_value: default text for input field
    Returns:
    - list containing GUI elements for input row
    '''
    return [
        sg.Text(f"{title}:", size=(25, 1)),
        sg.Text(size=(10, 1), key=f'-OUTPUT-{key_prefix}'),
        sg.Input(key=f'-IN-{key_prefix}', size=(10, 1), default_text=initial_value)
    ]
    

def get_districts(df, chosen_state):
    '''
    Gets a list of congressional districts for a state

    Args:
    - df (df): df with data
    - chosen_state (str): selected state
    Returns:
    - districts (list): congressional districts for the chosen state
    '''
    districts = []

    for index, row in df.iterrows():
        if row['State'] == chosen_state:
            districts.append(row['District'])

    return districts


def get_percentages(df, new_column, column, total):
    '''
    Calculates and adds a new percentage column to a df

    Args:
    - df (df): df with data
    - new_column (str): name of new column
    - column (str): name of column to use as numerator
    - total (str): name of column to use as denominator
    '''
    df[new_column] = (df[column] / df[total]) * 100
    df[new_column] = df[new_column].round(2)


def get_url(state, year):
    '''
    Generates the URL for a Wikipedia page based on the state and year

    Args:
    - state (str): name of desired state
    - year (int): year of the election
    Returns:
    - url (str): generated wikipedia URL
    '''
    state_url = state.replace(" ", "_")
    multi_url = "https://en.wikipedia.org/wiki/" + str(year) + "_United_States_House_of_Representatives_elections_in_" + state_url
    one_url = "https://en.wikipedia.org/wiki/" + str(year) + "_United_States_House_of_Representatives_election_in_" + state_url

    target_text = "does not have an article"
    response = requests.get(multi_url)
    content = response.text 
    matches = find_exact_match(content, target_text)

    if matches:
        url = one_url
    else:
        url = multi_url

    return url


def find_exact_match(page_content, target_text):
    '''
    Checks if a specific target text exists within a page's content

    Args:
    - page_content (str): HTML content of a web page
    - target_text (str): the target text to search for
    Returns:
    - bool: True if target_text is found, False if not
    '''
    soup = BeautifulSoup(page_content, 'html.parser')
    matches = soup.find_all(string=lambda text: target_text in text)
    return bool(matches)


def replace_if_not_number(string):
    '''
    Replaces a string with 0 if it does not start with a digit
    
    Args:
    - string (str): the input string
    Returns:
    - string (str): original string if it starts with a digit, 0 if not
    '''
    if string and not string[0].isdigit():
        string = "0"
    elif len(string) == 0: 
        string = "0"
    else:
        string = string
    return string


def percentage_within_threshold(y_true, y_pred, threshold_percent=5):
    '''
    Calculates the percentage of predictions within a specified threshold

    Args:
    - y_true (array): true values
    - y_pred (array): predicted values
    - threshold_percent (float): percentage threshold
    Returns:
    - accuracy (float): percentage of predictions within the threshold 
    '''
    threshold = threshold_percent / 100.0
    absolute_errors = np.abs(y_true - y_pred)
    accurate_predictions = np.sum(absolute_errors <= threshold * np.abs(y_true))
    accuracy = (accurate_predictions / len(y_true)) * 100.0
    return accuracy