from dash import html, dcc
import dash_bootstrap_components as dbc
from .graphs import (
    create_pie_chart,
    create_delegation_chart, 
    create_publisher_chart, 
    create_type_chart
)
import pandas as pd
import requests
from .config import Config
from .utils import logger

def create_layout(statistics_data, new_listings_data):
    if not isinstance(statistics_data, dict) or not isinstance(new_listings_data, dict):
        return html.Div("Error: Data is not in the expected format.")
    
    total_listings = statistics_data.get('total_listings', 0)
    governorate_stats = {item['_id']: item['count'] for item in statistics_data.get('governorate_stats', [])}
    type_stats = {item['_id']: item['count'] for item in statistics_data.get('type_stats', [])}
    avg_price_sale = round(statistics_data.get('avg_price_sale', 0), 2)
    avg_price_rent = round(statistics_data.get('avg_price_rent', 0), 2)
    publisher_stats = {item['_id']: item['count'] for item in statistics_data.get('publisher_stats', [])}
    delegation_data = statistics_data.get('delegation_by_governorate', [])
    
    total_shops = sum(count for is_shop, count in publisher_stats.items() if is_shop)
    total_individuals = sum(count for is_shop, count in publisher_stats.items() if not is_shop)
    shop_percentage = round((total_shops / total_listings) * 100, 1) if total_listings > 0 else 0
    
    new_annonces = new_listings_data.get('new_annonces', [])
    new_count = new_listings_data.get('count', 0)
    
    return dbc.Container([
        html.H1("Tunisian Real Estate Dashboard", className="text-center my-4"),
        
        # Key Metrics Cards
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    html.H4("Total Listings", className="card-title"),
                    html.H2(f"{total_listings:,}", className="card-text")
                ], body=True, className="metric-card"),
                md=3
            ),
            dbc.Col(
                dbc.Card([
                    html.H4("Avg Sale Price", className="card-title"),
                    html.H2(f"{avg_price_sale:,.2f} TND", className="card-text")
                ], body=True, className="metric-card"),
                md=3
            ),
            dbc.Col(
                dbc.Card([
                    html.H4("Avg Rent Price", className="card-title"),
                    html.H2(f"{avg_price_rent:,.2f} TND", className="card-text")
                ], body=True, className="metric-card"),
                md=3
            ),
            dbc.Col(
                dbc.Card([
                    html.H4("Shop Listings", className="card-title"),
                    html.H2(f"{shop_percentage}%", className="card-text")
                ], body=True, className="metric-card"),
                md=3
            )
        ], className="mb-5"),
        
        # Bento Grid Layout
        dbc.Row([
            # Left Column
            dbc.Col([
                # Governorate Distribution Chart
                dbc.Card([
                    dcc.Graph(
                        id='governorate-pie',
                        figure=create_pie_chart(governorate_stats, "Listings by Governorate")
                    )
                ], body=True, className="mb-4"),
                
                # Publisher Type Distribution
                dbc.Card([
                    dcc.Graph(
                        id='publisher-chart',
                        figure=create_publisher_chart(publisher_stats)
                    )
                ], body=True)
            ], md=6),
            
            # Right Column
            dbc.Col([
                # Type Distribution Chart (Donut)
                dbc.Card([
                    dcc.Graph(
                        id='type-chart',
                        figure=create_type_chart(type_stats)
                    )
                ], body=True, className="mb-4"),
                
                # Top Delegations Chart
                dbc.Card([
                    dcc.Graph(
                        id='delegation-chart',
                        figure=create_delegation_chart(delegation_data)
                    )
                ], body=True)
            ], md=6)
        ]),
        
        # Navigation Buttons in Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Button(
                            "View New Listings",
                            href="/new-listings",
                            color="primary",
                            className="w-100 mt-2"
                        )
                    ], className="p-0")
                ], className="mb-4 metric-card")
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Button(
                            "Filter by Price",
                            href="/price-filter",
                            color="primary",
                            className="w-100 mt-2"
                        )
                    ], className="p-0")
                ], className="mb-4 metric-card")
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Button(
                            "Back to Dashboard",
                            href="/",
                            color="secondary",
                            className="w-100 mt-2"
                        )
                    ], className="p-0")
                ], className="mb-4 metric-card")
            ], md=4)
        ])
    ], fluid=True, className="dashboard-container")

def create_new_listings_layout(new_listings_data):
    new_annonces = new_listings_data.get('new_annonces', [])
    new_count = new_listings_data.get('count', 0)
    
    if not new_annonces:
        return dbc.Container([
            html.H1("New Listings", className="text-center my-4"),
            html.H4(f"Total New Listings: {new_count}", className="text-center my-2"),
            html.P("No new listings found.", className="text-center my-2"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Button(
                                "Back to Dashboard",
                                href="/",
                                color="secondary",
                                className="w-100 mt-2"
                            )
                        ], className="p-0")
                    ], className="mb-4 metric-card")
                ], md=12, className="text-center")
            ])
        ], fluid=True, className="dashboard-container")
    
    listings_cards = [
        dbc.Card([
            dbc.CardHeader(f"Listing ID: {annonce.get('id', 'N/A')}"),
            dbc.CardBody([
                html.H5(annonce.get('title', 'N/A'), className="card-title"),
                html.P(f"Price: {annonce.get('price', 'N/A')} TND", className="card-text"),
                html.P(f"Location: {annonce.get('location', {}).get('governorate', 'N/A')}, {annonce.get('location', {}).get('delegation', 'N/A')}", className="card-text"),
                html.P(f"Description: {annonce.get('description', 'N/A')[:100]}...", className="card-text"),
                html.P(f"Published On: {annonce.get('metadata', {}).get('publishedOn', 'N/A')}", className="card-text")
            ])
        ], className="mb-4 rounded-card") for annonce in new_annonces
    ]
    
    return dbc.Container([
        html.H1("New Listings", className="text-center my-4"),
        html.H4(f"Total New Listings: {new_count}", className="text-center my-2"),
        
        # Back to Dashboard Button in Card
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Button(
                            "Back to Dashboard",
                            href="/",
                            color="secondary",
                            className="w-100 mt-2"
                        )
                    ], className="p-0")
                ], className="mb-4 metric-card")
            ], md=12, className="text-center")
        ]),
        
        dbc.Row(listings_cards, className="justify-content-center"),
    ], fluid=True, className="dashboard-container")

def create_price_filter_layout():
    return dbc.Container([
        html.H1("Filter Listings by Price", className="text-center my-4"),
        
        # Back to Dashboard Button in Card
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Button(
                            "Back to Dashboard",
                            href="/",
                            color="secondary",
                            className="w-100 mt-2"
                        )
                    ], className="p-0")
                ], className="mb-4 metric-card")
            ], md=12, className="text-center")
        ]),
        
        # Price Range Inputs
        dbc.Row([
            dbc.Col([
                dbc.Label("Minimum Price (TND)", className="mb-2"),
                dbc.Input(
                    id='min-price-input',
                    type='number',
                    value=0,
                    min=0,
                    className="mb-4"
                )
            ], md=6),
            dbc.Col([
                dbc.Label("Maximum Price (TND)", className="mb-2"),
                dbc.Input(
                    id='max-price-input',
                    type='number',
                    value=1_000_000,
                    min=0,
                    className="mb-4"
                )
            ], md=6)
        ]),
        
        # Product Type Selector
        dbc.Row([
            dbc.Col([
                dbc.Label("Product Type", className="mb-2"),
                dbc.RadioItems(
                    id='product-type-selector',
                    options=[
                        {"label": "Sale", "value": 1},
                        {"label": "Rent", "value": 0},
                        {"label": "Both", "value": None}
                    ],
                    value=None,
                    inline=True,
                    className="mb-4"
                )
            ], md=12)
        ]),
        
        # Listings Display
        dbc.Row([
            dbc.Col([
                html.Div(id='price-filter-results', className="mt-4")
            ], md=12)
        ])
    ], fluid=True, className="dashboard-container")