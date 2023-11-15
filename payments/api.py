import requests
from datetime import datetime, timedelta, timezone

from .models import PaypalModel

# get access token
def new_access_token(url, client_id, secret):

    # PayPal API URL
    paypal_url = f"{url}/v1/oauth2/token"

    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    payload = "grant_type=client_credentials"

    try:
        response = requests.post(paypal_url, auth=(client_id, secret), data=payload, headers=headers)

        if response.status_code == 200:
            data_json = response.json()
            return data_json
        else:
            error_message = response.json()
            return {"error": f"Failed to create PayPal payment. Status Code: {response.status_code}. Error: {error_message}"}
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect to PayPal API. {str(e)}"}

# Function to retrieve the PayPalModel from the database
def get_paypal_from_db():
    try:
        return PaypalModel.objects.all()[0]
    except IndexError:
        return None

# Function to update the PayPalModel with new data
def update_paypal_model(paypal, new_requests):
    paypal.app_id = new_requests['app_id']
    paypal.access_token = new_requests['access_token']
    paypal.expires_in = new_requests['expires_in']
    paypal.save()

# Function to check if a given time (now) is later than another time (expires)
def is_expired(now, expires):
    return now >= expires

# Main function to get the PayPal access token
def get_access_token(url, client_id, secret):
    now = datetime.now(timezone.utc)  # Make the current date and time timezone-aware in UTC
    paypal = get_paypal_from_db()

    # Check if the stored PayPal data is not available or if the access token has expired
    if not paypal or is_expired(now, paypal.updated_at + timedelta(seconds=paypal.expires_in)):
        new_requests = new_access_token(url, client_id, secret)

        # If new access token is obtained
        if new_requests:
            # If PayPal data is already stored, update it; otherwise, create a new entry
            if paypal:
                update_paypal_model(paypal, new_requests)
            else:
                paypal = PaypalModel.objects.create(
                    app_id=new_requests['app_id'],
                    access_token=new_requests['access_token'],
                    expires_in=new_requests['expires_in']
                )
        else:
            return None

    # Return the access token from the stored or updated PayPal data
    return paypal.access_token

# generate new payment link
def create_paypal_payment(url, access_token, price):
    # PayPal API URL
    paypal_url = f"{url}/v2/checkout/orders"

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
                    "value": f"{price}"
                }
            }
        ],
        'application_context': {
            "brand_name": "myApp.com",
            "landing_page": "NO_PREFERENCE",
            "user_action": "PAY_NOW",
            "return_url": "http://localhost:8000/payments/success/",
            "cancel_url": "http://localhost:8000/payments/cancelled/",
            "shipping_preference": "NO_SHIPPING",
        }
    }

    try:
        response = requests.post(paypal_url, json=payload, headers=headers)

        if response.status_code == 201:
            data_json = response.json()
            return data_json['links'][1]['href']
        else:
            error_message = response.json()
            return {"error": f"Failed to create PayPal payment. Status Code: {response.status_code}. Error: {error_message}"}
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to connect to PayPal API. {str(e)}"}