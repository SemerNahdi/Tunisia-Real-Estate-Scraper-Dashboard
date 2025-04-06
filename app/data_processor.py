import requests
import logging

logger = logging.getLogger(__name__)

def load_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            logger.debug("Data fetched successfully.")
            return data
        else:
            logger.error(f"Error: Received status code {response.status_code}")
            return {}
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return {}

def load_new_listings(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            logger.debug("New listings fetched successfully.")
            # print(data)
            return data
        else:
            logger.error(f"Error: Received status code {response.status_code}")
            return {}
    except Exception as e:
        logger.error(f"Error fetching new listings: {e}")
        return {}

def load_statistics(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            logger.debug("Statistics data fetched successfully.")
            
            return data
        else:
            logger.error(f"Error: Received status code {response.status_code}")
            return {}
    except Exception as e:
        logger.error(f"Error fetching statistics data: {e}")
        return {}

def clean_data(data):
    """Clean and preprocess the data if needed."""
    # Any data cleaning (e.g., handle missing values)
    return data
