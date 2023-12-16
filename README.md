# Predicting 2020 Congressional House Elections 

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Data and Resources](#dataandresources)
- [Process and Code](#processandcode)

## Overview
This project uses election data and community demographic data from 2014, 2016, and 2018 to predict how different congressional districts will vote in 2020. Determining the factors that contribute to how US citizens vote in elections is important for political scientists and political campaigns. This project uses machine learning to use the relationship between a congressional district’s demographic profile and how that district votes in U.S. House of Representatives elections. It focuses on racial makeup, education levels, and income, as well as some other factors.

I used the U.S. Census Bureau’s API for the American Community Survey to gather the community demographic data, and I scraped Wikipedia for elections results and vote counts. Using these, I created and trained Random Forest models on 2014, 2016, and 2018 data and used those models to predict the percentage of Democratic and Republican votes for each congressional district in 2020. Finally, I created a website to allow users to view the predictions, choosing either an existing congressional district, making their own with different demographic profiles, or just viewing the entire United States!

The technical components I used are: web scraping, using an API call to handle messy data, complex data visualization using plotly, building a GUI, and building a dynamic website.


## Setup
All you need to run is `main.py`!

If you clone the repository, you can replicate my results by running `main.py`. You do not need to run anything else, as all the functions are packaged in such a way that you only need to run the one program. It may take a little bit for the website to show up as `main.py` also has to scrape data, use API calls, create and train models, and make predictions in addition to creating a website. It takes me about five minutes for the website to be created, and it may take shorter or longer depending on your computer. When all the data has been processed and the models have been created, a tab will automatically open in your browser and you will be able to use the website. The `csv` files will be overwritten when you run the program (with identical/very similar data).

Python Version: 3.10.13
See `requirements.txt` for what packages/libraries you need to have installed.

```bash
# example installation 
git clone https://github.com/jennifermei/voter_prediction.git
cd voter_prediction     # or your file path
pip install -r requirements.txt
python main.py
```

## Data and Resources
Data for the project are drawn from publicly available sources, including:
- [American Community Survey](https://www.census.gov/data/developers/data-sets/acs-5year.2014.html#list-tab-1036221584): demographic data for each US house district in 2014, 2016, 2018, and 2020
- [Wikipedia](https://en.wikipedia.org/wiki/2014_United_States_House_of_Representatives_elections_in_Alabama): election data for each US house district in 2014, 2016, 2018, and 2020 (link is for 2014 Alabama)
- [GeoJSON Data for the United States](https://eric.clst.org/tech/usgeojson/): GeoJSON boundary files for US congressional districts. Thank you so much Eric!
- [United States Census Bureau](https://www.census.gov/programs-surveys/acs/data/data-via-api.html): Census Bureau's API for accessing ACS data. Thank you to the Census Bureau!

## Process and Code
The data were ultimately combined into a single data file for a row for each congressional district in each year, and columns representing different election results and demographic features. To predict election results in 2020, I created a random forest model (which did not perform too well, but that's okay!). Generally, I focused on racial makeup, education level, income, voter turnout, median age, election predictions, and geographic data. For more details on the demographic data, refer to the dictionary of ACS codes in `dicts.py`, which has all the factors of note listed. 

Code for the project is organized as such:
- [functions.py](https://github.com/jennifermei/voter_prediction/blob/main/functions.py) and [dicts.py](https://github.com/jennifermei/voter_prediction/blob/main/dicts.py) for ease of access 
- [votes.py](https://github.com/jennifermei/voter_prediction/blob/main/votes.py) scrapes Wikipedia for election data from each congressional district in the 2014, 2016, 2018, and 2020 election cycles, combining it all into a single dataframe
- [census.py](https://github.com/jennifermei/voter_prediction/blob/main/census.py) uses the CensusData api to gather data from the ACS for each congressional district, combining it all into a single dataframe
- [final_data.py](https://github.com/jennifermei/voter_prediction/blob/main/final_data.py) combines the dataframes from the above two and processes it for modeling use
- [model.py](https://github.com/jennifermei/voter_prediction/blob/main/model.py) creates and trains RF models to predict Democratic and Republican percentages
- [mapping.py](https://github.com/jennifermei/voter_prediction/blob/main/mapping.py) generates maps using Plotly Express based on election predictions and geographic data
- [website.py](https://github.com/jennifermei/voter_prediction/blob/main/website.py) creates an interactive website for the user to explore election results and the impact of demographic factors, with the help of [cd_gui.py](https://github.com/jennifermei/voter_prediction/blob/main/cd_gui.py) which creates a GUI
- [main.py](https://github.com/jennifermei/voter_prediction/blob/main/main.py) is the only program you need to run!
