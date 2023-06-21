import sqlite3
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session

from db import create_task, get_tasks_without_user, mark_task_as_done, get_user, get_user_tasks

app = Flask(__name__)
app.secret_key = 'supertajny'


# mock_tasks = [
#     {"id": 0, "name": "Vynést odpadky", "description": "Prosím, fakt prosím lidi 🗑️", "is_done": False},
#     {"id": 1, "name": "Vytřít podlahu", "description": "V koupelně je to fakt síla 🤢", "is_done": False},
#     {"id": 2, "name": "Koupit mléko 🥛", "description": "Došlo a už nemáme žádné další", "is_done": True},
# ]

@app.route('/')
def home():
    tasks = get_tasks_without_user()
    context = {
        "tasks": tasks
    }
    return render_template('shared.html', **context)


@app.route('/add-shared', methods=['GET', 'POST'])
def add_shared():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        create_task(name, description)

        return redirect(url_for('home'))

    return render_template('add_shared.html')


@app.route('/done/<int:task_id>')
def done(task_id):
    mark_task_as_done(task_id)

    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        user = get_user(name)
        if user and user['password'] == password:
            session['user_id'] = user["id"]
            session['username'] = user["name"]
            return redirect(url_for('personal'))
        else:
            return render_template('login.html', error="Špatné údaje.")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))


@app.route('/personal')
def personal():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    tasks = get_user_tasks(session['user_id'])
    return render_template('personal.html', tasks=tasks)


@app.route('/add-personal', methods=['GET', 'POST'])
def add_personal():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        create_task(name, description, session["user_id"])
        return redirect(url_for('personal'))

    return render_template('add_personal.html')


@app.route('/done-personal/<int:task_id>')
def done_personal(task_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    mark_task_as_done(task_id, session["user_id"])

    return redirect(url_for('personal'))


if __name__ == "__main__":
    app.run(debug=True)
