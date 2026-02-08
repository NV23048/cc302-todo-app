from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = 'tasks.json'

# Helper functions to handle JSON storage
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    if title:
        tasks = load_tasks()
        # Simple ID generation based on list length
        new_task = {'id': len(tasks) + 1, 'title': title, 'done': False}
        tasks.append(new_task)
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    new_title = request.form.get('new_title')
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == task_id:
            t['title'] = new_title
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)