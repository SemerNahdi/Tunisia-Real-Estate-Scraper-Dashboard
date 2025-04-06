# layouts.py
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
        html.H1("🏠 Tunisian Real Estate Dashboard", className="emoji-header text-center my-4 p-3"),
        
        # Key Metrics Cards
        dbc.Row([
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.H4("📊 Total Listings", className="card-title mb-2"),
                html.H2(f"{total_listings:,}", className="metric-value text-pastel-blue")
            ])
        ], className="metric-card pastel-border-blue hover-scale", color="light"),
        md=3, className="mb-4"
    ),
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.H4("💰 Avg Sale Price", className="card-title mb-2"),
                html.H2(f"{avg_price_sale:,.2f} TND", className="metric-value text-pastel-mint")
            ])
        ], className="metric-card pastel-border-mint hover-scale", color="light"),
        md=3, className="mb-4"
    ),
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.H4("🏘️ Avg Rent Price", className="card-title mb-2"),
                html.H2(f"{avg_price_rent:,.2f} TND", className="metric-value text-pastel-peach")
            ])
        ], className="metric-card pastel-border-peach hover-scale", color="light"),
        md=3, className="mb-4"
    ),
    dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.H4("🏪 Shop Listings", className="card-title mb-2"),
                html.H2(f"{shop_percentage}%", className="metric-value text-pastel-pink")
            ])
        ], className="metric-card pastel-border-pink hover-scale", color="light"),
        md=3, className="mb-4"
    )
], className="mb-5 g-3"),  # Reduced gutter to g-3 for tighter spacing
        # Charts Grid
        dbc.Row([
            # Left Column
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📍 Listings by Governorate", className="chart-header"),
                    dbc.CardBody([
                        dcc.Graph(
                            id='governorate-pie',
                            figure=create_pie_chart(governorate_stats, "Listings by Governorate")
                        )
                    ])
                ], className="chart-card mb-4"),
                
                # Publisher Type Chart
                dbc.Card([
                    dbc.CardHeader("🏢 Publisher Types", className="chart-header"),
                    dbc.CardBody([
                        dcc.Graph(
                            id='publisher-chart',
                            figure=create_publisher_chart(publisher_stats)
                        )
                    ])
                ], className="chart-card")
            ], md=6),
            
            # Right Column
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🏛️ Property Types", className="chart-header"),
                    dbc.CardBody([
                        dcc.Graph(
                            id='type-chart',
                            figure=create_type_chart(type_stats)
                        )
                    ])
                ], className="chart-card mb-4"),
                
                dbc.Card([
                    dbc.CardHeader("🗺️ Top Delegations", className="chart-header"),
                    dbc.CardBody([
                        dcc.Graph(
                            id='delegation-chart',
                            figure=create_delegation_chart(delegation_data)
                        )
                    ])
                ], className="chart-card")
            ], md=6)
        ], className="g-4"),
        
        # Navigation Buttons
        dbc.Row([
            dbc.Col(
                dbc.Button(
                    "✨ View New Listings",
                    href="/new-listings",
                    color="primary",
                    className="nav-btn hover-scale py-3"
                ), md=4, className="mb-3"
            ),
            dbc.Col(
                dbc.Button(
                    "🔍 Filter by Price",
                    href="/price-filter",
                    color="secondary",
                    className="nav-btn hover-scale py-3"
                ), md=4, className="mb-3"
            ),
            dbc.Col(
                dbc.Button(
                    "🏡 Back to Dashboard",
                    href="/",
                    color="light",
                    className="nav-btn hover-scale py-3"
                ), md=4, className="mb-3"
            )
        ], className="g-4 mt-4")
    ], fluid=True, className="dashboard-container p-4")
def create_new_listings_layout(new_listings_data):
    new_annonces = new_listings_data.get('new_annonces', [])
    new_count = new_listings_data.get('count', 0)
    
    if not new_annonces:
        return dbc.Container([
            # Header Row
            dbc.Row([
                dbc.Col(
                    dbc.Button(
                        "← Dashboard",
                        href="/",
                        color="light",
                        className="back-btn py-2",
                    ), 
                    md=2, className="ps-4 pt-3"
                ),
                dbc.Col(
                    html.H1("✨ New Listings", className="emoji-header mb-0 text-center"), 
                    md=8, className="pt-3"
                ),
                dbc.Col(md=2)  # Empty column for spacing
            ], className="align-items-center mb-4"),
            
            # Content
            html.H4(f"📌 Total New Listings: {new_count}", className="text-center my-2"),
            html.P("😔 No new listings found.", className="text-center my-2"),
        ], fluid=True, className="dashboard-container p-4")
    
    listings_cards = [
        dbc.Card([
            dbc.CardHeader(f"🏷️ Listing ID: {annonce.get('id', 'N/A')}", className="listing-header"),
            dbc.CardBody([
                html.H5(annonce.get('title', 'N/A'), className="card-title text-primary"),
                html.P(f"💰 Price: {annonce.get('price', 'N/A')} TND", className="card-text price-highlight"),
                html.P(f"📍 Location: {annonce.get('location', {}).get('governorate', 'N/A')}, "
                      f"{annonce.get('location', {}).get('delegation', 'N/A')}", className="card-text"),
                html.P(f"📝 Description: {annonce.get('description', 'N/A')[:100]}...", className="card-text"),
                html.P(f"📅 Published On: {annonce.get('metadata', {}).get('publishedOn', 'N/A')}", 
                      className="card-text text-muted")
            ])
        ], className="mb-4 listing-card hover-scale") for annonce in new_annonces
    ]
    
    return dbc.Container([
        # Header Row
        dbc.Row([
            dbc.Col(
                dbc.Button(
                    "← Dashboard",
                    href="/",
                    color="light",
                    className="back-btn py-2",
                ), 
                md=2, className="ps-4 pt-3"
            ),
            dbc.Col(
                html.H1("✨ New Listings", className="emoji-header mb-0 text-center"), 
                md=8, className="pt-3"
            ),
            dbc.Col(md=2)  # Empty column for spacing
        ], className="align-items-center mb-4"),
        
        # Content
        html.H4(f"📌 Total New Listings: {new_count}", className="text-center my-2"),
        dbc.Row(listings_cards, className="g-4 px-4")  # Increased horizontal padding
    ], fluid=True, className="dashboard-container p-4")
def create_price_filter_layout():
    return dbc.Container([
        # Header Row with Title and Back Button
        dbc.Row([
            dbc.Col(
                html.H1("🔍 Filter Listings", className="emoji-header mb-0"), 
                md=10, className="ps-lg-5 pt-3"
            ),
            dbc.Col(
                dbc.Button(
                    "← Dashboard",
                    href="/",
                    color="light",
                    className="back-btn py-2",
                ), 
                md=2, className="pe-lg-5 pt-3 text-end"
            )
        ], className="align-items-center mb-4 px-lg-5"),
        
        # Filter Controls
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        # Price Range Row
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("💵 Min Price (TND)", className="mb-2"),
                                dbc.Input(
                                    id='min-price-input',
                                    type='number',
                                    value=0,
                                    min=0,
                                    className="form-control"
                                )
                            ], md=6, className="pe-3"),  
                            
                            dbc.Col([
                                dbc.Label("💸 Max Price (TND)", className="mb-2"),
                                dbc.Input(
                                    id='max-price-input',
                                    type='number',
                                    value=1_000_000,
                                    min=0,
                                    className="form-control"
                                )
                            ], md=6, className="ps-3")  
                        ], className="mb-4"),
                        
                        # Property Type
                        dbc.Label("🏘️ Property Type", className="mb-2"),
                        dbc.RadioItems(
                            id='product-type-selector',
                            options=[
                                {"label": "🏠 Sale", "value": 1},
                                {"label": "🏡 Rent", "value": 0},
                                {"label": "🤝 Both", "value": None}
                            ],
                            value=None,
                            inline=True,
                            className="filter-radio"
                        )
                    ])
                ], className="filter-card p-4")
            ], md=10, className="mx-auto")  
        ], className="px-lg-5"),  
        
        # Results Section
        dbc.Row([
            dbc.Col([
                html.Div(id='price-filter-results', className="mt-4 px-lg-5")
            ], md=12)
        ])
    ], fluid=True, className="dashboard-container p-4")