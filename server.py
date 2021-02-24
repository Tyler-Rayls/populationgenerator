import os

from populationgenerator import get_population
from flask import Flask, request, jsonify

state_code = {"AK": "02", "AL": "01", "AR": "05", "AZ": "04", "CA": "06", "CO": "08", "CT": "09", "DC": "11", "DE": "10",
              "FL": "12", "GA": "13", "HI": "15", "IA": "19", "ID": "16", "IL": "17", "IN": "18", "KS": "20", "KY": "21",
              "LA": "22", "MA": "25", "MD": "24", "ME": "23", "MI": "26", "MN": "27", "MO": "29", "MS": "28", "MT": "30",
              "NC": "37", "ND": "38", "NE": "31", "NH": "33", "NJ": "34", "NM": "35", "NV": "32", "NY": "36", "OH": "39",
              "OK": "40", "OR": "41", "PA": "42", "RI": "44", "SC": "45", "SD": "46", "TN": "47", "TX": "48", "UT": "49",
              "VA": "51", "VT": "50", "WA": "53", "WI": "55", "WV": "54", "WY": "56"}

app = Flask(__name__)

@app.route('/get', methods=['GET'])
def respond():
    state = request.args.get("state")
    year = request.args.get("year")

    if not state or not year:
        return "The state or year was not provided."

    results = get_data(state, year)

    response = {"state": state, "year": year, "population": results[1][1]}

    return jsonify(response)

@app.route('/')
def index():
    return "Enter a get request in the following format: '/get?state=state&year=year'"

if __name__ == "__main__":
    app.run(port=(os.getenv('PORT') if os.getenv('PORT') else 5003))