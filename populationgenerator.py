# Author: Tyler Rayls
# Date: 2/14/21
# References:
#   Using TKinter: https://coderslegacy.com/python/python-gui/
#   Setting up the API call: https://www.youtube.com/watch?v=l47HptzM7ao
#   Reading and writing .csv files: https://realpython.com/python-csv/

from tkinter import *
from tkinter import ttk
import requests
import sys
import csv

state_code = {"AK": "02", "AL": "01", "AR": "05", "AZ": "04", "CA": "06", "CO": "08", "CT": "09", "DC": "11", "DE": "10",
              "FL": "12", "GA": "13", "HI": "15", "IA": "19", "ID": "16", "IL": "17", "IN": "18", "KS": "20", "KY": "21",
              "LA": "22", "MA": "25", "MD": "24", "ME": "23", "MI": "26", "MN": "27", "MO": "29", "MS": "28", "MT": "30",
              "NC": "37", "ND": "38", "NE": "31", "NH": "33", "NJ": "34", "NM": "35", "NV": "32", "NY": "36", "OH": "39",
              "OK": "40", "OR": "41", "PA": "42", "RI": "44", "SC": "45", "SD": "46", "TN": "47", "TX": "48", "UT": "49",
              "VA": "51", "VT": "50", "WA": "53", "WI": "55", "WV": "54", "WY": "56"}

wiki_states = {"AK": "Alaska", "AL": "Alabama", "AR": "Arkansas", "AZ": "Arizona", "CA": "California", "CO": "Colorado",
               "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "IA": "Iowa",
               "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
               "MA": "Massachusetts", "MD": "Maryland", "ME": "Maine", "MI": "Michigan", "MN": "Minnesota", "MO": "Missouri",
               "MS": "Mississippi", "MT": "Montana", "NC": "North_Carolina", "ND": "North_Dakota", "NE": "Nebraska",
               "NH": "New_Hampshire", "NJ": "New_Jersey", "NM": "New_Mexico", "NV": "Nevada", "NY": "New_York_(state)",
               "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode_Island", "SC": "South_Carolina",
               "SD": "South_Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VA": "Virginia", "VT": "Vermont",
               "WA": "Washingotn", "WI": "Wisconsin", "WV": "West_Virginia", "WY": "Wyoming"}

def get_data_for_gui():
    '''
    Executes when the button is clicked to get data for the selected state and year and display it on the GUI.

    '''
    state = state_drop_down.get()
    year = years_drop_down.get()
    population_results = get_population(state, year)
    info_results = get_info(state, year)
    display_results(population_results, info_results, state, year)

def get_info(state, year):
    '''
    Makes a request to the content generator microservice.
    :param state: state to request data on
    :param year: year to look for additional info on
    :return: short paragraph with additional information related to the state
    '''
    base_url = "http://127.0.0.1:5001/get?"
    predicates = {}
    predicates["pri"] = wiki_states[state]
    predicates["sec"] = year
    r = requests.get(base_url, params=predicates)
    return r.json()


def get_population(state, year):
    '''
    Makes a request to the API for the population size of a state in a given year.
    :param state: state to request population size of
    :param year: year to request the data
    :param update_GUI: boolean used to determine if the GUI is being used and results should be displayed there
    :return: a json of the response from the request
    '''
    # Creates the base url for the API request
    host = "https://api.census.gov/data"
    dataset = "acs/acs1/spp"
    base_url = "/".join([host, year, dataset])

    # Sets the query parameters for the API
    predicates = {}
    get_vars = ["NAME", "S0201_001E"]
    predicates["get"] = ",".join(get_vars)
    predicates["for"] = ":".join(["state", state_code[state]])
    predicates["key"] = "93647a1c34b435616eb32f2172d87eed03eebfa7"

    # Requests the data for the given state and year returns the json of the response
    r = requests.get(base_url, params=predicates)
    return r.json()

def display_results(population_results, economy_results, state, year):
    '''
    Updates the labels on the GUI with the results from the API call.
    :param results: json response from the API call
    :param state: state that was requested
    :param year: year for the request
    '''
    state_text = " ".join(["State:", state])
    year_text = " ".join(["Year:", year])
    pop_text = " ".join(["Population:", population_results[1][1]])
    econ_text = economy_results["wiki"]
    state_label.configure(text=state_text)
    year_label.configure(text=year_text)
    population_label.configure(text=pop_text)
    economy_label.configure(text=econ_text)

def parse_input_csv():
    '''
    Parses the input.csv file for the state and year if it was passed as an argument when running the program.
    '''
    # Opens the input.csv file that was passed into the user
    with open('input.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            input_data = (row["input_state"], row["input_year"])
            return input_data

def write_output_csv(results, state, year):
    '''
    Writes the results to a file named output.csv in the same directory the program is stored in.
    :param results: json response from the API call
    :param state: state that was requested
    :param year: year for the request
    '''
    # Opens/creates output.csv and writes the header and data row to the file
    with open('output.csv', mode="w") as output_file:
        output_writer = csv.writer(output_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(["input_year", "input_state", "output_population_size"])
        output_writer.writerow([year, state, results[1][1]])

# Checks if the input.csv file was included as an argument when loading the program
if len(sys.argv) > 1 and sys.argv[1] == 'input.csv':
    # Parses input.csv, requests the data from the census API, and writes the response to output.csv
    state, year = parse_input_csv()
    results = get_population(state, year)
    write_output_csv(results, state, year)
else:
    # Creates the GUI, gives it a title, and defines the start up size
    window = Tk()
    window.title("Population Generator")
    window.geometry("400x400")
    frame = Frame(window)
    frame.pack()

    # Adds a drop down list (combobox) to the window for the user to select a state from
    states = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY",
              "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY",
              "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UM", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]
    state_drop_down = ttk.Combobox(frame, values=states)
    state_drop_down.set("Pick a State")
    state_drop_down.pack(padx=5, pady=5)

    # Adds a drop down list (combobox) to the window for the user to select a census year from
    years = ["2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012",
             "2011", "2010", "2009", "2008"]
    years_drop_down = ttk.Combobox(frame, values=years)
    years_drop_down.set("Pick a Year")
    years_drop_down.pack(padx=5, pady=5)

    # Adds a button to get the population size for the State and Year selected
    get_data_button = ttk.Button(frame, text="Submit", command=get_data_for_gui)
    get_data_button.pack(padx=5, pady=5)

    # Adds a labels for the state, year, and population results to be displayed
    state_label = Label(frame, text="State: ")
    state_label.pack()
    year_label = Label(frame, text="Year: ")
    year_label.pack()
    population_label = Label(frame, text="Population: ")
    population_label.pack()
    economy_label = Label(frame, text="", wraplength=350)
    economy_label.pack()

    # Starts the GUI application
    window.mainloop()