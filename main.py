import csv
import time
import requests

from datetime import datetime
from bitvavo_rest_client import BitvavoRestClient, APIKEY, APISECRET, bitvavo_api

def get_historical_data(symbol, time_window, start_time, end_time, APIKEY, APISECRET):
    # Create an instance of BitvavoRestClient
    bitvavo_rest_client = BitvavoRestClient(APIKEY, APISECRET, bitvavo_api)

    if not APIKEY:
        print("API key is missing. Please provide your Bitvavo API key.")
        return

    while start_time < end_time:
        try:
            timestamp = int(time.time() * 1000)
            method = 'GET'
            url = f'/{symbol}/candles?interval={time_window}&end={int(end_time.timestamp() * 1000)}'
            body = {}
            # Call the create_signature method on the BitvavoRestClient instance
            signature = bitvavo_rest_client.create_signature(timestamp, method, url, body)
            headers = {
                'Bitvavo-Access-Key': APIKEY,
                'Bitvavo-Access-Signature': signature,
                'Bitvavo-Access-Timestamp': str(timestamp),
                'Bitvavo-Access-Window': '10000',
            }
            response = requests.request(method=method, url='https://api.bitvavo.com/v2' + url, headers=headers, json=body)
            data = response.json()
            if data:
                # Update end_time to the timestamp of the last retrieved data
                end_time = datetime.fromtimestamp(int(data[-1][0]) / 1000)
                formatted_data = [[datetime.fromtimestamp(int(candle[0]) / 1000).strftime('%d-%m-%Y %H:%M')] + candle[1:] for candle in data]
                with open(f'{symbol}_historical_data_{time_window}.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    # Check if file is empty
                    if f.tell() == 0:
                        # Write headers
                        writer.writerow(['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                    # Write data
                    writer.writerows(formatted_data)
                    print(f"Data successfully written to {symbol}_historical_data_{time_window}.csv")
            else:
                print("No more data to retrieve.")
                break  # No more data to retrieve
        except Exception as e:  # catch all exceptions
            if '429' in str(e):  # rate limit exceeded
                print("Rate limit exceeded. Pausing for 1 minute...")
                time.sleep(60)  # pause for 1 minute
            else:
                raise

start_time = datetime(2021, 1, 1)
end_time = datetime.now()

get_historical_data('ETH-EUR', '5m', start_time, end_time, APIKEY, APISECRET)