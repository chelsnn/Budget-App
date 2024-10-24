import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# set secret key for session management
app.secret_key = 'my_secret_key_for_testing_in_development_server'

# create connection to sqlite database
def get_db_connection():
    conn = sqlite3.connect('database.db') 
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/expenses')
def expenses():
    return render_template('expenses.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/budget_form')
def budget_form():
    return render_template('budget_form.html')

@app.route('/budget_form_submit', methods=['GET', 'POST'])
def budget_form_submit():
    if request.method == 'POST':
        # retrieve user input from form
        budget = request.form['budget']
        arrival_date = request.form['arrival_date']
        departure_date = request.form['departure_date']
        city = request.form['city']
        country = request.form['country']

        # insert data into sqlite
        conn = get_db_connection()
        cursor = conn.execute('INSERT INTO budget_details (budget, arrival_date, departure_date, city, country, categories) VALUES (?, ?, ?, ?, ?, ?)',
            (budget, arrival_date, departure_date, city, country, 'temp'))
        conn.commit()
        conn.close()

        # store record ID for current session
        session['budget_id'] = cursor.lastrowid

        # after form submission, redirect to budget_category page
        return redirect(url_for('budget_category'))

@app.route('/budget_category')
def budget_category():
    return render_template('budget_category.html')

@app.route('/budget_category_submit', methods=['GET', 'POST'])
def budget_category_submit():
    if request.method == 'POST':
        # retrieve selected categories from form
        selected_categories = request.form.getlist('categories')

        # concatenate categories
        categories_str = ', '.join(selected_categories)

        # insert string into database in appropriate row
        budget_id = session.get('budget_id')  # retrieve record ID for current session
        if budget_id:
            conn = get_db_connection()
            conn.execute(
                'UPDATE budget_details SET categories = ? WHERE id = ?',
                (categories_str, budget_id)
            )
            conn.commit()
            conn.close()

        # after form submission, redirect to budget_view page
        return redirect(url_for('budget_view'))

# create database to store user data
def create_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS budget_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            budget REAL NOT NULL,
            arrival_date TEXT NOT NULL,
            departure_date TEXT NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            categories TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

@app.route('/budget_view')
def budget_view():
    return render_template('budget_view.html')

@app.route('/advice')
def advice():
    return render_template('advice.html')

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
