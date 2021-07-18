import flask
from application import db


class Results(db.Document):
    tournament_name = db.StringField(max_length=250)
    player1 = db.StringField(max_length=250)
    player2 = db.StringField(max_length=250)
    player1_score = db.IntField()
    player2_score = db.IntField()