# Tunisia Real Estate Dashboard

A modern dashboard for visualizing Tunisian real estate market data, built with Dash and Plotly.

## Features

- Interactive visualizations of real estate market data
- Key metrics display (Total Listings, Average Prices, Shop Listings)
- Distribution charts for:
  - Listings by Governorate
  - Sale vs. Rent distribution
  - Publisher types (Shop vs. Individual)
  - Top delegations by number of listings
- Price distribution analysis
- Modern, responsive design with hover effects

## Data Structure

The dashboard processes real estate listings with the following key attributes:

- **producttype**:
  - 1 for sales
  - 0 for rentals
- Location data (governorate, delegation)
- Price information
- Publisher type (shop/individual)

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the dashboard:

```bash
python app/main.py
```

3. Access the dashboard at `http://localhost:8050`

## Technologies Used

- Python
- Dash
- Plotly
- Pandas
- MongoDB (for data storage)
