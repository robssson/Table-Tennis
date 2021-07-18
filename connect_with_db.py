import psycopg2

# connect to the db


def connect_to_db():
    con = psycopg2.connect(
            host="localhost",
            database="results",
            user="robssson",
            password="robssson123" # password only for this project
    )
    return con


def insert_row_to_db(con, *values):
    data = []
    cur = con.cursor()
    insert_query = '''insert into results(date, match_id, tournament_name, player_1, player_2, 
                    player_1_score, player_2_score, sets, points_per_set) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    for val in values:
        data.append(val)
    data_to_insert = data
    cur.execute(insert_query, data_to_insert)
    con.commit()
    cur.close()


def query_for_data(con):
    cur = con.cursor()
    cur.execute("SELECT tournament_name, player_1, player_2, player_1_score, player_2_score FROM results")
    counts = cur.rowcount
    rows = cur.fetchall()
    return [rows, counts]


def close_connection(con):
    con.close()


def query_for_tournaments(con):
    cur = con.cursor()
    cur.execute("SELECT distinct tournament_name from results order by 1")
    tournaments_list = cur.fetchall()
    return tournaments_list
