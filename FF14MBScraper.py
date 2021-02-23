#!python3
#FF14MBscraper.py

"""
This scraper program will grab a database file from Universalis.app 
"""

import csv
import datetime
import json
import os
from datetime import date
from pathlib import Path
import requests
from bs4 import BeautifulSoup


# Get my datetime object for use with the file

def writeTextfile(textinput,name):
    # This is a tool function
    with open(f'{name}.txt',"w") as f:
aslkjasdkl;awsejdl;k asdj;lkasjd;fk ajsdfkl; ajdsf;l        f.write(textinput)
        f.close()


def serverchecker(server):
    serverlist=["Adamantoise","Cactuar","Faerie","Gilgamesh","Jenova",\
    "Midgardsormr","Sargatanas","Siren", "Behemoth","Excalibur",\
    "Exodus","Famfrit","Hyperion","Lamia","Leviathan","Ultros","Balmung",\
    "Brynhildr","Coeurl","Diabolos","Goblin","Malboro","Mateus","Zalera"]

    if server not in serverlist:
        print("Server not in serverlist, try again")
        return False
    else:
        return True

def createDatabaseCSV(name,headers,targetdirectory):
    # This is a tool function    
    os.chdir(Path.home() / Path(targetdirectory))
    with open(f'{name}.csv','w',newline='') as csvfile:
        writer=csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
    csvfile.close()

def makedirectory(primary, secondary=None):
    # Checks for the working directory and creates it and subdirectories
    working = Path.home() / Path(primary)
    print("Checking if the working directory exist")
    if working.exists():
        print("Directory Exist")
    else:
        print(f"Directory Does not exist, creating directory at {working}")
        Path.mkdir(working)

        if isinstance(secondary,list):
            listlength= len(secondary)
            for thingy in secondary:
                secondaryPath = working / Path(thingy)
                Path.mkdir(secondaryPath)
            print(f"{listlength} directories created")

def javascriptGrabby(target):
    # Target points to a .js target
    if target.endswith('.js'):
        print("Target is a javascript object")
        reqtarget = requests.get(target)
        if reqtarget.status_code==200:
            print("Converting")
            reqjson = json.loads(reqtarget.content)
            return reqjson
        else:
            return print("No go, Error: ", reqtarget.status_code())
    else:
        return print("Error, not a proper target")

def createBaseLineDatabase(universalisgrabby):
    """
    This will take in the javascript grabby and grab shit from universalis.
    Once grabbed, it'll create a new baseline dictionary that will be the \
    basis for what the data will be before its chopped down.  
    """
    FF14Dics={}

    DictionaryHeaders = ["Monk","Paladin", "Warrior","Bard",\
        "Dragoon","Black Mage", "White Mage","Summoner", "Paladin Shields",\
        "Carpenter","Blacksmith","Armsmith","Goldsmith","Leatherworker",\
        "Weaver","Alchemist","Culinarian","Miner","Botanist","Fisher","Bait",\
        "Head","Chest","Pants","Gloves","Boots","Belt","Necklace","Earrings",\
        "Bracelet","Ring","Consummables","Culinarian Materials"\
        ,"Food","Fish","Quarrying","Minerals","Wood","Botany","Leather"\
        ,"Monster Parts","Reagent", "Dye","Parts","Furnishing","Materia",\
        "Elemental Crystals", "Matter","Loot","Roof","Interior Furniture",\
        "Exterior Furniture","Lounge Furniture","Furniture","Tabletop1",\
        "Tabletop2", "Rugs","Ninja","Toys", "Minions","Dark Knight",\
        "Machinist", "Astrologian","Vehicles","Music","Seeds","Paintings",\
        "Samurai", "Redmage","Scholar","Gunbreaker", "Dancer"]


    # Lets fill the dic
    try:
        valuecounter = 0
        for v in universalisgrabby.values():
            FF14Dics[DictionaryHeaders[valuecounter]] = v
            valuecounter +=1
    except IndexError:
        print(DictionaryHeaders[valuecounter])
    return FF14Dics 
    

def bs4ff14MBItemscrape(itemID, itemName, server):
    # This will grab the thingy with beautiful soup and write to the database
    # easier to just merge the shit together and titties
    dataset = []
    
    completeUrl=f'https://www.ffxivmb.com/Items/{server}/{itemID}'
    ff14mbreq = requests.get(completeUrl)
    print(f"Attempting to Navigate to {completeUrl}, please wait..")
    if ff14mbreq.status_code !=200:
        return print(f'No go, unable to get to {completeUrl}')
    else:
        print("Success")
    
    # Time to make some soup
    print(f"Scraping data for {itemName}")
    ff14itemsoup = BeautifulSoup(ff14mbreq.content, 'html.parser')
    # Get the last updated date
    try:
        spanlist = ff14itemsoup.find_all("span")
        shitlerslist=str(spanlist[3].get_text())
        datasplit = shitlerslist.split()
        lastupdatedDate = datasplit[2]
        dataset.append(lastupdatedDate)
        # Grab the top block and associated data elements
        itemTable = ff14itemsoup.table.tbody.find_all("td")
        for item in itemTable:
            itemTable = str(item).replace("<td>", "")
            itemTable = itemTable.replace("</td>","")
            dataset.append(itemTable)
        print("Done")
        # With a dataset created, its time to open the database and merge it 
        
        return dataset
    except IndexError:
        print(f'No Data for item, {itemName}')
        dataset.append("No Data for this item")
        return dataset

# --------------------Script Start------------------------
today = date.today()
fileDate = today.strftime("%b-%d-%Y")
headers=["Item ID", "Item Name", "Item Level", "Class", "Last Updated",\
    "Quantity For Sale","Lowest Price", "Lowest HQ Price","Lowest NQ Price",\
    "Average Price","Last Sale Price","Last Week Sales Total Gil",\
    "Last Week Sales Number"]
workingdir = "FF14MBScraper"
universalistUrl = 'https://universalis.app/data/categories_en.js'
# Create the directory and the empty database
makedirectory(workingdir)
requestloop = False

while requestloop==False:
    server= str(input("Welcome, please specify the server you play on: \n"))
    server = server.title()
    if serverchecker(server) == True:
        requestloop = True

databasename = f"FF14-{server}-{fileDate}"
createDatabaseCSV(databasename,headers,workingdir)

#Lets grab the database file from universalis
universalisItem = createBaseLineDatabase(javascriptGrabby(universalistUrl))

# We need to clean the data since as it is..it a bunch of dictionaries with lists as values 
FF14ItemList = []
for listkey in universalisItem.keys():
    for valueset in universalisItem[listkey]:
        FF14ItemList.append(valueset)
# I can pop item 2 and 3 from each list.  2 is a picture, 3 is a mystery
for item in FF14ItemList:
    del item[2]
    del item[3]

#TODO : Iterate over the list rows to grab the Item ID and match that to the MB site
with open(f"{databasename}.csv","a", newline="") as f:
    itemwriter = csv.writer(f)
    for item in FF14ItemList:
        item.extend(bs4ff14MBItemscrape(item[0], item[1],str(server)))
        itemwriter.writerow(item)

print("Done")
