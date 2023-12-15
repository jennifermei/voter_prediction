import requests
from bs4 import BeautifulSoup
import pandas as pd
from dicts import abbrs
from functions import replace_if_not_number, get_url

def get_votes():
    all_data = pd.DataFrame()

    years = [2014, 2016, 2018, 2020]

    state_abbrs = abbrs()
    state_names = list(state_abbrs)
    state_abbrs = list(state_abbrs.values())

    for year in years: 
        for state in state_names:

            url = get_url(state, year)
            
            response = requests.get(url)
            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')

            table = soup.find('table', {'class': 'wikitable plainrowheaders sortable'})

            districts = []
            democratic_votes = []
            republican_votes = []
            total_votes = []

            if table:
                for row in table.find_all('tr')[1:]:
                    columns = row.find_all('td')
                    if columns:
                        district_name = columns[0].text
                        district_name = district_name[len("District "):]

                        top_row = table.find_all('tr')[0].text
                        party = top_row.split()[1]
                        if party == "Republican":
                            rep_votes = replace_if_not_number(columns[1].text)
                            rep_votes = int(rep_votes.replace(',', ''))
                            dem_votes = replace_if_not_number(columns[3].text)
                            dem_votes = int(dem_votes.replace(',', ''))
                        if party == "Democratic":
                            rep_votes = replace_if_not_number(columns[3].text)
                            rep_votes = int(rep_votes.replace(',', ''))
                            dem_votes = replace_if_not_number(columns[1].text)
                            dem_votes = int(dem_votes.replace(',', ''))   

                        if columns[-2].text == "100%" or columns[-2].text == "100.0%" or columns[-2].text == "100.00%":
                            tot_votes = replace_if_not_number(columns[-3].text)
                        else:
                            tot_votes = tot_votes = replace_if_not_number(columns[-2].text)
                        tot_votes = int(tot_votes.replace(',', ''))

                        districts.append(district_name)
                        republican_votes.append(rep_votes)
                        democratic_votes.append(dem_votes)
                        total_votes.append(tot_votes)

                if len(districts) > 1:
                    districts.pop()
                    republican_votes.pop()
                    democratic_votes.pop()
                    total_votes.pop()

            elif "elections" in url:
                tables = soup.find_all("table", {"class": "wikitable plainrowheaders"})

                district_name = 1

                for table_cd in tables:
                    caption = table_cd.find("caption")

                    if caption and "congressional district" in caption.get_text().lower():
                        table = table_cd
                    else:
                        continue

                    if table:
                        dem_votes = 0
                        rep_votes = 0

                        for row in table.find_all("tr"):
                            cells = row.find_all(["th", "td"])
                            if len(cells) >= 3:
                                party = cells[1].text.strip()

                                if "Republican" in party:
                                    rep_votes_append = replace_if_not_number(cells[3].text.strip())
                                    rep_votes_append = int(rep_votes_append.replace(",", ""))
                                    rep_votes += rep_votes_append
                                elif "Democratic" in party:
                                    dem_votes_append = replace_if_not_number(cells[3].text.strip())
                                    dem_votes_append = int(dem_votes_append.replace(",", ""))
                                    dem_votes += dem_votes_append
                                elif any(char.isdigit() for char in party):
                                    tot_votes = party
                                    tot_votes = int(tot_votes.replace("'", "").replace(",", ""))

                        districts.append(district_name)
                        republican_votes.append(rep_votes)
                        democratic_votes.append(dem_votes)
                        total_votes.append(tot_votes)
                        district_name += 1

            # for if it is a single district state
            else:
                table_single = None
                tables_single = soup.find_all("table", {"class": "wikitable plainrowheaders"})

                for table_cd in tables_single:
                    caption = table_cd.find("caption")
                    if caption and "at-large" in caption.get_text().lower():
                        table_single = table_cd
                        break

                if table_single:
                    district_name = 1
                    dem_votes = 0
                    rep_votes = 0

                    for row in table_single.find_all("tr"):
                        cells = row.find_all(["th", "td"])
                        if len(cells) >= 3:
                            party = cells[1].text.strip()

                            if "Republican" in party:
                                rep_votes_append = replace_if_not_number(cells[3].text.strip())
                                rep_votes_append = int(rep_votes_append.replace(",", ""))
                                rep_votes += rep_votes_append
                            elif "Democratic" in party:
                                dem_votes_append = replace_if_not_number(cells[3].text.strip())
                                dem_votes_append = int(dem_votes_append.replace(",", ""))
                                dem_votes += dem_votes_append
                            elif any(char.isdigit() for char in party):
                                tot_votes = party
                                tot_votes = int(tot_votes.replace("'", "").replace(",", ""))

                    districts.append(district_name)
                    republican_votes.append(rep_votes)
                    democratic_votes.append(dem_votes)
                    total_votes.append(tot_votes)

            if year == 2016 and state == "Illinois":
                republican_votes[9] = "135535"
                total_votes[9] = "285996"

            data = {
                'District': districts,
                'Democratic Votes': democratic_votes,
                'Republican Votes': republican_votes,
                'Total Votes': total_votes,
                'Year': [year] * len(districts),
                'State': state
            }

            df = pd.DataFrame(data)

            all_data = pd.concat([all_data, df], ignore_index=True)

    all_data['Democratic Votes'] = all_data['Democratic Votes'].astype(int)
    all_data['Republican Votes'] = all_data['Republican Votes'].astype(int)
    all_data['Total Votes'] = all_data['Total Votes'].astype(int)
    all_data['Year'] = all_data['Year'].astype(int)
    
    all_data.to_csv("votes.csv", index=False)
    return all_data