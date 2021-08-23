from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SECRET_KEY'] = os.environ.get('TODO_API_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)

# db.create_all()


@app.route("/")
def home():
    all_tasks = Todo.query.all()
    today = str(date.today())
    return render_template("index.html", tasks=all_tasks, date=today)


@app.route("/add", methods=["GET", "POST"])
def add():
    date_task = request.form['trip-start']
    date_task = datetime.strptime(date_task, '%Y-%m-%d').date().strftime('%d-%m')
    new_task = Todo(task=request.form['todotask'], date=date_task, complete=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/done", methods=["GET", "POST"])
def done():
    task_id = request.args.get('id')
    task = Todo.query.get(task_id)
    today = str(date.today().strftime('%d-%m'))
    task.date = today
    task.complete = True
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete", methods=["GET", "POST"])
def delete():
    task_id = request.args.get('id')
    task = Todo.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
