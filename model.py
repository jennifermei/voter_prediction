import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def create_models(data):
    train_columns = ['Voter Turnout %', 'Median Age', 'Median income', 'Below poverty line %', 
                    'White (non Hispanic or Latino) %', 'Hispanic or Latino %', 'Black %', 'American Indian %', 'Asian %', 
                    'Less than HS %', 'HS grad %', 'Some college %', "Bachelor's degree %", "Graduate degree %",
                    'Income under 25k %', 'Income 25k to 50k %', 'Income 50k to 75k %','Income above 75k %']

    # training data 2014, 2016, 2018 ;; testing data 2020
    train_data = data[data['Year'].isin([2014, 2016, 2018])]

    # training features
    X_train = train_data[train_columns].values

    # target variables
    y_train_dem = train_data['Democratic %'].values
    y_train_rep = train_data['Republican %'].values

    # normalize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)

    # 80% training, 20% validation for both dem and rep
    X_train_dem, X_val_dem, y_train_dem, y_val_dem = train_test_split(
        X_train, y_train_dem, test_size=0.2, random_state=42
    )

    X_train_rep, X_val_rep, y_train_rep, y_val_rep = train_test_split(
        X_train, y_train_rep, test_size=0.2, random_state=42
    )

    # define and train random forests
    rf_dem = RandomForestRegressor(random_state=42)
    rf_dem.fit(X_train_dem, y_train_dem)

    rf_rep = RandomForestRegressor(random_state=42)
    rf_rep.fit(X_train_rep, y_train_rep)

    return rf_dem, rf_rep, scaler

def predict_2020(data, rf_dem, rf_rep, scaler):    
    train_columns = ['Voter Turnout %', 'Median Age', 'Median income', 'Below poverty line %', 
                    'White (non Hispanic or Latino) %', 'Hispanic or Latino %', 'Black %', 'American Indian %', 'Asian %', 
                    'Less than HS %', 'HS grad %', 'Some college %', "Bachelor's degree %", "Graduate degree %",
                    'Income under 25k %', 'Income 25k to 50k %', 'Income 50k to 75k %','Income above 75k %']

    test_data = data[data['Year'] == 2020].copy()

    # testing features, normalize
    X_test = test_data[train_columns].values
    X_test = scaler.transform(X_test)

    # use trained models to predict on 2020 test data
    predict_dem = rf_dem.predict(X_test)
    predict_dem = np.clip(predict_dem, 0, 100)
    predict_rep = rf_rep.predict(X_test)
    predict_rep = np.clip(predict_rep, 0, 100)

    # make sure combined percentages don't go above 100
    total = predict_dem + predict_rep
    scaling_factor = 100 / np.maximum(total, 1)  
    predict_dem *= scaling_factor
    predict_rep *= scaling_factor

    predict_dem = np.round(predict_dem, 2)
    predict_rep = np.round(predict_rep, 2)

    # add predictions, winners to new df
    test_data.loc[:, 'Predicted Democratic %'] = predict_dem
    test_data.loc[:, 'Predicted Republican %'] = predict_rep
    test_data.loc[:, 'Winner'] = np.where(test_data['Democratic %'] > test_data['Republican %'], 'Democratic', 'Republican')
    test_data.loc[:, 'Predicted Winner'] = np.where(test_data['Predicted Democratic %'] > test_data['Predicted Republican %'],
                                                    'Democratic', 'Republican')

    result_df = test_data[['Year', 'State', 'State Abbr', 'State FIPS', 'District', 'Democratic %', 'Republican %',
                            'Predicted Democratic %', 'Predicted Republican %', 'Winner', 'Predicted Winner']]
    result_df.to_csv('predictions_2020.csv', index=False)
    return result_df

def predict_user_cd(user_cd, rf_dem, rf_rep, scaler):
    user_cd = np.array(user_cd).reshape(1, -1)
    user_cd = scaler.transform(user_cd)

    predict_dem = rf_dem.predict(user_cd)
    predict_dem = np.clip(predict_dem, 0, 100)
    predict_rep = rf_rep.predict(user_cd)
    predict_rep = np.clip(predict_rep, 0, 100)

    # make sure combined percentages don't go above 100
    total = predict_dem + predict_rep
    scaling_factor = 100 / np.maximum(total, 1)  
    predict_dem *= scaling_factor
    predict_rep *= scaling_factor

    predict_dem = np.round(predict_dem, 2)
    predict_rep = np.round(predict_rep, 2)

    if predict_dem > predict_rep:
        winner = "Democratic"
    else:
        winner = "Republican"

    return predict_dem[0], predict_rep[0], winner