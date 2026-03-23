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

@app.route('/finances')
def finances():
    db = get_db()
    all_transactions = db.execute('SELECT * FROM finances ORDER BY created_at DESC').fetchall()
    total_income = db.execute('SELECT SUM(amount) FROM finances WHERE type = "income"').fetchone()[0] or 0
    total_expenses = db.execute('SELECT SUM(amount) FROM finances WHERE type = "expense"').fetchone()[0] or 0
    balance = total_income - total_expenses
    db.close()
    return render_template('finances.html', transactions=all_transactions, balance=balance, total_income=total_income, total_expenses=total_expenses)

@app.route('/finances/add', methods=['POST'])
def add_transaction():
    title = request.form['title']
    amount = float(request.form['amount'])
    type = request.form['type']
    category = request.form['category']
    db = get_db()
    db.execute('INSERT INTO finances (title, amount, type, category) VALUES (?, ?, ?, ?)', (title, amount, type, category))
    db.commit()
    db.close()
    return redirect(url_for('finances'))

@app.route('/finances/delete/<int:id>')
def delete_transaction(id):
    db = get_db()
    db.execute('DELETE FROM finances WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('finances'))

@app.route('/goals')
def goals():
    db = get_db()
    all_goals = db.execute('SELECT * FROM goals ORDER BY created_at DESC').fetchall()
    db.close()
    return render_template('goals.html', goals=all_goals)

@app.route('/goals/add', methods=['POST'])
def add_goal():
    title = request.form['title']
    description = request.form['description']
    target_date = request.form['target_date']
    db = get_db()
    db.execute('INSERT INTO goals (title, description, target_date) VALUES (?, ?, ?)', (title, description, target_date))
    db.commit()
    db.close()
    return redirect(url_for('goals'))

@app.route('/goals/complete/<int:id>')
def complete_goal(id):
    db = get_db()
    db.execute('UPDATE goals SET done = 1 WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('goals'))

@app.route('/goals/delete/<int:id>')
def delete_goal(id):
    db = get_db()
    db.execute('DELETE FROM goals WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('goals'))

@app.route('/watchlist')
def watchlist():
    db = get_db()
    all_items = db.execute('SELECT * FROM watchlist ORDER BY created_at DESC').fetchall()
    db.close()
    return render_template('watchlist.html', items=all_items)

@app.route('/watchlist/add', methods=['POST'])
def add_watchlist():
    title = request.form['title']
    genre = request.form['genre']
    type = request.form['type']
    db = get_db()
    db.execute('INSERT INTO watchlist (title, genre, type) VALUES (?, ?, ?)', (title, genre, type))
    db.commit()
    db.close()
    return redirect(url_for('watchlist'))

@app.route('/watchlist/watched/<int:id>')
def watched_item(id):
    db = get_db()
    db.execute('UPDATE watchlist SET watched = 1 WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('watchlist'))

@app.route('/watchlist/delete/<int:id>')
def delete_watchlist(id):
    db = get_db()
    db.execute('DELETE FROM watchlist WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('watchlist'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)