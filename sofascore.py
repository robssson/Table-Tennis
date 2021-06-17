import requests
import json
import pandas as pd
from datetime import date, timedelta
from get_functions import get_value
from connect_with_db import connect_to_db, insert_row_to_db, close_connection


def generate_dates():
    lst_of_dates = []
    sdate = date(2021, 6, 1)
    edate = date(2021, 6, 17)
    delta = edate - sdate
    for i in range(delta.days+1):
        day = sdate + timedelta(days=i)
        lst_of_dates.append(day)
    return lst_of_dates


def scrape_data(date):
    url = f'https://api.sofascore.com/api/v1/sport/table-tennis/scheduled-events/{date}'
    data = requests.get(url)
    json_data = json.loads(data.content)['events']
    return json_data


def parse_data(matches, date):
    con = connect_to_db()
    for match in matches:
        status = get_value(match, 'status', default_key='code')
        if status == 100: # status equals 100 means, that the match is ended
            tournament_name = get_value(match, 'tournament', default_key='name')
            winner_code = get_value(match, 'winnerCode')
            player_1 = get_value(match, 'homeTeam', default_key='name')
            player_1_score = get_value(match, 'homeScore', default_key='display')
            player_2 = get_value(match, 'awayTeam', default_key='name')
            player_2_score = get_value(match, 'awayScore', default_key='display')
            number_of_sets = player_1_score + player_2_score
            if int(player_1_score) > int(player_2_score):
                insert_row_to_db(con, date, player_1, player_2, tournament_name,
                                 player_1_score, player_2_score, number_of_sets)
            else:
                insert_row_to_db(con, date, player_2, player_1, tournament_name,
                                 player_2_score, player_1_score, number_of_sets)
    close_connection(con)


if __name__ == "__main__":
    dates = generate_dates()
    for day in dates:
        print(f"Scraping data for {day} in progress...")
        matches = scrape_data(day)
        parse_data(matches, day)

