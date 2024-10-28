from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/expenses')
def expenses():
    return render_template('expenses.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

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


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
