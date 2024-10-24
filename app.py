import sqlite3
from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/budget')
def budget():
    return render_template('budget.html')

# route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_program_details():
    if request.method == 'POST':
        # obtain user input from form
        budget = request.form['budget']
        arrival_date = request.form['arrival_date']
        departure_date = request.form['departure_date']
        city = request.form['city']
        country = request.form['country']

        # insert data into sqlite
        conn = get_db_connection()
        conn.execute(
            (budget, arrival_date, departure_date, city, country)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('advice'))


if __name__ == '__main__':
    app.run(debug=True)
