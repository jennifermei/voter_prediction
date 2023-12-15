import pandas as pd
from dicts import abbrs
from functions import get_percentages
from census import get_census
from votes import get_votes

def get_final_data():
    abbrs_data = abbrs()
    df_abbr = pd.DataFrame(list(abbrs_data.items()), columns=['State', 'State Abbr'])

    # df_votes = pd.read_csv('wiki_elections.csv')
    df_votes = get_votes()
    df_votes = pd.merge(df_votes, df_abbr[['State', 'State Abbr']], on='State', how='left')

    # df_census = pd.read_csv('census.csv')
    df_census = get_census()
    df_votes['District'] = df_votes['District'].astype(str)
    df_census['District'] = df_census['District'].astype(str)
    merge_columns = ['Year', 'State Abbr', 'District']
    df_number = pd.merge(df_votes, df_census, on=merge_columns, how='left')

    df_number['Voting Eligible Male'] = df_number["Male 18+ birthright"] + df_number["Male 18+ bloodright"] + df_number["Male 18+ naturalized"]
    df_number['Voting Eligible Female'] = df_number["Female 18+ birthright"] + df_number["Female 18+ bloodright"] + df_number["Female 18+ naturalized"]
    df_number['Voting Eligible Population'] = df_number['Voting Eligible Male'] + df_number['Voting Eligible Female']
    remove_columns1 = ['Male 18+ birthright','Male 18+ bloodright','Male 18+ naturalized','Male 18+ not citizen',
                    'Female 18+ birthright','Female 18+ bloodright','Female 18+ naturalized','Female 18+ not citizen']
    df_number.drop(columns=remove_columns1, inplace=True)

    df_number['Income under 25k'] = df_number['No income'] + df_number['Income under 10k'] + df_number['Income 10k to 15k'] + df_number['Income 15k to 25k']
    df_number['Income 25k to 50k'] = df_number['Income 25k to 35k'] + df_number['Income 35k to 50k']
    df_number['Income 50k to 75k'] = df_number['Income 50k to 65k'] + df_number['Income 65k to 75k']
    remove_columns2 = ['No income','Income under 10k','Income 10k to 15k','Income 15k to 25k','Income 25k to 35k',
                    'Income 35k to 50k','Income 50k to 65k','Income 65k to 75k']
    df_number.drop(columns=remove_columns2, inplace=True)

    first_columns = ['Year', 'State', 'State Abbr', 'District', 'Democratic Votes', 'Republican Votes', 'Total Votes',
                    'Voting Eligible Male', 'Voting Eligible Female', 'Voting Eligible Population', 'Total Population']
    df_data = df_number[first_columns + [col for col in df_number.columns if col not in first_columns]]

    keep_as_float = ['Democratic Percentage', 'Republican Percentage', 
                    'Voter Turnout', 'Year', 'State', 'State Abbr', 
                    'District', 'Median Age']
    change_to_int = [col for col in df_data.columns if col not in keep_as_float]
    df_data[change_to_int] = df_data[change_to_int].fillna(0).astype(int)
    df_data[change_to_int] = df_data[change_to_int].astype(int)

    remove_pa19 = (df_data['Year'] == 2016) & (df_data['State'] == 'Pennsylvania') & (df_data['District'] == '19')
    remove_ca44 = (df_data['Year'] == 2020) & (df_data['State'] == 'California') & (df_data['District'] == '44')
    df_data = df_data[~remove_pa19]
    df_data = df_data[~remove_ca44]

    df_data.to_csv('number_data.csv', index=False)

    #######################################

    df_final = df_data.copy()
    remove_columns_final = []

    get_percentages(df_final, 'Democratic %', 'Democratic Votes', 'Total Votes')
    get_percentages(df_final, 'Republican %', 'Republican Votes', 'Total Votes')
    get_percentages(df_final, 'Voter Turnout %', 'Total Votes', 'Voting Eligible Population')
    get_percentages(df_final, 'Male Population %', 'Male', 'Total Population')
    get_percentages(df_final, 'Female Population %', 'Female', 'Total Population')

    races = ['White','White (non Hispanic or Latino)','Hispanic or Latino','Black',
             'American Indian','Asian','Pacific','Multiracial']
    for race in races:
        new_name = race + ' %'
        get_percentages(df_final, new_name, race, 'Total Population')
    remove_columns_final.extend(races)

    educations = ['Less than HS','HS grad','Some college',"Bachelor's degree",'Graduate degree']
    for education in educations:
        new_name = education + ' %'
        get_percentages(df_final, new_name, education, 'Total Population')
    remove_columns_final.extend(educations)

    get_percentages(df_final, 'Below poverty line %','Income below poverty','Total income')
    incomes = ['Income under 25k','Income 25k to 50k','Income 50k to 75k','Income above 75k']
    for income in incomes:
        new_name = income + ' %'
        get_percentages(df_final, new_name, income, 'Total income')
    remove_columns_final.extend(incomes)

    last_to_remove = ['Male','Female','Total Population','Democratic Votes','Republican Votes','Total Votes','Not a citizen',
                      'Voting Eligible Male','Voting Eligible Female','Voting Eligible Population','Voting Eligible Male',
                      'Voting Eligible Female','Voting Eligible Population','Income below poverty','Total income']
    remove_columns_final.extend(last_to_remove)
    df_final.drop(columns=remove_columns_final, inplace=True)

    first_columns_final = ['Year', 'State', 'State Abbr', 'State FIPS','District', 'Democratic %', 'Republican %', 
                           'Voter Turnout %']
    df_final = df_final[first_columns_final + [col for col in df_final.columns if col not in first_columns_final]]

    df_final.to_csv('final_data.csv', index=False)
    return df_final