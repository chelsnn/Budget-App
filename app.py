from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/expenses')
def expenses():
    return render_template('expenses.html')

@app.route('/homepage')
def expenses():
    return render_template('homepage.html')


if __name__ == '__main__':
    app.run(debug=True)
