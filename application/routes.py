from application import app, db
from flask import render_template, jsonify, request, Response
from sofascore import get_match_stats, parse_match_stats
from application.models import Results
from connect_with_db import connect_to_db, close_connection, query_for_data, query_for_tournaments
import json


data = [{"data": {"name": "Tomek"}}]


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template('index.html', index=True)


@app.route("/tools/global")
def global_data():
    con = connect_to_db()
    res = query_for_data(con)
    results = res[0]
    results = results[:100]
    counts = res[1]
    close_connection(con)
    return render_template('global_data.html', results=results, counts=counts, whole_data=True)


@app.route("/tools/tournament_stats")
def tournament_stats(display=False):
    display = request.args.get('display')
    con = connect_to_db()
    tournament_names = query_for_tournaments(con)
    close_connection(con)
    if display:
        tournament_name = request.args.get('tour')
        print(tournament_name)
        return render_template('tournament_stats.html', tournament_name=tournament_name,
                               tournament_names=tournament_names, tournament=True, display=True)
    else:
        return render_template('tournament_stats.html', tournament_names=tournament_names, tournament=True)


@app.route("/tools/match_stats", methods=["GET"])
def match_stats(display=False):
    display = request.args.get('display')
    if display:
        match_id = request.args.get('match_id')
        raw_data = get_match_stats(match_id)
        stats = parse_match_stats(raw_data)
        stats = json.loads(stats)['sets']
        return render_template('match_stats.html', match_id=match_id, display=display, matchStats=stats, match=True)
    else:
        return render_template('match_stats.html', display=display, match=True)


@app.route('/api/')
@app.route('/api/<idx>')
def api(idx=None):
    if idx != None:
        return "Hello world!"
    else:
        return Response(json.dumps(data), mimetype="application/json")


@app.route('/results')
def user():
    Results(tournament_name='Test', player1='player1', player2='player2', player1_score=3, player2_score=2).save()
    results = Results.objects.all()
    return render_template("results.html", results=results)
