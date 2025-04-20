import requests
import logging
from .config import Config

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

def fetch_filtered_listings(min_price, max_price, producttype):
    url = f"{Config.FASTAPI_URL}/annonces/price"
    params = {
        "min_price": min_price,
        "max_price": max_price,
        "producttype": producttype,
        "skip": 0,
        "limit": 100  
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            logger.debug("Filtered listings fetched successfully.")
            return data
        else:
            logger.error(f"Error: Received status code {response.status_code}")
            return {}
    except Exception as e:
        logger.error(f"Error fetching filtered listings: {e}")
        return {}

def fetch_listing_details(listing_id):
    """Fetch details for a single listing."""
    url = f"{Config.FASTAPI_URL}/annonces/{listing_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            logger.debug(f"Listing details fetched successfully for listing_id: {listing_id}")
            print(data)
            return data
        elif response.status_code == 404:
            logger.warning(f"Listing not found for listing_id: {listing_id}")
            return None
        else:
            logger.error(f"Error: Received status code {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error fetching listing details for listing_id {listing_id}: {e}")
        return None

      
def clean_data(data):
    """Clean and preprocess the data if needed."""
    # Any data cleaning (e.g., handle missing values)
    return data