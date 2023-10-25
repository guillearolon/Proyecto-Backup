from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

# LISTA DE TAREAS
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    deleted = db.Column(db.Boolean, default=False)

@app.route('/tareas')
def tareas():
    tasks = Task.query.filter_by(deleted=False).all()
    deleted_tasks = Task.query.filter_by(deleted=True).all()
    return render_template('lista-tareas.html', tasks=tasks, deleted_tasks=deleted_tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    new_task = Task(title=title)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('tareas'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    task.deleted = True
    db.session.commit()
    return redirect('/tareas')

@app.route('/restore/<int:id>', methods=['POST'])
def restore_task(id):
    tarea = Task.query.get_or_404(id)
    tarea.deleted = False
    db.session.commit()
    return redirect('/tareas')
