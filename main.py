from flask import Flask, render_template, request, flash, session, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # This should be kept secret in real-world apps

file_path = os.path.join(app.root_path, 'constituents_financials.csv')
df = pd.read_csv(file_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    if request.method == 'POST':
        stock_to_remove = request.form['stock_to_remove']
        if 'portfolio' in session and stock_to_remove in session['portfolio']:
            session['portfolio'].remove(stock_to_remove)
            flash(f"{stock_to_remove} removed from your portfolio!")
        else:
            flash("Error: Stock not found in your portfolio!")
        return redirect(url_for('portfolio'))

    user_portfolio = session.get('portfolio', [])
    return render_template('portfolio.html', portfolio=user_portfolio)


@app.route('/stock_search', methods=['GET', 'POST'])
def stock_search():
    stock_info = None

    if request.method == 'POST':
        if "search" in request.form:
            stock_name = request.form['stock_name']
            stock_info = df[df['Name'] == stock_name].to_dict(orient='records')
            if not stock_info:
                flash("Error: Stock not in directory.")
                return render_template('stock_search.html')

        elif "add_to_portfolio" in request.form:
            stock_to_add = request.form['stock_to_add']
            if 'portfolio' not in session:
                session['portfolio'] = []
            session['portfolio'].append(stock_to_add)
            flash(f"{stock_to_add} added to your portfolio!")

    return render_template('stock_search.html', stock_info=stock_info)

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/stock_prediction')
def stock_prediction():
    return render_template('stock_prediction.html')

@app.route('/learning_materials')
def learning_materials():
    return render_template('learning_materials.html')

if __name__ == '__main__':
    app.run(debug=True, port=50001)
