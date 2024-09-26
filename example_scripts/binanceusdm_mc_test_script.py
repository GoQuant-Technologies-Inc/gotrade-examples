import requests
import sys
import websocket


def login():
    # Login endpoint
    url = "http://localhost:8001/gotrade/v2/binanceusdm/credentials"
    headers = {
        "Content-Type": "application/json",
        "Client-API-Key": "94fbcf0815d0ec8b292d61e805b7f83b"
    }
    data = {
    "exchange":"BINANCEUSDM",
    "name":"account_name",
    "key":"binanceusdm_api_key",
    "secret":"binanceusdm_secret",
    "authenticate":True,
    "passphrase":"binanceusdm_passphrase",
    "mode": ""

 
}


    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Login successful.")
    else:
        print("Failed to login:", response.status_code, response.text)
        sys.exit(1)

def get_credentials():
    # Get credentials endpoint
    url = "http://localhost:8001/gotrade/v2/binanceusdm/credentials"
    headers = {
        "Content-Type": "application/json",
        "Client-API-Key": "94fbcf0815d0ec8b292d61e805b7f83b"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Parse the response JSON
        credentials_response = response.json()
        print("Credentials Response:", credentials_response)

        # Access the 'data' key, which contains the list of credentials
        credentials = credentials_response.get("data", [])

        # Find the first binanceusdm credential
        for credential in credentials:
            # Ensure each item is a dictionary
            if isinstance(credential, dict) and 'account_name' in credential and 'credential_id' in credential:
                # Use the first valid binanceusdm credential
                credential_id = credential["credential_id"]
                account_name = credential["account_name"]
                print(f"Account Name: {account_name}")
                print(f"Credential ID: {credential_id}")
                return credential_id, account_name
        
        print("No valid binanceusdm credentials found.")
        sys.exit(1)
    else:
        print("Failed to retrieve credentials:", response.status_code, response.text)
        sys.exit(1)

def place_orders(credential_id, account_name):
    # Place market orders
    url = "http://localhost:8001/gotrade/v2/binanceusdm/order/place"
    headers = {
        "Content-Type": "application/json",
        "Client-API-Key": "94fbcf0815d0ec8b292d61e805b7f83b"
    }
    print("Placing market algo")
    data = {
    "credential_id": credential_id,
    "algorithm_type": "PLACE", 
    "exchange": "BINANCEUSDM", 
    "account": account_name, 
    "symbol": "EOSUSDT", 
    "side": "BUY", 
    "quantity": 15.0, 
    "price": 0,
    "type": "market" 
}

    for i in range(10):
        print(f"Placing order {i + 1} of 10")
        response = requests.post(url, headers=headers, json=data)
        print(response.status_code)
        print(response.json())

    # Place a TWAP algo to sell 10 shares of EOSUSDT on binanceusdm over 10 seconds
    print("Placing TWAP algo")
    data = {
        "credential_id": credential_id,
        "algorithm_type": "PLACE",
        "exchange": "BINANCEUSDM",
        "account": account_name,
        "symbol": "EOSUSDT",
        "quantity": 10,
        "side": "SELL",
        "type": "twap",
        "duration": 10,
        "interval": 5,
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    print(response.json())

def get_holdings(credential_id):
    # Endpoint to get holdings
    url = f"http://localhost:8001/gotrade/v2/binanceusdm/{credential_id}/holdings"
    headers = {
        "Client-API-Key": "94fbcf0815d0ec8b292d61e805b7f83b"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Holdings Response:", response.json())
    else:
        print("Failed to retrieve holdings:", response.status_code, response.text)


def on_message(ws, message):
    print("Received message:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed.")

def on_open(ws):
    print("WebSocket connection opened.")

def setup_websocket(credential_id):
    ws_url = f"ws://localhost:8001/ws/gotrade/v2/binanceusdm/{credential_id}/orders"
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

def main():
    # task 1: Login
    login()

    # task 2: Get credentials and account name from the credentials endpoint
    credential_id, account_name = get_credentials()

    # task 3: Place orders using the credential ID and account name
    place_orders(credential_id, account_name)

    # task 4 get the holdings in the account
    get_holdings(credential_id)

    # task 5: Set up WebSocket to print data
    setup_websocket(credential_id)

if __name__ == "__main__":
    main()
