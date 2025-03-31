import pandas as pd
import requests

# data_processor.py

import requests

def load_data():
    try:
        response = requests.get("http://127.0.0.1:8000/statistics")
        if response.status_code == 200:
            data = response.json()
            # print(data)  # Debug print to check the structure
            return data
        else:
            print(f"Error: Received status code {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {}



def clean_data(data):
    """Clean and preprocess the data if needed."""
    # Any data cleaning (e.g., handle missing values)
    return data
