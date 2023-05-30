from flask import Flask, render_template, request
from sentiment_analysis import sentiment_analyzer

app = Flask(__name__)

@app.route('/')
def query():
    return render_template('query.html')

@app.route('/results', methods=['POST'])
def results():
    form = request.form
    if request.method == 'POST':
        query = form['query']
        sentiment, pos_tweets, neg_tweets = sentiment_analyzer(query)
        return render_template('results.html', query=query, sentiment_score=sentiment, pos_tweets=pos_tweets, neg_tweets=neg_tweets)
    
if __name__ == "__main__":
    app.run(debug=True)