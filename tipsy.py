"""
tipsy.py -- A flask-based todo list
"""
from flask import Flask, render_template, redirect, request, session, g
import model

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret'
)

@app.before_request
def set_up_db():
    g.db = model.connect_db()

@app.after_request
def disconnect_db(response):
    g.db.close()
    return response


@app.route("/")
def index():
    return render_template("index.html", user_name="chriszf")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/authenticate", methods=["POST"])
def authenticate():
    email = request.form['email']
    password = request.form['password']
    user_id = model.User.authenticate(g.db, email, password)
    session['user_id'] = user_id
    if session['user_id'] != None:
        return redirect("/tasks")
    return "wrong password or email"

@app.route("/save_task", methods=["POST"])
def save_task():
    user_id = session.get("user_id", None)
    title = request.form['title']
    model.Task.new(g.db, title, user_id.id)
    return redirect("/tasks")

@app.route("/tasks")
def list_tasks():
    user_id = session.get("user_id", None)
    tasks_from_db = model.User.get_tasks(g.db, user_id.id)
    return render_template("list_tasks.html", tasks=tasks_from_db)

@app.route("/task/<int:id>", methods=["GET"])
def view_task(id):
    task_from_db = model.get_task(g.db, id)
    return render_template("view_task.html", task=task_from_db)

@app.route("/task/<int:id>", methods=["POST"])
def complete_task(id):
    model.Task.complete(g.db, id)
    return redirect("/tasks")

@app.route("/set_date")
def set_date():
    session['date'] = datetime.datetime.now()
    return "Date set"

@app.route("/get_date")
def get_date():
    return str(session['date'])

if __name__ == "__main__":
    app.run(debug=True)
