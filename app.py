import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# set secret key for session management
app.secret_key = 'my_secret_key_for_testing_in_development_server'

# create connection to sqlite database
def get_db_connection():
    conn = sqlite3.connect('testDB.db') 
    conn.row_factory = sqlite3.Row
    return conn

#dummy profile data
submitted_data = {
    'first_name': 'Jane',
    'last_name': 'Doe',
    'email': 'janedoe@example.com',
    'username': 'janed123',
    'password': '123456',
    'home_street': '1234 Park Ln',
    'home_city': 'New York',
    'home_country': 'United States'
}

#dummy category data
selected = ['Accommodation', 'Food', 'Travel']

#dummy budget data

percent_left = 75

@app.route('/')

@app.route('/homepage')
def homepage():
    print("First Name:", submitted_data['first_name'])  
    print("Last Name:", submitted_data['last_name'])  
    return render_template('homepage.html', percent_left=percent_left, first_name=submitted_data['first_name'], last_name=submitted_data['last_name'])

def home():
    return render_template('homepage.html')


@app.route('/expenses')
def expenses():
    return render_template('expenses.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', data=submitted_data, selected=selected)

@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html', data=submitted_data, selected=selected)

# @app.route('/homepage')
# def homepage():
#     return render_template('homepage.html')
    
@app.route('/addExpense', methods=['GET', 'POST'])
def addExpense():
    if request.method == 'POST':
        
        add_expense()

        # conn = get_db_connection()
        # conn.execute('INSERT INTO expenses (amount, expenseName, category, date, notes), VALUES (?,?)', (amount, expenseName, category, date, notes))
        # conn.commit()
        # conn.close()
        
        return redirect(url_for('expenses'))
    return render_template('addExpense.html')

def add_expense():
    conn = get_db_connection()
    amount = request.form.get('amount')
    expenseName = request.form.get('expenseName')
    category = request.form.get('category')
    date = request.form.get('date')
    notes = request.form.get('notes')
    budgetID = 1

    conn.execute('''
        INSERT INTO expenses_details (budget_id, amount, expenseName, category, date, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (budgetID, amount, expenseName, category, date, notes))
    conn.commit()
    conn.close()


# @app.route('/addExpenseSubmit', methods=['GET', 'POST'])
# def addExpenseSubmit():
#     if request.method == 'POST':
#         # retrieve user input from form
#         amount = request.form.get('amount')
#         expenseName = request.form.get('expenseName')
#         category = request.form.get('categories')
#         date = request.form.get('date')
#         notes = request.form.get('notes')
#         budgetID = 1 #placeholder


#         # insert data into sqlite
#         conn = get_db_connection()
#         cursor = conn.execute('INSERT INTO expenses_details (budget_id, amount, category, expenseName, notes, date) VALUES (?, ?, ?, ?, ?, ?)',
#             (budgetID, amount, category, expenseName, notes, date))
       
#         conn.commit()
#         conn.close()

#         # store record ID for current session
#         session['expenseID'] = cursor.lastrowid

#         # after form submission, redirect to budget_category page
#         return redirect(url_for('expenses'))


@app.route('/budget')
def budget():
    return render_template('budget.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Add authentication logic here
        # if username == 'admin' and password == 'password':  # Dummy check
        #     return redirect(url_for('homepage'))
        # else:
        #     return "Invalid credentials, please try again."
    return render_template('login.html')

#Dummy code for sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        emailaddress = request.form['emailaddress']
        username = request.form['username']
        password = request.form['password']
        homepage = request.form['homepage']
        # Add authentication logic here
    return render_template('signup.html')

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
def create_tables():
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

    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses_details (
            expenseID INTEGER PRIMARY KEY AUTOINCREMENT,
            budget_id INTEGER NOT NULL,
            amount TEXT NOT NULL,
            category TEXT NOT NULL,
            expenseName TEXT NOT NULL,
            notes TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY (budget_id) REFERENCES budget_details(id)
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
    create_tables()
    app.run(debug=True, host='127.0.0.1', port=5000)

