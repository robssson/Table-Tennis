import requests
import json
import pandas as pd
from get_functions import get_value


def scrape_data(date):
    url = f'https://api.sofascore.com/api/v1/sport/table-tennis/scheduled-events/{date}'
    data = requests.get(url)
    json_data = json.loads(data.content)['events']
    return json_data


def parse_data(matches):
    for match in matches:
        status = get_value(match, 'status', default_key='code')
        if status == 100: # status equals 100 means, that the match is ended
            tournament_name = get_value(match, 'tournament', default_key='name')
            winner_code = get_value(match, 'winnerCode')
            player_1 = get_value(match, 'homeTeam', default_key='name')
            player_1_score = get_value(match, 'homeScore', default_key='display')
            player_2 = get_value(match, 'awayTeam', default_key='name')
            player_2_score = get_value(match, 'awayScore', default_key='display')
            pass


if __name__ == "__main__":
    date = '2021-06-01'
    matches = scrape_data(date)
    parse_data(matches)

