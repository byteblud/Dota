from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'database/app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'bloomtrack_secret'

db = SQLAlchemy(app)


class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    estimated_minutes = db.Column(db.Integer)

    actual_minutes = db.Column(db.Integer, default=0)

    completed = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route('/')
def index():

    tasks = Task.query.order_by(Task.created_at.desc()).all()

    return render_template('index.html', tasks=tasks)


@app.route('/add_task', methods=['POST'])
def add_task():

    title = request.form.get('title')

    estimated = request.form.get('estimated')

    task = Task(
        title=title,
        estimated_minutes=estimated
    )

    db.session.add(task)

    db.session.commit()

    return redirect(url_for('index'))


@app.route('/complete/<int:id>')
def complete_task(id):

    task = Task.query.get_or_404(id)

    task.completed = True

    db.session.commit()

    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():

    tasks = Task.query.all()

    total = len(tasks)

    completed = len([t for t in tasks if t.completed])

    progress = 0

    if total > 0:
        progress = int((completed / total) * 100)

    return render_template(
        'dashboard.html',
        total=total,
        completed=completed,
        progress=progress,
        tasks=tasks
    )


@app.route('/focus')
def focus():

    tasks = Task.query.filter_by(completed=False).all()

    return render_template('focus.html', tasks=tasks)


@app.route('/roadmap')
def roadmap():

    return render_template('roadmap.html')


@app.route('/analytics')
def analytics():

    return render_template('analytics.html')


@app.route('/upload')
def upload():

    return render_template('upload.html')


if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)
