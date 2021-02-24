This population generator is a microservice. The population generator takes a state and name and makes a request to a census API to get the population size. 

In addition to this, the population generator works with another microservice to get additional information on that state in that year from its Wikipedia page. Sometimes the Wikipedia page will not find a paragraph that matches the primary (state) and secondary (year) keywords that are being used to perform the search.

The content generator microservice that this application communicates with can be found here:
https://github.com/mxjeffers/contentcreator

Package Requirements:
tkinter
requests
sys
csv
os
Flask

To run the population generator from the command line with an input.csv file:
python populationgenerator.py input.csv

To run the population generator as a GUI:
python populationgenerator.py

To use the population generator as a microservice:
python server.py

NOTE: The microservice currently has a bug that prompts the GUI to open. Simply close the GUI and the server will then
run and you will be able to make requests to port 5003 on the localhost.

