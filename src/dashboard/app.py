from flask import Flask, render_template, jsonify
from src.database.db_handler import DatabaseHandler
from src.analysis.price_predictor import PricePredictor
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)
db_handler = DatabaseHandler('ecommerce_data.db')
price_predictor = PricePredictor()

@app.route('/')
def index():
    products = db_handler.get_all_products()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product_history = db_handler.get_product_history(product_id)
    df = pd.DataFrame(product_history, columns=['price', 'platform', 'timestamp'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    price_predictor.train(product_history)
    future_prices = price_predictor.predict_future_prices()
    
    fig = go.Figure()
    for platform in df['platform'].unique():
        platform_data = df[df['platform'] == platform]
        fig.add_trace(go.Scatter(x=platform_data['timestamp'], y=platform_data['price'], mode='lines+markers', name=platform))
    
    fig.add_trace(go.Scatter(x=[p['date'] for p in future_prices], y=[p['price'] for p in future_prices], mode='lines', name='Predicted', line=dict(dash='dash')))
    
    fig.update_layout(title='Price History and Prediction', xaxis_title='Date', yaxis_title='Price')
    
    return render_template('product.html', product_id=product_id, graph=fig.to_json())

if __name__ == '__main__':
    app.run(debug=True)
