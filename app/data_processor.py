import requests
import logging
import pandas as pd  
import plotly.express as px  
from datetime import datetime
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
            logger.debug(f"Response data: {data}") 
            
            if isinstance(data, dict):
                if 'listing' in data:
                    return data['listing']
                return data  
            
            logger.warning(f"Unexpected data format: {data}")
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


def fetch_all_listings(max_listings=10000):
    """Fetch all listings from the /annonces endpoint, handling pagination."""
    url = f"{Config.FASTAPI_URL}/annonces"
    all_annonces = []
    skip = 0
    limit = 100
    total = None

    while True:
        params = {"skip": skip, "limit": limit}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                annonces = data.get('annonces', [])
                all_annonces.extend(annonces)
                total = data.get('total', 0)
                logger.debug(f"Fetched {len(annonces)} listings, total so far: {len(all_annonces)}")
                if len(all_annonces) >= total or not annonces or len(all_annonces) >= max_listings:
                    break
                skip += limit
            else:
                logger.error(f"Error fetching listings: Received status code {response.status_code}")
                return []
        except Exception as e:
            logger.error(f"Error fetching all listings: {e}")
            return []
    
    # Log the date range of the fetched listings
    if all_annonces:
        dates = [datetime.fromisoformat(annonce['metadata']['publishedOn'].replace("Z", "+00:00")) 
                 for annonce in all_annonces if 'metadata' in annonce and 'publishedOn' in annonce['metadata']]
        if dates:
            min_date = min(dates).strftime('%Y-%m-%d')
            max_date = max(dates).strftime('%Y-%m-%d')
            logger.info(f"Fetched listings date range: {min_date} to {max_date}")
        else:
            logger.warning("No valid dates found in fetched listings")
    
    logger.info(f"Total listings fetched: {len(all_annonces)}")
    return all_annonces

def process_average_prices_over_time(annonces):
    """Process listings to compute average prices by month, split by Rent and Sale."""
    if not annonces:
        logger.warning("No listings data for average price processing")
        return pd.DataFrame()

    # Create DataFrame
    df = pd.DataFrame(annonces)
    if 'price' not in df.columns or 'metadata' not in df.columns:
        logger.error("Missing required fields (price or metadata) in listings data")
        return pd.DataFrame()

    # Extract publishedOn and producttype from metadata, filter invalid prices
    df['publishedOn'] = df['metadata'].apply(lambda x: x.get('publishedOn', None))
    df['producttype'] = df['metadata'].apply(lambda x: x.get('producttype', None))
    df = df.dropna(subset=['publishedOn', 'price', 'producttype'])
    df = df[df['price'].apply(lambda x: isinstance(x, (int, float)) and x > 0)]  # Ensure price is positive

    # Convert producttype to labels
    df['type_label'] = df['producttype'].map({1: 'Sale', 0: 'Rent'}).fillna(df['producttype'].astype(str).str.capitalize())

    # Convert publishedOn to datetime and extract year-month
    try:
        df['date'] = pd.to_datetime(df['publishedOn'])
        df['year_month'] = df['date'].dt.to_period('M').astype(str)
    except Exception as e:
        logger.error(f"Error parsing dates: {e}")
        return pd.DataFrame()

    # Compute average price per month, split by type
    avg_prices = df.groupby(['year_month', 'type_label'])['price'].mean().reset_index()
    logger.debug(f"Average prices DataFrame (split by type):\n{avg_prices}")
    return avg_prices

def process_monthly_distribution_by_type(annonces):
    """Process listings to compute monthly distribution by property type."""
    if not annonces:
        logger.warning("No listings data for distribution processing")
        return pd.DataFrame()

    # Create DataFrame
    df = pd.DataFrame(annonces)
    if 'metadata' not in df.columns:
        logger.error("Missing metadata field in listings data")
        return pd.DataFrame()

    # Extract producttype and publishedOn from metadata
    df['producttype'] = df['metadata'].apply(lambda x: x.get('producttype', None))
    df['publishedOn'] = df['metadata'].apply(lambda x: x.get('publishedOn', None))
    df = df.dropna(subset=['publishedOn', 'producttype'])

    # Convert producttype to labels
    df['type_label'] = df['producttype'].map({1: 'Sale', 0: 'Rent'}).fillna(df['producttype'].astype(str).str.capitalize())

    # Convert publishedOn to datetime and extract year-month
    try:
        df['date'] = pd.to_datetime(df['publishedOn'])
        df['year_month'] = df['date'].dt.to_period('M').astype(str)
    except Exception as e:
        logger.error(f"Error parsing dates: {e}")
        return pd.DataFrame()

    # Pivot to get counts by month and type
    pivot = df.pivot_table(index='year_month', columns='type_label', aggfunc='size', fill_value=0).reset_index()
    logger.debug(f"Monthly distribution DataFrame:\n{pivot}")
    return pivot
