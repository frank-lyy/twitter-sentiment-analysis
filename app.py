from flask import Flask, render_template, request
from sentiment_analysis import sentiment_analyzer

app = Flask('tweet_sentiment_analyzer')

@app.route('/')
def show_predict_stock_form():
    return render_template('searchform.html')

@app.route('/results', methods=['POST'])
def results():
    form = request.form
    if request.method == 'POST':
        query = form['query']
        sentiment = sentiment_analyzer(query)
        return render_template('resultsform.html', query=query, predicted_price=sentiment)