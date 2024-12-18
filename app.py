from collections import defaultdict
import sqlite3
import os
import prompts

import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session
import requests
import openai
from dotenv import load_dotenv, find_dotenv

from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# set keys
load_dotenv()
app.secret_key = os.getenv("FLASK_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
exchange_key = os.getenv("xchange_key")
pepper = os.getenv("PEPPER")

# set OpenAI preferences
client = openai  
temperature = 0.7  
max_tokens = 500  
model = "gpt-4o-mini"

# create connection to sqlite database
def get_db_connection():
    conn = sqlite3.connect('database.db') 
    conn.row_factory = sqlite3.Row
    return conn




# create database to store user data
def create_tables():
    conn = get_db_connection()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            salt TEXT NOT NULL,
            address TEXT NOT NULL
        );
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS budget_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            budget REAL NOT NULL,
            arrival_date TEXT NOT NULL,
            departure_date TEXT NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            categories TEXT NOT NULL,
            api_output TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
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

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # store username, hashed password, and salt in the database
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()
        conn.close()

        if user:
            # retrieve stored hash and salt
            stored_hashed_password = user['password']

            # combine input password with pepper
            password_with_pepper = password + pepper

            # Hash the combined password with the stored salt
            is_valid = bcrypt.checkpw(password_with_pepper.encode('utf-8'), stored_hashed_password)

        
            if is_valid:
                session['user_id'] = user['id']
                return redirect(url_for('homepage'))
                
            else:
                return render_template('login.html', error="Invalid credentials") # display error message if incorrect password
            
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # obtain user input from signup form
        fullname = request.form['fullname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']

        # generate a unique salt
        salt = bcrypt.gensalt()

        # add pepper to the password
        password_with_pepper = password + pepper

        # hash combined password with salt
        hashed_password = bcrypt.hashpw(password_with_pepper.encode('utf-8'), salt)

        # store new user info in 'users' table
        conn = get_db_connection()
        try:
            conn.execute(
                'INSERT INTO users (fullname, email, username, password, salt, address) VALUES (?, ?, ?, ?, ?, ?)',
                (fullname, email, username, hashed_password, salt, address)
            )
            conn.commit()
            return redirect(url_for('login')) # redirect to login webpage if account creation successful 
        except sqlite3.IntegrityError:
            error_message = "Username or email already exists."
            return render_template('login.html', error=error_message, show_signup=True) # display error message if creation unsuccessful
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
            error_message = "Passwords do not match."
            return render_template('login.html', error=error_message, show_forgot_password=True)
        
        # generate a unique salt
        salt = bcrypt.gensalt()

        # add pepper to the password
        password_with_pepper = new_password + pepper

        # hash combined password with salt
        hashed_password = bcrypt.hashpw(password_with_pepper.encode('utf-8'), salt)
        
        conn = get_db_connection()
        conn.execute('UPDATE users SET password = ? WHERE username = ?', (hashed_password, username))
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
       fullname = user['fullname']
   else:
       fullname = "Guest"


   remaining_budget, total_budget, percent_left = calculate_budget_left()
   total_budget = round(total_budget, 2)
   remaining_budget = round(remaining_budget, 2)
   percent_left = round(percent_left, 2)


   today = datetime.today().strftime('%Y-%m-%d')
   expenses_data = sorted(
   sorted(get_expenses(), key=lambda x: x['expenseID'], reverse=True)[:5],
   key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'),
   reverse=True
)
   grouped_expenses = defaultdict(list)
   for expense in expenses_data:
       formatted_date = datetime.strptime(expense['date'], '%Y-%m-%d')  # Adjust format as necessary
       date = formatted_date.strftime('%m-%d-%Y')
       grouped_expenses[date].append(expense)


   today = datetime.today().strftime('%m-%d-%Y')
      
   return render_template('homepage.html', percent_left=percent_left, fullname=fullname, expenses=grouped_expenses, today=today)






def home():
    return render_template('homepage.html')


@app.route('/expenses')
def expenses():
    today = datetime.today().strftime('%Y-%m-%d')
    expenses_data = sorted(get_expenses(), key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), reverse=True) #sorts expenses in backwards order to ensure display is in order
    
    #creates a dictionary with dates as keys to display expenses by date
    grouped_expenses = defaultdict(list)
    for expense in expenses_data:
        formatted_date = datetime.strptime(expense['date'], '%Y-%m-%d')  # Adjust format as necessary
        date = formatted_date.strftime('%m-%d-%Y')
        grouped_expenses[date].append(expense)

    today = datetime.today().strftime('%m-%d-%Y')
    return render_template('expenses.html', expenses=grouped_expenses, today=today)

 #sorts expenses in backwards order to ensure display is in order
    
@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    conn.close()

    if user:
        # Split fullname into first and last names
        fullname = user['fullname']

        return render_template('profile.html', user=user, fullname=fullname)
    else:
        return redirect(url_for('login'))  # Redirect if user not found

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user_id = session.get('user_id')
    conn = get_db_connection()
    """cursor = conn.execute("PRAGMA table_info(users);")
    columns = cursor.fetchall()
    for column in columns:
        print(column)"""
    if request.method == 'POST':
        # Capture the form data
        fullname = request.form['fullname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']

        # test form answers
        print(f"User ID: {user_id}")
        print(f"Full Name: {fullname}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Address: {address}")
        

        # You would typically also update this in the database
        
        conn.execute(
            '''UPDATE users SET fullname = ?, email = ?, username = ?, password = ?, address = ? WHERE id = ?''',
            (fullname, email, username, password, address, user_id)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('profile'))  # Redirect to profile page after submission
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return render_template('edit_profile.html', user=user)

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
    budgetID = session['user_id']

    

    conn.execute('''
        INSERT INTO expenses_details (budget_id, amount, expenseName, category, date, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (budgetID, amount, expenseName, category, date, notes))
    conn.commit()
    conn.close()

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    conn = get_db_connection()  # Open a new database connection
    conn.execute('DELETE FROM expenses_details WHERE expenseID = ?', (expense_id,))
    conn.commit()
    conn.close()  # Close the database connection
    return redirect(url_for('expenses'))

def get_expenses():
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM expenses_details WHERE budget_id = ?', (session['user_id'],))

    expenses = cursor.fetchall()
    conn.close()
    return expenses

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

        # simple validation checks
        error = None
        if not budget.isdigit():
            error = "Budget must be a numeric value."
        elif not arrival_date or not departure_date:
            error = "Both arrival and departure dates are required."
        elif not city or not country:
            error = "City and country are required."

        # if user input invalid, render budget_form again with the error message
        if error:
            return render_template('budget_form.html', error=error)

        # retrieve the user id from the session if logged in
        user_id = session.get('user_id')

        if user_id:
            # insert user input into sqLite
            conn = get_db_connection()
            cursor = conn.execute(
                'INSERT INTO budget_details (budget, arrival_date, departure_date, city, country, categories, api_output, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (budget, arrival_date, departure_date, city, country, 'temp', 'temp', user_id)
            )
            conn.commit()
            conn.close()
            
            # store the record id for current session
            session['budget_id'] = cursor.lastrowid

            # After form submission, redirect to budget_category page
            return redirect(url_for('budget_category'))
        else:
            return "Error: User not logged in", 403

@app.route('/budget_category')
def budget_category():
    return render_template('budget_category.html')

@app.route('/budget_category_submit', methods=['GET', 'POST'])
def budget_category_submit():
    if request.method == 'POST':
        # retrieve selected categories from the form
        selected_categories = request.form.getlist('categories')

        # concatenate categories into a string
        categories_str = ', '.join(selected_categories)

        budget_id = session.get('budget_id') 
        if budget_id:
            conn = get_db_connection()

            # update value in categories column for current row
            conn.execute(
                'UPDATE budget_details SET categories = ? WHERE id = ?',
                (categories_str, budget_id)
            )

            # retrieve values from the database and store them in variables
            budget_row = conn.execute(
                'SELECT budget, arrival_date, departure_date, city, country FROM budget_details WHERE id = ?',
                (budget_id,)
            ).fetchone()

            if budget_row:
                # if OpenAI API key not active, store error message into ai_output column of budget_details table
                if not openai.api_key or openai.api_key == "placeholder":
                    error_message = "Sorry, our OpenAI API is currently unavailable."
                    conn.execute(
                        'UPDATE budget_details SET api_output = ? WHERE id = ?', (error_message, budget_id)
                    )
                    return redirect(url_for('budget_view'))

                budget, arrival_date, departure_date, city, country = budget_row

                # generate prompt using the variables
                prompt = prompts.generate_budget_prompt(budget, arrival_date, departure_date, city, country, categories_str)

                # call OpenAI API with the generated prompt
                response = client.chat.completions.create(
                    model = model,
                    messages=[
                        {"role": "system", "content": prompts.system_message},
                        {"role": "user", "content": prompt}
                    ],
                    temperature = temperature,
                    max_tokens = max_tokens
                )

                # retrieve the API output as plain text
                api_output = response.choices[0].message.content

                # store the API output message in the database
                conn.execute(
                    'UPDATE budget_details SET api_output = ? WHERE id = ?',
                    (api_output, budget_id)
                )

                conn.commit()
                conn.close()
            else:
                print("Error: No data found for budget_id:", budget_id)

        # after form submission, redirect to the budget_view page
        return redirect(url_for('budget_view'))
    
@app.route('/budget_view')
def budget_view():
    budget_id = session.get('budget_id')
    if budget_id:
        conn = get_db_connection()

        # retrieve budget details along with API output
        budget_row = conn.execute(
            'SELECT budget, arrival_date, departure_date, city, country, categories, api_output FROM budget_details WHERE id = ?',
            (budget_id,)
        ).fetchone()
        
        if budget_row:
            budget, arrival_date, departure_date, city, country, categories, api_output = budget_row
            # pass data to the template
            return render_template('budget_view.html', budget=budget, arrival_date=arrival_date, 
                                   departure_date=departure_date, city=city, country=country, categories=categories,
                                   api_output=api_output)
        else:
            # Handle the case where no budget was found for the budget_id
            return "Budget not found.", 404  # You can return a more user-friendly template or message here
        
        conn.close()
    
    # Handle the case where no budget_id was found in the session
    return "No budget ID in session.", 400  # You can return a more user-friendly template or message here

@app.route('/advice')
def advice():
    return render_template('advice.html')

@app.route('/currency_converter', methods=['POST'])
def currency_converter():
    base_currency = request.form['base_currency'].upper()
    target_currency = request.form['target_currency'].upper()
    amount = float(request.form['amount'])
    print(f"Received: {base_currency}, {target_currency}, Amount: {amount}")

    # obtain current user's name to render homepage template
    conn = get_db_connection()
    user_id = session.get('user_id')
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()

    remaining_budget, total_budget, percent_left = calculate_budget_left()

    # obtain current user's expenses to render homepage template
    expenses_data = sorted(
    sorted(get_expenses(), key=lambda x: x['expenseID'], reverse=True)[:5],
    key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'), 
    reverse=True
)  
    grouped_expenses = defaultdict(list)
    for expense in expenses_data:
        date = expense['date']
        grouped_expenses[date].append(expense)

    if user:
        fullname = user['fullname']
    else:
        fullname = "Guest"
    
    url = f'https://v6.exchangerate-api.com/v6/{exchange_key}/pair/{base_currency}/{target_currency}'

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
                           base_currency=base_currency, target_currency=target_currency, error_message=error_message, 
                           percent_left=percent_left, fullname=fullname, expenses=grouped_expenses)

@app.route('/calculate_budget_left')
def calculate_budget_left():
   user_id = session.get('user_id') 
   if not user_id:
       return {"error": "User not logged in"}, 400  # Handle the case where user_id is missing


   conn = get_db_connection()
  
   budget_data = conn.execute(
       'SELECT budget FROM budget_details WHERE user_id = ?', (user_id,)
   ).fetchone()
   total_budget = budget_data[0] if budget_data else 0  # Access by index
   
   expenses_data = conn.execute(
        'SELECT SUM(amount) AS total_expenses FROM expenses_details WHERE budget_id = ?',
        (user_id,)
    ).fetchone()
   total_expenses = expenses_data[0] if expenses_data and expenses_data[0] else 0  # Access by index
   conn.close()
  
   remaining_budget = total_budget - total_expenses
   if total_budget > 0:
       percent_left = (remaining_budget / total_budget) * 100
   else:
       percent_left = 0
   return remaining_budget, total_budget, percent_left








if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='127.0.0.1', port=5000)

