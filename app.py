from flask import Flask, render_template, request
from sentiment_analysis import sentiment_analyzer

app = Flask('tweet_sentiment_analyzer')

@app.route('/')
def query():
    return render_template('query.html')

@app.route('/results', methods=['POST'])
def results():
    form = request.form
    if request.method == 'POST':
        query = form['query']
        sentiment = sentiment_analyzer(query)
        return render_template('results.html', query=query, sentiment_score=sentiment)