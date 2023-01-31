import requests
from typing import List, Dict
import itertools

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from bs4 import BeautifulSoup


url = 'https://www.globalfirepower.com/global-ranks-previous.php'
req = requests.get(url)
content = BeautifulSoup(req.content,'html.parser')
cards_content = content.find_all('div',{"class":"mainLists"})
years = content.find_all('span',{'class':"textLarger textBold"})


def get_years(content) -> List[str]:
    """
    Function to get years. Starting from 2005 to present.

    Parameters
    ----------
    content - html content of globalfirepower.com page

    Returns
    -------
    list_of_years: List[str] - list of years of all rankings
    """
    list_of_years = [year.string for year in content]
    return list_of_years


def get_countries(years: List, content) -> pd.DataFrame:
    """
    Parameters
    ----------
    content - html content of globalfirepower.com page - rankings over the years

    Returns
    -------
    df: pd.DataFrame - data frame with positions of top 25 countires accros all years
    """
    stats = {}
    for year, one_year in zip(years, content):
        # Get tags with countries names
        countries = one_year.find_all('div', {'class': 'countryName'})
        # Get just the cauntries from tags
        countries_list = [x.string for x in countries]
        stats[year] = countries_list
    df = pd.DataFrame(stats)
    return df


def get_countries_positions(data: pd.DataFrame, list_of_countries: List[str], list_of_years: List[str]):
    """
    Gets countries' postions in rankigs across the years.

    Parameters
    ----------
    data: pd.DataFrame - dataframe object mapping years to countries' positions
    list_of_countries: List[str] - list with countries to filter
    list_of_years: List[str] - years to get the rankings from

    Returns
    -------
    stats_over_years : Dict - dictionary with countries postions across the years.
    """
    data_sliced = data[list_of_years]
    stats_over_years = {}
    for year, country in zip(list_of_years, list_of_countries):
        positions = [np.where(data_sliced[one_year] == country)[0][0] + 1 for one_year in list_of_years]
        stats_over_years[country] = positions
    return stats_over_years


def create_plot_with_countries_comparison(object: Dict, list_of_years: List[str]) -> None:
    """
    Parameters
    ----------
    object: Dict -  dataframe object mapping years to countries' positions
    list_of_years: List[str] - list with years to compare

    Returns
    -------
    Plot comparing requested countires over years
    """
    for country in object:
        plt.plot(list_of_years, object[country], linestyle="-", marker="o", label=country)
    plt.xlabel('Years')
    plt.ylabel('Positions')
    plt.legend()
    plt.gca().invert_yaxis()
    plt.title('Positions comparison in GFP ranking over time')
    plt.grid()
    plt.show()

# Srcape data from globalfirepower.com
# Get list of years.
list_of_years = get_years(content=years)
# Get rankings across the years.
data = get_countries(years=list_of_years,content=cards_content)
# Clean column names.
data = data.rename(columns={'2009 (No Update)':'2009', '2008 (No Update)': '2008'})
# Save data to .csv file
data.to_csv('gfp_rankings.csv')
# Plot data at scatter plot.
list_of_countries = ['Poland','Germany','Japan','Pakistan']
list_of_years = ['2018','2019','2020','2021','2022','2023']
stats_over_years = get_countries_positions(data=data,
                                           list_of_countries=list_of_countries,
                                           list_of_years=list_of_years)
create_plot_with_countries_comparison(object=stats_over_years,
                                      list_of_years=list_of_years)
