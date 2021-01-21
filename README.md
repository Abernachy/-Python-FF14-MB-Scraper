# -Python-FF14-MB-Scraper 1.0 Release
This is the FF14 Market Board scraper.

This program queries the user for his/her Final Fantasy 14 server.  It then grabs a database of every item in the game and scans ffxivMB and grabs the summary datatable for each item.
Once it grabs the data, it writes it to a spreadsheet csv file.

For the 1.0 release, that is all this program does.  It takes about 14 hours to write ALL of the data, so best bet is to run it before work and keep your laptop plugged in.

## Required Modules
You need the following modules or your attempts to run this program will end in poop:
 
1.  Requests
2.  Beautiful Soup 4



## Future Release Ideas
1.  A GUI
2.  A better way to organize the data and give the user the ability to specify what data he/she wants
3.  Save the item database and the server marketboard database as 2 offline elements so that after the initial long scan, it becomes an easily searchable offline database
4.  A counter to give you a time estimate as the marketboard database is being built.
5.  An installer that comes with the script that auto grabs the modules you need when you run the program
