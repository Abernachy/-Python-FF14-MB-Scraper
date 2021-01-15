#!python3
#FF14MBscraper.py

"""
Man, this programs idea just needs evolving and changing.  
So for now this program will scan the database from universalis,
then it will iterate over each item and match the ItemID to the marketboard
website and it will then append that data to itself and update the list.

Then the final list will be outputted to a CSV file for use with spreadsheets
"""

# imports
from pathlib import Path
import os
import json
from bs4 import BeautifulSoup
import datetime
import requests
import csv
from datetime import date




#TODO: Search for the working directory, if none exist, create it


home = Path.home()
basedir = Path("FF14MB Scraper")
database= Path("Database")
scrapes = Path("Scrapes")

workingdir = home / basedir
databasedir = workingdir / database
scrapesdir = workingdir / scrapes
directory = [workingdir,databasedir,scrapesdir]

server = "Cactuar"
MBUrl = 'https://www.ffxivmb.com/Items'

# Check if the directory exist

print("Checking if directory exists within your home directory, please wait..")
if workingdir.exists():
    print("Directory exist")
else:
    print(f"Directory does not exist, creating directory at {workingdir}")
    print(f"Creating database directory {databasedir}")
    # Make the directories
    for path in directory:
        path.mkdir()
        
# Get my datetime object for use with the file
today = date.today()
fileDate = today.strftime("%b-%d-%Y")

#TODO: Grab the database.js file from universalis and conver it to a list 

#Titties
#Lets grab the database file from universalis
universalisREQ = requests.get('https://universalis.app/data/categories_en.js')
ff14json = json.loads(universalisREQ.text)
UniversalisFF14ItemList = []
# We need to clean the data since as it is..it a bunch of dictionaries with lists as values 
# Theres also pictures I dont need, TO THE TRASH!!1


for listkey in ff14json.keys():
    for valueset in ff14json[listkey]:
        UniversalisFF14ItemList.append(valueset)

# I can pop item 2 and 3 from each list.  2 is a picture, 3 is a mystery
for item in UniversalisFF14ItemList:
    del item[2]
    del item[3]

#TODO : Iterate over the list rows to grab the Item ID and match that to the MB site

for row in UniversalisFF14ItemList[:100]:
    newData=[]
    itemID=row[0]
    itemName=row[1]
    itemLevel=row[2]
    Class=row[3]

    print("Starting data grab for: ", itemName)
    # Go to the MB URL site associated with the itemID
    completeUrl=(f"{MBUrl}/{server}/{itemID}")
    print(f"Navigating to {completeUrl}")
    idRequest = requests.get(completeUrl)
    if idRequest.status_code != 200:
        print(f"No go, unable to get to {completeUrl}")
        break
    
    #Make the soup
    print("scraping")
    ff14ItemSoup = BeautifulSoup(idRequest.content,'html.parser')

    # Last updated data
    spanlist=ff14ItemSoup.find_all("span")
    shitlerslist=str(spanlist[3].get_text())
    bimmy=shitlerslist.split()
    lastupdatedDate=bimmy[2]
    row.append(lastupdatedDate)

    #Grab the top block of data from the Market Board summary chart
    jimmy= ff14ItemSoup.table.tbody.find_all("td")

    spacestrip=[]

    for item in jimmy:
        jimmy = str(item).replace("<td>","")
        jimmy=jimmy.replace("</td>","")
        row.append(jimmy)

    print(f"Merging new {itemName} data with old")

    

    # We want to append the new items to the new data list

#TODO: Write the entire lists to a CSV file for use in a spreadsheet application

with open(f'{databasedir}/FF14ItemDatabase-{fileDate}.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Item ID", "Item Name", "Item Level",  "Class", "Last Updated",\
       "Lowest Price", "Lowest HQ Price","Last Sale Price", \
        "Last Week Sales Number", "Last Week Sales total Gil" ])
    writer.writerows(UniversalisFF14ItemList)


    print("Done")
