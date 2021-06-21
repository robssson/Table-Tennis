from connect_with_db import connect_to_db, insert_row_to_db, close_connection
from get_functions import get_value
from collections import defaultdict
import json


def parse_matches_data(matches, date):
    con = connect_to_db()
    matches = matches['events']
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
            sets = player_1_score + player_2_score
            match_id = get_value(match, 'id')
            for i in range(sets):
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
                insert_row_to_db(con, date, match_id, tournament_name, player_1, player_2,
                                 player_1_score, player_2_score, sets, avg_of_points)
            else:
                insert_row_to_db(con, date, match_id, tournament_name, player_2, player_1,
                                 player_2_score, player_1_score, sets, avg_of_points)
    print("Data has been inserted to DB.")
    close_connection(con)


def parse_match_stats(stats):
    json_dict = defaultdict(list)
    stats_dct = {}
    stats = stats['statistics']
    for period in stats:
        period_name = period['period']
        if period_name not in 'ALL':
            stats_dct['period_name'] = period_name
            for group in period['groups']:
                if group['groupName'] == "Points":
                    statistics_items = group['statisticsItems']
                    for stat_item in statistics_items:
                        if stat_item['name'] == 'Points won':
                            stats_dct['home_points'] = stat_item['home']
                            stats_dct['away_points'] = stat_item['away']
                        elif stat_item['name'] == 'Biggest lead':
                            stats_dct['biggest_lead_home'] = stat_item['home']
                            stats_dct['biggest_lead_away'] = stat_item['away']
                    stats_dct_copy = stats_dct.copy()
                    json_dict['sets'].append(stats_dct_copy)
    return json.dumps(json_dict, indent=4)


