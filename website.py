import pywebio
import pandas as pd
from dicts import fips
from functions import get_districts
from model import create_models, predict_2020, predict_user_cd
from mapping import mapping
from cd_gui import gui_cd
from pywebio.input import *
from pywebio.output import *

def website():

    state_fips = fips()
    state_names = list(state_fips)

    # data = get_final_data()
    data = pd.read_csv('final_data.csv')
    data = data.dropna(axis=0)

    rf_dem, rf_rep, scaler = create_models(data)
    
    while True:
        clear()
        choice = radio("Choose a congressional district, make your own, or just look at the whole map!", options=['Select a state and district', 'Make my own district', 'Just show me the entire country!'], required=True)

        if choice == 'Select a state and district':
            pred_2020 = predict_2020(data, rf_dem, rf_rep, scaler)
            state = select('Select a state: ', options=state_names)

            if state:
                districts = get_districts(pred_2020, state)
                district = select('Select a congressional district: ', options=districts, required=True)
                if district:
                    put_text(f'You selected {state} Congressional District {district}!')
                    put_text("Remember, this is my prediction of the 2020 election, not the real thing.")
                    fig = mapping(pred_2020, state, district)
                    if fig == "no json":
                        put_text("Sorry, the JSON we used is behind a congressional map so that district is unavailable.")
                        try_again = radio("Would you like to try another option?", options=['Yes', 'No'], required=True)
                        if try_again == 'Yes':
                            continue
                    html = fig.to_html(include_plotlyjs="require", full_html=False)
                    put_html(html)

        elif choice == 'Make my own district':
            user_cd = gui_cd()
            user_cd_values = list(user_cd.values())
            dem, rep, winner = predict_user_cd(user_cd_values, rf_dem, rf_rep, scaler)
            if user_cd:
                table_data = [['Demographic Feature', 'Percentage']]
                table_data.extend([[key, str(value)] for key, value in user_cd.items()])
                put_text(f"Your congressional district will be split: {dem}% Democratic and {rep}% Republican.")
                put_text(f"The {winner} Party wins!")
                put_text("As a reminder, here was your congressional district's demographic profile:")
                put_table(table_data)

        elif choice == 'Just show me the entire country!':
            put_text("Here's a map of my predictions for the 2020 elections! Feel free to look around.")
            pred_2020 = predict_2020(data, rf_dem, rf_rep, scaler)
            fig = mapping(pred_2020)
            html = fig.to_html(include_plotlyjs="require", full_html=False)
            put_html(html)

        try_again = radio("Would you like to try another option?", options=['Yes', 'No'], required=True)
        if try_again == 'No':
            break 



if __name__ == "__main__":
    website()