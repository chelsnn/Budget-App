import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from collections import defaultdict
import requests


app = Flask(__name__)

# set secret key for session management
app.secret_key = 'my_secret_key_for_testing_in_development_server'

# create connection to sqlite database
def get_db_connection():
    conn = sqlite3.connect('testDB.db') 
    conn.row_factory = sqlite3.Row
    return conn


#app = Flask(__name__)

def create_users_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            address TEXT
        );
    ''')
    conn.commit()
    conn.close()

# Call this function when the app starts
create_users_table()

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



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('homepage'))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']

        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO users (fullname, email, username, password, address) VALUES (?, ?, ?, ?, ?)',
                (fullname, email, username, password, address)
            )
            conn.commit()
            return redirect(url_for('login'))  # Redirect to login after signup
        except sqlite3.IntegrityError:
            error_message = "Username or email already exists."
            return render_template('login.html', error=error_message, show_signup=True)
        finally:
            conn.close()

    return render_template('signup.html')

@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            error = "Passwords do not match."
            return render_template('login.html', error=error, show_forgot_password=True)
        
        conn = get_db_connection()
        conn.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('forgotPassword.html')



@app.route('/homepage')
def homepage():
    conn = get_db_connection()
    user_id = session.get('user_id')
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()

    if user:
        full_name = user['fullname']
        
    else:
        full_name = "Guest"
        

    
    return render_template('homepage.html', percent_left=percent_left, full_name=full_name)


def home():
    return render_template('homepage.html')


@app.route('/expenses')
def expenses():
    today = datetime.today().strftime('%Y-%m-%d')
    expenses_data = sorted(get_expenses(), key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True) #sorts expenses in backwards order to ensure display is in order
    
    #creates a dictionary with dates as keys to display expenses by date
    grouped_expenses = defaultdict(list)
    for expense in expenses_data:
        date = expense['date']
        grouped_expenses[date].append(expense)
    return render_template('expenses.html', expenses=grouped_expenses, today=today)

@app.route('/profile')
def profile():
    conn = get_db_connection()
    user = conn.execute(
        'SELECT fullname, email, username, password, address FROM users WHERE id = ?',
        (session['user_id'],)
    ).fetchone()
    conn.close()

    if user:
        # Split fullname into first and last names
        full_name = user['fullname'].split(' ', 1)
        profile_data = {
            'fullname':full_name,
            'email': user['email'],
            'username': user['username'],
            'password': user['password'],
            'home_country': user['address'],  # Assuming address is being used as home_country
        }

        return render_template('profile.html', data=profile_data, selected=selected)
    else:
        return redirect(url_for('login'))  # Redirect if user not found

@app.route('/edit_profile')
def edit_profile():
    if request.method == 'POST':
        # Capture the form data
        fullname = request.form['fullname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        home_country = request.form['address']

        # Update the submitted_data dictionary with new values
        submitted_data['fullname'] = fullname
        submitted_data['email'] = email
        submitted_data['username'] = username
        submitted_data['password'] = password
        submitted_data['address'] = home_country

        # You would typically also update this in the database
        conn = get_db_connection()
        conn.execute(
            'UPDATE users SET fullname = ?, email = ?, username = ?, password = ?, address = ? WHERE id = ?',
            (f"{fullname}", email, username, password, home_country, session['user_id'])
        )
        conn.commit()
        conn.close()

        return redirect(url_for('homepage'))  # Redirect to profile page after submission
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


def get_expenses():
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM expenses_details')
    expenses = cursor.fetchall()
    conn.close()
    return expenses


@app.route('/budget')
def budget():
    return render_template('budget.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         # Add authentication logic here
#         # if username == 'admin' and password == 'password':  # Dummy check
#         #     return redirect(url_for('homepage'))
#         # else:
#         #     return "Invalid credentials, please try again."
#     return render_template('login.html')



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

@app.route('/currency_converter', methods=['POST'])
def currency_converter():
    base_currency = request.form['base_currency'].upper()
    target_currency = request.form['target_currency'].upper()
    amount = float(request.form['amount'])
    print(f"Received: {base_currency}, {target_currency}, Amount: {amount}")

    api_key = 'bee70f6922891b797fde27b2'  
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}'

    response = requests.get(url)
    converted_amount = None
    error_message = None

    if response.status_code == 200:
        data = response.json()
        print("API RESPONSE:", data)
        if data['result'] == "success":
            exchange_rate = data['conversion_rate']
            converted_amount = amount * exchange_rate
        else: error_message = data.get('error-type', 'Unknown error occurred.')
    else: 
        error_message = f'API request failed with status code {response.status_code}'

    return render_template('homepage.html', converted_amount=converted_amount, amount=amount, 
                           base_currency=base_currency, target_currency=target_currency, error_message=error_message, first_name=submitted_data['first_name'], last_name=submitted_data['last_name'], percent_left=percent_left)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='127.0.0.1', port=5000)

