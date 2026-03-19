from flask import Flask, render_template, request, redirect, url_for
from database import init_db, get_db

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    db = get_db()
    all_tasks = db.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
    db.close()
    return render_template('tasks.html', tasks=all_tasks)

@app.route('/tasks/add', methods=['POST'])
def add_task():
    title = request.form['title']
    db = get_db()
    db.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    db.commit()
    db.close()
    return redirect(url_for('tasks'))

@app.route('/tasks/complete/<int:id>')
def complete_task(id):
    db = get_db()
    db.execute('UPDATE tasks SET done = 1 WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('tasks'))

@app.route('/tasks/delete/<int:id>')
def delete_task(id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)