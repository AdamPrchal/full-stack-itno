from flask import (
    Flask,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

app = Flask(__name__)
app.secret_key = "supertajny"


mock_tasks = [
    {
        "id": 0,
        "name": "Vynést odpadky",
        "description": "Prosím, fakt prosím lidi 🗑️",
        "is_done": False,
    },
    {
        "id": 1,
        "name": "Vytřít podlahu",
        "description": "V koupelně je to fakt síla 🤢",
        "is_done": False,
    },
    {
        "id": 2,
        "name": "Koupit mléko 🥛",
        "description": "Došlo a už nemáme žádné další",
        "is_done": True,
    },
]


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
