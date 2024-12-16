import PySimpleGUI as sg
import pandas as pd
from functions import valid_100, median, input_row

def gui_cd():
    '''
    Creates a GUI for inputting a demographic profile of the user's choosing

    Returns:
    - user_cd (dict): contains the user's inputted demographic data 
    '''

    sg.theme('DarkAmber')
    
    # load data from csv file created by get_final_data() in final_data.py
    final_data = pd.read_csv('final_data.csv')

    # get medians for the data as default values
    medians = median(final_data)

    # demographic categories
    racial = ["White_non_Hispanic", "Hispanic_Latino", "Black", "American_Indian", "Asian"]
    education = ["Less_than_HS", "HS_grad", "Some_college", "Bachelors_degree", "Graduate_degree"]
    income = ['Income_under_25k', 'Income_25k_to_50k', 'Income_50k_to_75k','Income_above_75k']

    # initialize dictionary for demographic profile
    user_cd = {}
    
    # creat GUI
    layout = [
        [sg.Text("Input desired demographics.", font=20)],
        [sg.Text("(Prefilled with nationwide medians.)", font=10)],
        [sg.Text("Racial Makeup", font=18)],
        input_row("White (non Hispanic or Latino) %", "White_non_Hispanic", medians['White (non Hispanic or Latino) %']),
        input_row("Hispanic or Latino %", "Hispanic_Latino", medians['Hispanic or Latino %']),
        input_row("Black %", "Black", medians['Black %']),
        input_row("American Indian %", "American_Indian", medians['American Indian %']),
        input_row("Asian %", "Asian", medians['Asian %']),
        [sg.Text("Education Level", font=18)],
        input_row("Less than HS %", "Less_than_HS", medians['Less than HS %']),
        input_row("HS grad %", "HS_grad", medians['HS grad %']),
        input_row("Some college %", "Some_college", medians['Some college %']),
        input_row("Bachelor's degree %", "Bachelors_degree", medians["Bachelor's degree %"]),
        input_row("Graduate degree %", "Graduate_degree", medians["Graduate degree %"]),
        [sg.Text("Income:", font=18)],
        input_row("Income under 25k %", "Income_under_25k", medians["Income under 25k %"]),
        input_row("Income 25k to 50k %", "Income_25k_to_50k", medians["Income 25k to 50k %"]),
        input_row("Income 50k to 75k %", "Income_50k_to_75k", medians["Income 50k to 75k %"]),
        input_row("Income above 75k %", "Income_above_75k", medians["Income above 75k %"]),
        [sg.Text("Other:", font=18)],
        input_row('Voter Turnout %', 'Voter_Turnout', medians['Voter Turnout %']),
        input_row('Median Age', 'Median_Age', medians['Median Age']),
        input_row('Median income', 'Median_income', medians['Median income']),
        input_row("Below poverty line %", "Below_poverty_line", medians["Below poverty line %"]),
        [sg.Button("Submit")]
    ]

    window = sg.Window("Demographic Profile", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event == 'Submit':
            categories = [racial, education, income]

            # check if input data is valid
            invalid_categories = [category for category in categories if not valid_100(category, values)]
            voter_turnout = float(values['-IN-Voter_Turnout'])
            median_age = float(values['-IN-Median_Age'])
            median_income = float(values['-IN-Median_income'])
            below_poverty_line = float(values['-IN-Below_poverty_line'])
            
            # makes sure categories don't exceed 100%
            if invalid_categories or voter_turnout > 100 or below_poverty_line > 100:
                error_message = "Validation Error: "
                if invalid_categories:
                    error_message += "The sum of percentages exceeds 100% in one or more categories. "
                if voter_turnout > 100:
                    error_message += "Voter Turnout % exceeds 100. "
                if below_poverty_line > 100:
                    error_message += "Below poverty line % exceeds 100. "
                sg.popup_error(error_message)
            else:
                # store user input in dictionary
                sg.popup("Percentages are valid.")
                user_cd['Voter Turnout'] = voter_turnout
                user_cd['Median Age'] = median_age
                user_cd['Median income'] = median_income
                user_cd['Below poverty line'] = below_poverty_line
                for category in categories:
                    for row in category:
                        user_cd[row.replace("_", " ")] = float(values[f'-IN-{row}'])
                break
                
    window.close()
    return user_cd