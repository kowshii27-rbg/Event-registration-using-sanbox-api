from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import json

app = Flask(__name__)

# Your PayPal sandbox client ID and secret
PAYPAL_CLIENT_ID = 'AZ4jxSTKBz_HfzWC55Q--dE8YOqEtv80KokoUPmUalRVD2_RRhB5r5Q15T8yiUpcPTnMBaumrzbwf8Tk'
PAYPAL_CLIENT_SECRET = 'EG1OVqlUbD8haxuWYckJKoIpWwAhwt8ITCTP8RYir4F5IfhNW1VtTrDVHVusP1VQBe3cJbAgFOU9LOys'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-order', methods=['POST'])
def create_order():
    total = request.json.get('total')
    
    # Create an order with PayPal
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}',
    }

    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": str(total)
            }
        }]
    }

    response = requests.post('https://api-m.sandbox.paypal.com/v2/checkout/orders', headers=headers, json=order_data)
    return jsonify(response.json())

@app.route('/capture-order', methods=['POST'])
def capture_order():
    order_id = request.json.get('orderID')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}',
    }

    response = requests.post(f'https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture', headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
