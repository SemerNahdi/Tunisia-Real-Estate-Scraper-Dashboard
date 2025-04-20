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
            return response.json()
        return {}
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return {}

def load_new_listings(url):
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        logger.error(f"Error fetching new listings: {e}")
        return {}

def load_statistics(url):
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        logger.error(f"Error fetching statistics: {e}")
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
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        logger.error(f"Error fetching filtered listings: {e}")
        return {}

def fetch_listing_details(listing_id):
    url = f"{Config.FASTAPI_URL}/annonces/{listing_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('listing', data) if isinstance(data, dict) else None
        return None
    except Exception as e:
        logger.error(f"Error fetching listing {listing_id}: {e}")
        return None

def clean_data(data):
    return data

def fetch_listings_by_date(start_date, end_date, producttype=None, skip=0, limit=100):
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
        return response.json() if response.status_code == 200 else {}
    except Exception as e:
        logger.error(f"Error fetching listings by date: {e}")
        return {}

def fetch_governorates_delegations():
    url = f"{Config.FASTAPI_URL}/governorates-with-delegations"
    try:
        response = requests.get(url)
        return response.json().get('governorates_with_delegations', []) if response.status_code == 200 else []
    except Exception as e:
        logger.error(f"Error fetching governorates and delegations: {e}")
        return []

def fetch_all_listings(max_listings=10000):
    url = f"{Config.FASTAPI_URL}/annonces"
    all_annonces = []
    skip = 0
    limit = 100

    while True:
        try:
            response = requests.get(url, params={"skip": skip, "limit": limit})
            if response.status_code == 200:
                data = response.json()
                annonces = data.get('annonces', [])
                all_annonces.extend(annonces)
                if len(all_annonces) >= data.get('total', 0) or not annonces or len(all_annonces) >= max_listings:
                    break
                skip += limit
            else:
                return []
        except Exception:
            return []
    
    return all_annonces

def process_average_prices_over_time(annonces):
    if not annonces:
        return pd.DataFrame()

    df = pd.DataFrame(annonces)
    if 'price' not in df.columns or 'metadata' not in df.columns:
        return pd.DataFrame()

    df['publishedOn'] = df['metadata'].apply(lambda x: x.get('publishedOn', None))
    df['producttype'] = df['metadata'].apply(lambda x: x.get('producttype', None))
    df = df.dropna(subset=['publishedOn', 'price', 'producttype'])
    df = df[df['price'].apply(lambda x: isinstance(x, (int, float)) and x > 0)]

    df['type_label'] = df['producttype'].map({1: 'Sale', 0: 'Rent'}).fillna(df['producttype'].astype(str).str.capitalize())

    try:
        df['date'] = pd.to_datetime(df['publishedOn'])
        df['year_month'] = df['date'].dt.to_period('M').astype(str)
    except Exception:
        return pd.DataFrame()

    return df.groupby(['year_month', 'type_label'])['price'].mean().reset_index()

def process_monthly_distribution_by_type(annonces):
    if not annonces:
        return pd.DataFrame()

    df = pd.DataFrame(annonces)
    if 'metadata' not in df.columns:
        return pd.DataFrame()

    df['producttype'] = df['metadata'].apply(lambda x: x.get('producttype', None))
    df['publishedOn'] = df['metadata'].apply(lambda x: x.get('publishedOn', None))
    df = df.dropna(subset=['publishedOn', 'producttype'])

    df['type_label'] = df['producttype'].map({1: 'Sale', 0: 'Rent'}).fillna(df['producttype'].astype(str).str.capitalize())

    try:
        df['date'] = pd.to_datetime(df['publishedOn'])
        df['year_month'] = df['date'].dt.to_period('M').astype(str)
    except Exception:
        return pd.DataFrame()

    # Pivot to get counts by month and type
    pivot = df.pivot_table(index='year_month', columns='type_label', aggfunc='size', fill_value=0).reset_index()
    logger.debug(f"Monthly distribution DataFrame:\n{pivot}")
    return pivot
