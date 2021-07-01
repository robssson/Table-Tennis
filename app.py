from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Hello! This is website to display stats from tennis-table matches!</h1>"


if __name__ == "__main__":
    app.run()
