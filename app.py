from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


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


@app.route('/homepage')
def homepage():
    return render_template('homepage.html')
    
@app.route('/addExpense', methods=['GET', 'POST'])
def addExpense():
    if request.method == 'POST':
        amount = request.form.get('amount')
        expenseName = request.form.get('expenseName')
        category = request.form.get('categories')
        date = request.form.get('date')
        notes = request.form.get('notes')

        # conn = get_db_connection()
        # conn.execute('INSERT INTO expenses (amount, expenseName, category, date, notes), VALUES (?,?)', (amount, expenseName, category, date, notes))
        # conn.commit()
        # conn.close()
        
        return redirect(url_for('expenses'))
    return render_template('addExpense.html')

@app.route('/budget')
def budget():
    return render_template('budget.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

