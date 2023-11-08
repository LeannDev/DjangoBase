import requests

# generate new payment link
def create_paypal_payment(access_token):
    # PayPal API URL
    paypal_url = "https://api.sandbox.paypal.com/v2/checkout/orders"  # Sandbox URL

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "reference_id": "ID15465464",
                "amount": {
                    "currency_code": "USD",
                    "value": "100"
                }
            }
        ],
        'application_context': {
            "brand_name": "myApp.com",
            "landing_page": "NO_PREFERENCE",
            "user_action": "PAY_NOW",
            "return_url": "http://localhost:8000/execute-payment",
            "cancel_url": "http://localhost:8000/cancel-payment",
            "shipping_preference": "NO_SHIPPING",
        }
    }

    try:
        response = requests.post(paypal_url, json=payload, headers=headers)

        if response.status_code == 201:
            data_json = response.json()
            return data_json
        else:
            error_message = response.json()
            return {"error": f"Failed to create PayPal payment. Status Code: {response.status_code}. Error: {error_message}"}
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect to PayPal API. {str(e)}"}