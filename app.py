from flask import Flask, render_template
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

@app.route('/expenses')
def expenses():
    return render_template('expenses.html')




@app.route('/profile')
def profile():
    return render_template('profile.html', data=submitted_data, selected=selected)

@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html', data=submitted_data, selected=selected)


if __name__ == '__main__':
    app.run(debug=True)
