import requests
import json
import pandas as pd


def scrape_data(date):
    url = f'https://api.sofascore.com/api/v1/sport/table-tennis/scheduled-events/{date}'
    data = requests.get(url)
    json_data = json.loads(data.content)
    return json_data


def parse_data(results):
    return(results)


def display_data():
    pass


if __name__ == "__main__":
    date = '2021-06-01'
    results = scrape_data(date)
    parse_data(results)
    display_data()
