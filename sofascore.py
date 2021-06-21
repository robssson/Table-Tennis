import requests
import json
import pandas as pd
from requests.adapters import HTTPAdapter
from requests.exceptions import Timeout, ConnectionError
from datetime import date, timedelta
from parse_data import parse_matches_data, parse_match_stats


def generate_dates():
    lst_of_dates = []
    start_date = date(2021, 5, 1)
    end_date = date(2021, 6, 20)
    delta = end_date - start_date
    for i in range(delta.days+1):
        day = start_date + timedelta(days=i)
        lst_of_dates.append(day)
    return lst_of_dates


def make_http_request(url):
    sofascore_adapter = HTTPAdapter(max_retries=5)
    session = requests.Session()
    session.mount('https://', sofascore_adapter)
    try:
        data = session.get(url, timeout=5)
        json_data = json.loads(data.content)
        return json_data
    except ConnectionError as ce:
        print(ce)


def scrape_data(date):
    url = f'https://api.sofascore.com/api/v1/sport/table-tennis/scheduled-events/{date}'
    return make_http_request(url)


def get_match_stats(id):
    url = f'https://api.sofascore.com/api/v1/event/{id}/statistics'
    return make_http_request(url)


if __name__ == "__main__":
    dates = generate_dates()
    for day in dates:
        print(f"Scraping data for {day} in progress...")
        matches = scrape_data(day)
        parse_matches_data(matches, day)
    match = get_match_stats('9548291')
    match_stats = parse_match_stats(match)
    print(match_stats)


