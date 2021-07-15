from application import app
from flask import render_template, jsonify
from sofascore import get_match_stats, parse_match_stats


@app.route("/")
def index():
    return render_template('index.html', index=True)


@app.route("/tools/global")
def global_data():
    return render_template('global_data.html', whole_data=True)


@app.route("/tools/tournament_stats")
def tournament_stats():
    return render_template('tournament_stats.html', tournament=True)


@app.route("/tools/match_stats")
def match_stats():
    match = get_match_stats('9548291')
    stats = parse_match_stats(match)
    return render_template('match_stats.html', data=stats, match=True)
