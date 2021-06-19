import requests
import json
import pandas as pd
from requests.adapters import HTTPAdapter
from requests.exceptions import Timeout, ConnectionError
from datetime import date, timedelta
from get_functions import get_value
from connect_with_db import connect_to_db, insert_row_to_db, close_connection


def generate_dates():
    lst_of_dates = []
    start_date = date(2021, 5, 1)
    end_date = date(2021, 6, 17)
    delta = end_date - start_date
    for i in range(delta.days+1):
        day = start_date + timedelta(days=i)
        lst_of_dates.append(day)
    return lst_of_dates


def scrape_data(date):
    url = f'https://api.sofascore.com/api/v1/sport/table-tennis/scheduled-events/{date}'
    sofascore_adapter = HTTPAdapter(max_retries=5)
    session = requests.Session()
    session.mount('https://', sofascore_adapter)
    try:
        data = session.get(url, timeout=5)
        json_data = json.loads(data.content)
        return json_data['events']
    except ConnectionError as ce:
        print(ce)


def parse_data(matches, date):
    con = connect_to_db()
    for match in matches:
        status = get_value(match, 'status', default_key='code')
        if status == 100: # status equals 100 means, that the match is ended
            points = 0
            number_of_sets_temp = 0
            tournament_name = get_value(match, 'tournament', default_key='name')
            winner_code = get_value(match, 'winnerCode')
            player_1 = get_value(match, 'homeTeam', default_key='name')
            player_1_score = get_value(match, 'homeScore', default_key='display')
            player_2 = get_value(match, 'awayTeam', default_key='name')
            player_2_score = get_value(match, 'awayScore', default_key='display')
            number_of_sets = player_1_score + player_2_score
            for i in range(number_of_sets):
                try:
                    points += get_value(match, 'homeScore', default_key=f'period{i+1}')
                    points += get_value(match, 'awayScore', default_key=f'period{i+1}')
                    number_of_sets_temp += 1  # Sometimes API shows i.e 5 sets, but players played only 4 sets (BUG).
                except Exception as E:
                    break
            try:
                avg_of_points = round((points / number_of_sets_temp), 2)
            except Exception as E:
                break
            if int(player_1_score) > int(player_2_score):
                insert_row_to_db(con, date, player_1, player_2, tournament_name,
                                 player_1_score, player_2_score, number_of_sets, avg_of_points)
            else:
                insert_row_to_db(con, date, player_2, player_1, tournament_name,
                                 player_2_score, player_1_score, number_of_sets, avg_of_points)
    print("Data has been inserted to DB.")
    close_connection(con)


if __name__ == "__main__":
    dates = generate_dates()
    for day in dates:
        print(f"Scraping data for {day} in progress...")
        matches = scrape_data(day)
        parse_data(matches, day)

