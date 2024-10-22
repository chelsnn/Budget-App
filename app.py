from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the expenses page
@app.route('/expenses')
def expenses():
    return render_template('expense.html')

if __name__ == "__main__":
    app.run(debug=True)
