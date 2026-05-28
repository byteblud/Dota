from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'bloomtrack_secret'


db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    estimated_minutes = db.Column(db.Integer)
    actual_minutes = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form.get('title')
    estimated = request.form.get('estimated')

    task = Task(
        title=title,
        estimated_minutes=estimated,
        actual_minutes=0,
        completed=False
    )

    db.session.add(task)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/complete/<int:id>')
def complete_task(id):
    task = Task.query.get(id)

    if task:
        task.completed = True
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    tasks = Task.query.all()

    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.completed])

    app.run(debug=True)
