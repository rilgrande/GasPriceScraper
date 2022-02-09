#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Created By: Roger IL Grande
# ---------------------------------------------------------------------------
"""This script will scrape New Jersey refinery gasoline price data from the U.S. Energy Information Administration"""

# Using the BeautifulSoup scraper
from bs4 import BeautifulSoup
import pandas as pd
import requests
import matplotlib.pyplot as plt

url = "https://www.eia.gov/dnav/pet/hist/LeafHandler.ashx?n=PET&s=EMA_EPM0_PWG_SNJ_DPG&f=M"

result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")
#print(soup.prettify())

year = 0
start_position = 0
end_position = 0


# Prompt user input for year and convert this value into an index
def get_year_index():
    global start_position
    global end_position
    global year
    print("Which year's data would you like to see (1983-2021)?")
    year = int(input("Year: "))
    year = year - 1983
    while year > 38 or year < 0:
        year = int(input("Please enter a year in the range from 1983 to 2021: ")) - 1983
        if year not in range(0, 38):
            print("Please try again")
            continue
        else:
            # Year response is in range of price data
            # Ready to exit the loop
            break
    start_position = int(year * 12)
    end_position = int(start_position + 12)
    return start_position, end_position, year


get_year_index()
all_prices = []
year_prices = []
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


# Import all price data into prices list
for i in soup.find_all("table", class_="FloatTitle"):
    for j in i.find_all("tr"):
            for k in j.find_all("td",class_="B3"):
                all_prices.append(k.text.strip())


# Populate the list with prices for each month in the desired year
def get_year_prices(start_position, end_position):
    global year_prices
    year_prices = all_prices[start_position:end_position]
    return year_prices


get_year_prices(start_position, end_position)


# Create a data frame of the year's prices with indexes corresponding to each month
df_year_prices = pd.DataFrame(list(zip(year_prices)), columns=[str(year + 1983) + " Prices"])
df_year_prices = df_year_prices.set_axis(months)
print(df_year_prices)


# Prepare the data to be plotted, and then create a line plot
price_floats = []

for element in year_prices:
    price_floats.append(float(element))


plt.title(str(year + 1983) + ' NJ Refinery Gasoline Prices')
plt.xlabel('Month')
plt.ylabel('Price ($)')
if year_prices[-1] > year_prices[0]:  # Compare January and December prices, change line color accordingly
    plt.plot(months, price_floats, color="green")
else:
    plt.plot(months, price_floats, color="red")
plt.grid()
plt.show()


