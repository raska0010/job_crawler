# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as BS
import re
from datetime import date
import os
import webbrowser
import web_tools as wb

   
   
# Add job advertisment to html_file
def write_file():
    with open(f'results/jobs_{city}.html', 'a') as f:
        url_name = job.a.text.strip()  # Use add text to create URL name.
        link = job.a['href']  # Link to the ad.
        hyperlink_format = '<a href="{link}" target="_blank">{text}</a>'
        hyperlink = hyperlink_format.format(link=link, text=url_name)
        f.write(f'{hyperlink}<br><br>')


# Ask user to select city
def get_city():

    user_input = input('>>> Do you want to look for new jobs in Köln or in Bonn? Type "1" for Köln. Type "2" for Bonn.\n')

    if user_input == '1' or user_input == '2':
        city_ = 'Köln' if user_input == '1' else 'Bonn'
        os.system('clear')
        return city_
    else:
        os.system('clear') 
        print('''>>> Wrong input!\n''')
        return get_city()


# Files with search results will be stored in the folder results. Check whether the folder results exists. 
def check_path_results():
    if os.path.isdir('results'):
        pass
    else:
        print('>>> The folder "results" does not exist')
        user_input = input('>>> Do you want to create a folder "results"? Type "1" for yes. Type "2" to abort the search.\n')
        if user_input =='1':
            os.makedirs('results')
        elif user_input == '2':
            exit()
        else:
            os.system('clear') 
            print('''>>> Wrong input!\n''')
            check_path_results()


# Ask user whether to open search results in a webbrowser or to finish the programme
def open_results(city):
    user_input = input('>>> Do you want to open the search results in your web browser? Type "1" for yes. Type "2" to finish.\n')
    if user_input == "1":
        webbrowser.open('file://' + os.getcwd() + f'/results/jobs_{city}.html')
        exit()
    elif user_input == "2":
        exit()
    else:
        os.system('clear') 
        print('''>>> Wrong input!\n''')
        open_results(city)


check_path_results()

city = get_city()

print(f'>>> Searching for new jobs in {city}\n')


# KULTtweet
payload = {
    'data' : city,
    'Suchen' : 'Jobs+finden'
}
content = wb.open_url('https://www.kultweet.de/jobs.php', 'post', payload)
if content:
    jobs = content.find_all('li', class_=re.compile(r'row'))  # Look for 'li' tags. They contain the job ad text and link.
    for job in jobs:
        write_file()


exit(0)

# Jobforum Kultur
payload = {'s': city}
content = open_html('https://jobforum-kultur.eu/', 'get', payload)
jobs = content.find_all(r'article')  # Look for 'article' tags. They contain the job ad text and link.
for job in jobs:
    write_file()


# GoodJobs / link= set filter to 100 results
payload = {
    'search': None,
    'search_type': None,
    'places': city,
    'distance': '10',
    'places_type': None,
    'countrycode': None,
    'state': None,
    'latlng': None,
    'num': '100'  # Set to 100 results per page.
}
content = open_html('https://goodjobs.eu/jobs', 'get', payload)
jobs = content.find_all('a', class_='jobcard')  # Look for 'a' tags with 'class='jobcard'' attribute. They contain the job ad text and link.

for job in jobs:
    job = job.parent  # Return parent tag of 'a' tag. Necessary to make write_file() work, because it expects a format where a is not the parent tag.

    tags = job.a.find_all('p', class_=re.compile('label-text'))  # The ad text is spread across various attributes. Appends all text fragments to the 'h3' tag.
    for tag in tags:
        job.h3.append(', ' + tag.text.strip())  # The ad text is spread across various attributes. Appends all text fragments to the 'h3' tag.
        tag.decompose()

    tags = job.find_all('span')  # Delete 'span' attributes that contain unwanted text.
    for tag in tags:
        tag.decompose()
    write_file()


# epojobs / Infos zum Arbeitgeber fehlen
payload = {
	"filter-search": "Köln",
	"limit": "30",
	"filter_order": "",
	"filter_order_Dir": "",
	"limitstart": "",
	"task": ""
}
content = open_html('https://www.epojobs.de/', 'post', payload)
jobs = content.find_all(class_=re.compile('cat-list-row'))
for job in jobs:
    full_text = job.text
    replace_tag = job.a
    replace_tag.string = full_text
    link = job.a['href']
    job.a['href'] = 'https://epojobs.de'+link  
    write_file()


# Wila Arbeitsmarkt
for x in range(1,11):  # How to not hard code '11'?
    content = open_html('https://www.wila-arbeitsmarkt.de/stellenanzeigen/?sortby=angebote_plz&sort=ASC&page='+str(x), 'get')
    jobs = content.find_all('td', string = re.compile('^50|^510|^511'))
    for job in jobs:
        job = job.find_parent('tr')
        full_text = job.text
        replace_tag = job.a
        replace_tag.string = full_text
        link = job.a['href']
        job.a['href'] = 'https://www.wila-arbeitsmarkt.de' + link
        write_file()


# Stadt Koeln
content = open_html('https://www.stadt-koeln.de/politik-und-verwaltung/ausbildung-karriere-bei-der-stadt/stellenangebote/wissenschaft-kultur', 'get')
jobs = content.find_all('ul', id=re.compile('ziel'))
for job in jobs:
    jobs = job.find_all('li')
    for job in jobs:
        link = job.a['href']
        job.a['href'] = 'https://www.stadt-koeln.de/'+link  
        write_file()

 
print('>>> New file created...\n')
        
open_results(city)