from flask import Flask, render_template, request
app = Flask('tweet_sentiment_analyzer')

@app.route('/')
def show_predict_stock_form():
    return render_template('predictorform.html')
@app.route('/results', methods=['POST'])
def results():
    form = request.form
    if request.method == 'POST':
    #write your function that loads the model
        model = get_model() #you can use pickle to load the trained model
        year = request.form['year']
        predicted_stock_price = model.predict(year)
        return render_template('resultsform.html', year=year, predicted_price=predicted_stock_price)