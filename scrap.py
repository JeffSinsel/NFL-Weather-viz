import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

prefix = 'http://www.nflweather.com'
webpage_response = requests.get('http://www.nflweather.com/en/archive/')

webpage = webpage_response.content
soup = BeautifulSoup(webpage, "html.parser")

#pull links from the website's html
week_links = soup.find_all("a", href=True)
links = []

for a in week_links:
    links.append(prefix + a['href'])

#clean the links
unclean_links = links[72:-18]
unclean_links = [x for x in unclean_links if "pre-season" not in x]
unclean_links = [x for x, x in enumerate(unclean_links) if re.search("W|week-", x)]
clean_links = unclean_links

#creates list of week names to combine with data later
week_names = []
for all in reversed(range(10,20)):
    for i in range(17):
        week_names.append('20'+ str(all) + '|Week ' + str(i+1))
for i in range (17):
    week_names.append('2009|Week ' + str(i+1))

#gets data from website
weather_data = {}
stats_list = []
for link in clean_links:
    print(link)
    webpage = requests.get(link)
    week = BeautifulSoup(webpage.content, "html.parser")
    stats = week.find('tbody')
    stats_text = stats.get_text("|")
    stats_list.append(stats_text)

#combines data from links and week names in dictionary and saves to unclean.csv
combined = dict(zip(week_names,stats_list))
total_df = pd.DataFrame.from_dict(combined,orient = "index")
total_df.to_csv('unclean.csv')