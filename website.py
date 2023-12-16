import pywebio
import pandas as pd
from dicts import fips
from functions import get_districts
from model import create_models, predict_2020, predict_user_cd
from final_data import get_final_data
from mapping import mapping
from cd_gui import gui_cd
from pywebio.input import *
from pywebio.output import *
from pywebio import *

def website():
    '''
    Creates a web application for election prediction and mapping
    Provides options to select an existing district, make your own, or view the entire map
    '''
    # get state fips codes from dicts
    state_fips = fips()
    state_names = list(state_fips)

    # generate final data to predict on
    data = get_final_data()
    data = data.dropna(axis=0)

    # create Random Forest models for election prediction
    rf_dem, rf_rep, scaler = create_models(data)
    
    while True:
        clear()
        # choose an option for what to view
        choice = radio("Choose a congressional district, make your own, or just look at the whole map!", options=['Select a state and district', 'Make my own district', 'Just show me the entire country!'], required=True)

        # for specified state and congressional district
        if choice == 'Select a state and district':
            # predict elections for 2020 
            pred_2020 = predict_2020(data, rf_dem, rf_rep, scaler)
            # display list of states to choose from
            state = select('Select a state: ', options=state_names)

            if state:
                # display list of districts to choose from within that state
                districts = get_districts(pred_2020, state)
                district = select('Select a congressional district: ', options=districts, required=True)
                if district:
                    # display state and district
                    put_text(f'You selected {state} Congressional District {district}!')
                    put_text("Remember, this is my prediction of the 2020 election, not the real thing.")
                    fig = mapping(pred_2020, state, district)
                    # to account for outdated congressional map
                    if fig == "no json":
                        put_text("Sorry, the JSON we used is an outdated congressional map so that district is unavailable.")
                        try_again = radio("Would you like to try another option?", options=['Yes', 'No'], required=True)
                        if try_again == 'Yes':
                            continue
                    # display map of election prediction
                    html = fig.to_html(include_plotlyjs="require", full_html=False)
                    put_html(html)

        # for if user wants to make their own district
        elif choice == 'Make my own district':
            # provide GUI for users to input demographic profile
            user_cd = gui_cd()
            user_cd_values = list(user_cd.values())
            dem, rep, winner = predict_user_cd(user_cd_values, rf_dem, rf_rep, scaler)
            if user_cd:
                table_data = [['Demographic Feature', 'Percentage']]
                table_data.extend([[key, str(value)] for key, value in user_cd.items()])
                # display election prediction and demographic profile
                put_text(f"Your congressional district will be split: {dem}% Democratic and {rep}% Republican.")
                put_text(f"The {winner} Party wins!")
                put_text("As a reminder, here was your congressional district's demographic profile:")
                put_table(table_data)

        # for viewing overall map
        elif choice == 'Just show me the entire country!':
            put_text("Here's a map of my predictions for the 2020 elections! Feel free to look around.")
            pred_2020 = predict_2020(data, rf_dem, rf_rep, scaler)
            fig = mapping(pred_2020)
            html = fig.to_html(include_plotlyjs="require", full_html=False)
            put_html(html)

        try_again = radio("Would you like to try another option?", options=['Yes', 'No'], required=True)
        if try_again == 'No':
            break 

# start_server(website, port=8080, debug=True)