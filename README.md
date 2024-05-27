# Crypto Dataset Generator

This Python script fetches historical data for a specified trading pair from the Bitvavo API and saves it to a CSV file.

## Requirements
- Python 3.6 or higher
- `python_bitvavo_api` package
- `requests` package
- `python-dotenv` package

## Setup
1. Clone this repository to your local machine.
2. Install the required Python packages using pip.
```
pip install python_bitvavo_api requests python-dotenv
```
3. Create a `.env` file in the root directory of the project and add your Bitvavo API key and secret.
```
APIKEY=your_bitvavo_api_key
APISECRET=your_bitvavo_api_secret
```

## Usage
1. Open `main.py` in your preferred text editor.
2. Set the `start_time` and `end_time` variables to the desired time range.
3. Call the `get_historical_data` function with the desired trading pair and time window.
```
get_historical_data('BTC-EUR', '1h', start_time, end_time, APIKEY, APISECRET)
```
4. Run the script.
```
python main.py
```

The historical data will be saved to a CSV file in the format `{symbol}_historical_data_{time_window}.csv`.

## Functionality
The `get_historical_data` function fetches historical data for the specified trading pair at the specified time window, starting from `start_time` up to `end_time`. It makes a GET request to the Bitvavo API for each time window and saves the data to a CSV file. If the rate limit is exceeded, it pauses for 1 minute before continuing. If there's an error other than rate limit exceeded, it raises an exception and stops executing.

**Note:** Please ensure that you have the necessary permissions and rate limits on your Bitvavo API key to fetch historical data.