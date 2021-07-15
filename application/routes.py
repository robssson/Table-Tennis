from application import app
from flask import render_template, jsonify, request
from sofascore import get_match_stats, parse_match_stats
import json


@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template('index.html', index=True)


@app.route("/tools/global")
def global_data():
    return render_template('global_data.html', whole_data=True)


@app.route("/tools/tournament_stats")
def tournament_stats():
    return render_template('tournament_stats.html', tournament=True)


@app.route("/tools/match_stats")
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



