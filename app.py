from flask import Flask, render_template, request, redirect, url_for


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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

