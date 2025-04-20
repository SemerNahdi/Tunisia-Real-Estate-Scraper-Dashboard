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
    """Fetch details for a single listing from the FastAPI endpoint."""
    url = f"{Config.FASTAPI_URL}/annonces/{listing_id}"
    logger.info(f"Fetching listing details from URL: {url}")
    try:
        response = requests.get(url)
        logger.debug(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            logger.debug(f"Response data keys: {list(data.keys())}")
            
            listing = data.get('listing')
            if listing:
                logger.info(f"Successfully fetched listing {listing_id} with title: {listing.get('title', 'N/A')}")
                return listing
            else:
                logger.warning(f"No listing data found for listing_id: {listing_id}")
                return None
        
        elif response.status_code == 404:
            logger.warning(f"Listing not found for listing_id: {listing_id}")
            return None
        
        else:
            logger.error(f"Unexpected status code {response.status_code} for listing_id: {listing_id}")
            return None
    
    except Exception as e:
        logger.error(f"Exception while fetching listing {listing_id}: {str(e)}")
        return None

def clean_data(data):
    """Clean and preprocess the data if needed."""
    return data


def fetch_listings_by_date(start_date, end_date, producttype=None, skip=0, limit=100):
    """Fetch listings within a date range."""
    url = f"{Config.FASTAPI_URL}/annonces/date"
    params = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "skip": skip,
        "limit": limit
    }
    if producttype is not None:
        params["producttype"] = producttype

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            logger.debug(f"Successfully fetched {len(data.get('annonces', []))} listings by date")
            return data
        else:
            logger.error(f"Error: Received status code {response.status_code}")
            return {}
    except Exception as e:
        logger.error(f"Error fetching listings by date: {e}")
        return {}

def fetch_governorates_delegations():
    """Fetch the list of governorates and their delegations."""
    url = f"{Config.FASTAPI_URL}/governorates-with-delegations"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            logger.debug("Successfully fetched governorates and delegations")
            return data.get('governorates_with_delegations', [])
        else:
            logger.error(f"Error: Received status code {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Error fetching governorates and delegations: {e}")
        return []
    