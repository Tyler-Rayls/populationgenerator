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
               "MA": "Massachusetts", "MD": "Maryland", "ME": "Maine", "MI": "Michigan", "MN": "Minnesota",
               "MO": "Missouri", "MS": "Mississippi", "MT": "Montana", "NC": "North_Carolina", "ND": "North_Dakota",
               "NE": "Nebraska", "NH": "New_Hampshire", "NJ": "New_Jersey", "NM": "New_Mexico", "NV": "Nevada",
               "NY": "New_York_(state)", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
               "RI": "Rhode_Island", "SC": "South_Carolina", "SD": "South_Dakota", "TN": "Tennessee", "TX": "Texas",
               "UT": "Utah", "VA": "Virginia", "VT": "Vermont", "WA": "Washington", "WI": "Wisconsin",
               "WV": "West_Virginia", "WY": "Wyoming"}

states = ["AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA", "ID", "IL", "IN", "KS", "KY",
          "LA", "MA", "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY",
          "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT", "WA", "WI", "WV", "WY"]

years = ["2019", "2018", "2017", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008"]

class GUI:
    '''Creates a graphical user interface (GUI) for the user to use the Population Generator microservice.'''
    def __init__(self):
        '''Initializes the window, frames, and widgets that belong to the GUI and launches it.'''
        self.window = self.create_window()
        self.input_frame = self.create_label_frame("Input")
        self.population_frame = self.create_label_frame("Population")
        self.info_frame = self.create_label_frame("Information")
        self.state_drop_down = self.create_drop_down(states, "Pick a State")
        self.years_drop_down = self.create_drop_down(years, "Pick a Year")
        self.get_data_button = self.create_button()
        self.state_label = self.create_label(self.population_frame, "State: ")
        self.year_label = self.create_label(self.population_frame, "Year: ")
        self.population_label = self.create_label(self.population_frame, "Population: ")
        self.info_label = self.create_label(self.info_frame, "", 350)
        self.window.mainloop()

    def create_window(self):
        '''Creates the GUI, gives it a title, sets the minimum size, and changes the background color'''
        window = Tk()
        window.title("Population Generator")
        window.minsize(400, 400)
        window.configure(background="grey91")
        return window

    def create_label_frame(self, type):
        '''Adds a label to the window to display text for the user.'''
        frame = ttk.Labelframe(self.window, text=type)
        frame.pack(fill="both", expand="yes", padx=5, pady=5)
        return frame

    def create_drop_down(self, values, default):
        '''Adds a drop down list (combobox) to the window for the user to select a value from'''
        drop_down = ttk.Combobox(self.input_frame, values=values)
        drop_down.set(default)
        drop_down.pack(padx=5, pady=5)
        return drop_down

    def create_button(self):
        '''Adds a button to get the population size and additional info for the State and Year selected'''
        button = ttk.Button(self.input_frame, text="Submit", command=self.get_data)
        button.pack(padx=5, pady=5)
        return button

    def create_label(self, frame, default, wrap=None):
        '''Adds a label for displaying results'''
        if wrap:
            label = Label(frame, text=default, wraplength=wrap, background="grey91")
        else:
            label = Label(frame, text=default, background="grey91")

        label.pack()
        return label

    def get_data(self):
        '''Gets the data that will be displayed on the GUI for the given year'''
        state = self.state_drop_down.get()
        year = self.years_drop_down.get()
        population_results = get_population(state, year)
        info_results = get_info(state, year)
        self.display_results(population_results, info_results, state, year)

    def display_results(self, population, info, state, year):
        '''Updates the labels on the GUI to contain the data that was just requested'''
        state_text = " ".join(["State:", state])
        year_text = " ".join(["Year:", year])
        pop_text = " ".join(["Population:", population[1][1]])
        self.state_label.configure(text=state_text)
        self.year_label.configure(text=year_text)
        self.population_label.configure(text=pop_text)
        self.info_label.configure(text=info)

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

    try:
        r = requests.get(base_url, params=predicates)
    except requests.exceptions.ConnectionError:
        return "Error connecting to the content generator server."

    return r.json()["wiki"]

def get_predicates(state):
    '''
    Sets the query parameters for the API call being made
    :param state: state to be request data from the API on
    :return predicates: parameters for the request URL
    '''
    predicates = {}
    predicates["get"] = ",".join(["NAME", "S0201_001E"])
    predicates["for"] = ":".join(["state", state_code[state]])
    predicates["key"] = "93647a1c34b435616eb32f2172d87eed03eebfa7"
    return predicates

def get_base_url(year):
    '''
    Creates the base url of the API request to get the population of a state in a year.
    :param year: year to get the population of
    :return base_url: url of the API request being made
    '''
    host = "https://api.census.gov/data"
    dataset = "acs/acs1/spp"
    base_url = "/".join([host, year, dataset])
    return base_url

def get_population(state, year):
    '''
    Makes a request to the API for the population size of a state in a given year.
    :param state: state to request population size of
    :param year: year to request the data
    :return: a json of the response from the request
    '''
    base_url = get_base_url(year)
    predicates = get_predicates(state)
    r = requests.get(base_url, params=predicates)
    return r.json()

def parse_input_csv():
    '''
    Parses the input.csv file for the state and year if it was passed as an argument when running the program.
    '''
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
    with open('output.csv', mode="w") as output_file:
        output_writer = csv.writer(output_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(["input_year", "input_state", "output_population_size"])
        output_writer.writerow([year, state, results[1][1]])

if __name__ == "__main__":
    # Checks if the user passed an argument in the command line signaling they do not want to use the GUI
    if len(sys.argv) > 1 and sys.argv[1] == 'input.csv':
        # Parses input.csv, requests the data from the census API, and writes the response to output.csv
        state, year = parse_input_csv()
        results = get_population(state, year)
        write_output_csv(results, state, year)
    else:
        # Starts the GUI application
        window = GUI()
