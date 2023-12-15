import censusdata
import pandas as pd
from dicts import fips, abbrs, acs

def get_census():
    '''
    Retrieves census data, saves to census.csv

    Returns: 
    - all_data (df): retrieved census data
    '''

    # api key from us census 
    api_key = "504da964b02039cd3885095fa07d63870cdae572"

    # years for which we want data
    years = [2014, 2016, 2018, 2020]

    # get state abbreviations, FIPS codes, census variables from dicts
    state_abbrs = abbrs()
    state_abbrs = list(state_abbrs.values())
    state_fips = fips()
    state_fips = list(state_fips.values())
    variables = acs()
    acs_codes = list(variables.values())
    acs_variables = list(variables.keys())

    # initialize df to store census data
    all_data = pd.DataFrame()

    # retrieve census data through each year and state
    for year in years:
        for state in state_fips:
            data = censusdata.download(
                "acs5", 
                year, 
                censusdata.censusgeo([("state", state), ("congressional district", "*")]), 
                acs_codes,
                key = api_key
            )

            data["Year"] = year
            data["State FIPS"] = state
            data["State Abbr"] = state_abbrs[state_fips.index(state)]

            # add congressional district number column
            number = data.index.astype(str).str.split().str[2]
            if number[0] == "(at":
                data["District"] = 1
            else:
                data["District"] = number

            # combine all data
            all_data = pd.concat([all_data, data])

    all_data.reset_index(inplace=True, drop=True)

    inv_map = {v: k for k, v in variables.items()}
    all_data.rename(columns=inv_map, inplace=True)

    all_data.to_csv("census.csv", index=False)
    return all_data