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
        tasks = json.load(f)
    # Migrate old tasks
    for t in tasks:
        if 'description' not in t:
            t['description'] = ''
        if 'priority' not in t:
            t['priority'] = 'medium'
        if 'status' not in t:
            t['status'] = 'completed' if t.get('done', False) else 'pending'
            if 'done' in t:
                del t['done']
        if 'due_date' not in t:
            t['due_date'] = None
        if 'updated_at' not in t:
            t['updated_at'] = None
    return tasks

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
    description = request.form.get('description', '')
    priority = request.form.get('priority', 'medium')
    if title:
        tasks = load_tasks()
        # Simple ID generation based on list length
        new_task = {
            'id': len(tasks) + 1, 
            'title': title, 
            'description': description,
            'priority': priority,
            'status': 'pending',
            'due_date': None,
            'updated_at': None
        }
        tasks.append(new_task)
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>')
def toggle(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == task_id:
            t['status'] = 'completed' if t['status'] == 'pending' else 'pending'
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit(task_id):
    new_title = request.form.get('new_title')
    new_description = request.form.get('new_description', '')
    new_priority = request.form.get('new_priority', 'medium')
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == task_id:
            t['title'] = new_title
            t['description'] = new_description
            t['priority'] = new_priority
            # Update updated_at if needed
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)