from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<h2>Hello! This is website to display stats from tennis-table matches!</h2>"


if __name__ == "__main__":
    app.run()


