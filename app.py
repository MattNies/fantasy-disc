# app.py
from flask import Flask, request, jsonify
import competitor
import create_roster
import scoring_round

app = Flask(__name__)

countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]


def _find_next_id():
    return max(country["id"] for country in countries) + 1


@app.get("/countries")
def get_countries():
    return jsonify(countries)


@app.post("/countries")
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415


_roster = """
Status,Curtis,Chris,Matt,Aaron,Jim,Kyle,Tim
Active,Niklas Anttila [91249],James Conrad [17295],Eagle McMahon [37817],Ricky Wysocki [38008],Isaac Robinson [50670],Anthony Barela [44382],Calvin Heimburg [45971]
Active,Jakub Semerád [91925],Paul Oman [34344],Ezra Aderhold [121715],Joel Freeman [69509],Luke Humphries [69424],Kyle Klein [85132],Chandler Kramer [139228]
Active,Eric Oakley [53565],Adam Hammes [57365],Kevin Jones [41760],Alden Harris [98091],Corey Ellis [44512],Kevin Kiefer III [97115],Thomas Gilbert [85850]
Active,Aaron Gossage [35449],Jake Monn [98722],Matthew Orum [18330],Väinö Mäkelä [59635],James Proctor [34250],Greg Barsby [15857],Chris Dickerson [62467]
Active,Ben Callaway [39015],Chris Clemons [50401],Bradley Williams [31644],Evan Smith [101574],Ezra Robinson [50671],Brodie Smith [128378],Robert Burridge [96512]
Active,Knut Valen Haland [35070],Cole Redalen [79748],Matt Bell [48950],Albert Tamm [76669],Nate Sexton [18824],Paul Ulibarri [27171],Mauri Villmann [107197]
AutoSub,Emerson Keith [47472],Andrew Presnell [63765],Tristan Tanner [99053],Jason Hebenheimer [43762],Casey White [81739],Lauri Lehtinen [82297],Austin Turner [54049]
Inactive,Mason Ford [72844],Austin Hannum [68835],Zach Melton [38631],Parker Welck [39491],Jeremy Koling [33705],Garrett Gurthie [13864],Andrew Marwede [75590]
Inactive,Gannon Buhr [75412],Nikko Locastro [11534],Gavin Rathbun [60436],Zach Arlinghaus [65266],Gavin Babcock [80331],Scott Stokely [3140],Aidan Scott [99246]
Inactive,Cale Leiviska [24341],Paul McBeth [27523],Michael Johansen [20300],Linus Carlsson [82098],Simon Lizotte [8332],Kyle Honeyager [84173],Drew Gibson [48346]
"""


@app.get("/event_roster")
def get_event_roster():
    event_id = request.args.get('event_id')
    event_modifier = float(request.args.get('event_modifier'))
    latest_round = request.args.get('latest_round')

    event_roster = create_roster.create_roster(_roster)

    scoring_rounds = [
        {'event_id': event_id, 'event_modifier': event_modifier}
    ]

    competitor_list = [
    ]

    for competitor_name, players in event_roster.items():
        active = []
        autosub = []
        inactive = []
        for player in players:
            if player['status'] == 'active':
                active.append(player['pdga'])
            elif player['status'] == 'autosub':
                autosub = player['pdga']
            else:
                inactive.append(player['pdga'])

        competitor_list.append(competitor.Competitor(competitor_name, active, autosub, inactive))

    for scoring_round_event in scoring_rounds:

        scoring_round_results = scoring_round.ScoringRound(scoring_round_event['event_id'],
                                                           scoring_round_event['event_modifier'], latest_round)

        for event_competitor in competitor_list:
            scoring_round_results.competitor_results(event_competitor)

        scoring_round_results.print_event_details()
        scoring_round_results.print_event_summary()

    return jsonify(event_roster, 201)
