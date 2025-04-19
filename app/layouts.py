# layouts.py
"""
Dash layouts for the Tunisia Real Estate Dashboard application.
Defines the main dashboard, new listings, and price filter page layouts.
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from .graphs import (
    create_pie_chart,
    create_delegation_chart,
    create_publisher_chart,
    create_type_chart
)
from datetime import datetime
from .config import Config
from .utils import logger
from .data_processor import fetch_listing_details
import pandas as pd
import json


# --------------------------- Navigation Header ---------------------------
def create_navigation_header(active_page='/'):
    """Create the navigation bar header for all pages."""
    return dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col(html.H3("🏠 Tunisia Real Estate", className="mb-0"), width="auto"),
                dbc.Col([
                    dbc.Nav([
                        dbc.NavItem(dbc.NavLink(
                            "📊 Dashboard", href="/", active=active_page == "/", className="nav-link")),
                        dbc.NavItem(dbc.NavLink(
                            "✨ New Listings", href="/new-listings", active=active_page == "/new-listings", className="nav-link")),
                        dbc.NavItem(dbc.NavLink(
                            "🔍 Price Filter", href="/price-filter", active=active_page == "/price-filter", className="nav-link"))
                    ], className="ms-auto")
                ])
            ], align="center")
        ], fluid=True),
        color="white",
        className="nav-header"
    )


# --------------------------- Main Dashboard Layout ---------------------------
def create_layout(statistics_data, new_listings_data):
    """Create the main dashboard layout with key metrics and charts."""
    if not isinstance(statistics_data, dict) or not isinstance(new_listings_data, dict):
        logger.error("Invalid data format for dashboard layout")
        return html.Div("Error: Data is not in the expected format.")

    # Extract statistics
    total_listings = statistics_data.get('total_listings', 0)
    governorate_stats = {item['_id']: item['count'] for item in statistics_data.get('governorate_stats', [])}
    type_stats = {item['_id']: item['count'] for item in statistics_data.get('type_stats', [])}
    avg_price_sale = round(statistics_data.get('avg_price_sale', 0), 2)
    avg_price_rent = round(statistics_data.get('avg_price_rent', 0), 2)
    publisher_stats = {item['_id']: item['count'] for item in statistics_data.get('publisher_stats', [])}
    delegation_data = statistics_data.get('delegation_by_governorate', [])

    # Calculate shop percentage
    total_shops = sum(count for is_shop, count in publisher_stats.items() if is_shop)
    total_individuals = sum(count for is_shop, count in publisher_stats.items() if not is_shop)
    shop_percentage = round((total_shops / total_listings) * 100, 1) if total_listings > 0 else 0

    return html.Div([
        create_navigation_header('/'),
        dbc.Container([
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
        ], className="mb-5 g-3"),

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
                dbc.Card([
                    dbc.CardHeader("🏢 Publisher Types", className="chart-header"),
                    dbc.CardBody([
                        dcc.Graph(id='publisher-chart', figure=create_publisher_chart(publisher_stats))
                    ])
                ], className="chart-card")
            ], md=6),

            # Right Column
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🏛️ Property Types", className="chart-header"),
                    dbc.CardBody([
                        dcc.Graph(id='type-chart', figure=create_type_chart(type_stats))
                    ])
                ], className="chart-card mb-4"),
                dbc.Card([
                    dbc.CardHeader("🗺️ Top Delegations", className="chart-header"),
                    dbc.CardBody([
                        dcc.Graph(id='delegation-chart', figure=create_delegation_chart(delegation_data))
                    ])
                ], className="chart-card")
            ], md=6)
        ], className="g-4")
    ], fluid=True, className="dashboard-container p-4")
    ])


# --------------------------- New Listings Layout ---------------------------
def create_new_listings_layout(new_listings_data):
    """Create the layout for the new listings page."""
    if not isinstance(new_listings_data, dict):
        logger.error("Invalid data format for new listings layout")
        return html.Div("Error: Data is not in the expected format.")

    new_count = new_listings_data.get('count', 0)
    new_annonces = new_listings_data.get('new_annonces', [])

    listings_cards = [
        dbc.Col([
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
            ], className="mb-4 listing-card hover-scale")
        ], md=6) for annonce in new_annonces
    ]

    return html.Div([
        create_navigation_header('/new-listings'),
        dbc.Container([
            # Header Row
            dbc.Row([
                dbc.Col(
                    dbc.Button(
                        "← Dashboard",
                        href="/",
                        color="light",
                        className="back-btn py-2"
                    ), md=2, className="ps-4 pt-3"
                ),
                dbc.Col(
                    html.H1("✨ New Listings", className="emoji-header mb-0 text-center"),
                    md=8, className="pt-3"
                ),
                dbc.Col(md=2)  # Empty column for spacing
            ], className="align-items-center mb-4"),
            html.H4(f"📌 Total New Listings: {new_count}", className="text-center my-2"),
            dbc.Row(listings_cards, className="g-4 px-4")
        ], fluid=True, className="dashboard-container p-4")
    ])

# --------------------------- Listing Details Layout ---------------------------
def create_listing_details_layout(listing_id):
    """Create styled layout for listing details with badges."""
    data = fetch_listing_details(listing_id)
    
    if not data:
        return dbc.Container([
            create_navigation_header('/listings'),
            html.H3("Listing Not Found", className="text-center my-4"),
            dbc.Button(
                "← Back to Price Filter",
                href="/price-filter",
                color="primary",
                className="btn btn-primary d-flex align-items-center mx-auto",
                style={"borderRadius": "20px"}
            )
        ], fluid=True, className="dashboard-container p-4")
    
    listing = data.get('listing', {})
    
    # Process images for carousel
    images = listing.get('images', [])
    carousel_items = [
        {
            "key": f"image-{i}",
            "src": img,
            "header": f"Image {i+1}",
            "img_style": {"width": "100%", "height": "500px", "objectFit": "cover"}
        } for i, img in enumerate(images)
    ]
    
    # Format date
    published_date = listing.get('metadata', {}).get('publishedOn', 'N/A')
    if published_date != 'N/A':
        published_date = datetime.fromisoformat(published_date.replace('Z', '+00:00')).strftime('%B %d, %Y')

    # Property type, publisher type, and status for badges
    property_type = "Rent" if listing.get('metadata', {}).get('producttype') == 0 else "Sale"
    publisher_type = "Shop" if listing.get('metadata', {}).get('publisher', {}).get('isShop') else "Individual"
    status = "Modified" if listing.get('metadata', {}).get('isModified') else "Original"

    return html.Div([
        create_navigation_header('/listings'),
        dbc.Container([
            # Header Row
            dbc.Row([
                dbc.Col(
                    dbc.Button(
                        "← Back to Price Filter",
                        href="/price-filter",
                        color="light",
                        className="back-btn py-2"
                    ), md=2, className="ps-4 pt-3"
                ),
                dbc.Col(
                    html.H1("🏠 Listing Details", className="emoji-header mb-0 text-center"),
                    md=8, className="pt-3"
                ),
                dbc.Col(md=2)
            ], className="align-items-center mb-4"),

            # Carousel
            dbc.Card([
                dbc.CardBody([
                    dbc.Carousel(
                        items=carousel_items,
                        controls=True,
                        indicators=True,
                        interval=4000,
                        className="listing-carousel"
                    ) if images else html.P("No images available", className="text-center")
                ])
            ], className="mb-4 shadow-sm", style={"borderRadius": "10px"}),

            # Main Info Card
            dbc.Card([
                dbc.CardBody([
                    html.H3(listing.get('title', 'N/A'), className="text-primary mb-4", style={"fontWeight": "600"}),
                    dbc.Row([
                        dbc.Col([
                            html.H4("💰 Price", className="mb-3"),
                            html.P(f"{listing.get('price', 'N/A')} TND", className="lead"),
                            html.H4("📍 Location", className="mb-3 mt-4"),
                            html.P([
                                f"{listing.get('location', {}).get('governorate', 'N/A')}, ",
                                f"{listing.get('location', {}).get('delegation', 'N/A')}"
                            ], className="lead")
                        ], md=6),
                        dbc.Col([
                            html.H4("📅 Published On", className="mb-3"),
                            html.P(published_date, className="lead"),
                            html.H4("👤 Publisher", className="mb-3 mt-4"),
                            html.P(listing.get('metadata', {}).get('publisher', {}).get('name', 'N/A'), className="lead")
                        ], md=6)
                    ]),
                    html.Hr(className="my-4"),
                    html.H4("📝 Description", className="mb-3"),
                    html.P(listing.get('description', 'N/A'), className="lead", style={"lineHeight": "1.6"}),
                    html.Hr(className="my-4"),
                    dbc.Row([
                        dbc.Col([
                            html.H4("Additional Details", className="mb-3"),
                            html.P([
                                "🏷️ Property Type: ",
                                dbc.Badge(
                                    property_type,
                                    color="primary" if property_type == "Rent" else "success",
                                    className="ms-2"
                                )
                            ], className="mb-2"),
                            html.P([
                                "🏪 Publisher Type: ",
                                dbc.Badge(
                                    publisher_type,
                                    color="warning" if publisher_type == "Shop" else "secondary",
                                    className="ms-2"
                                )
                            ], className="mb-2"),
                            html.P([
                                "✏️ Status: ",
                                dbc.Badge(
                                    status,
                                    color="info" if status == "Original" else "danger",
                                    className="ms-2"
                                )
                            ], className="mb-2")
                        ])
                    ])
                ])
            ], className="mb-4 shadow-sm", style={"borderRadius": "10px"})
        ], fluid=True, className="dashboard-container p-4")
    ])

# --------------------------- Price Filter Layout ---------------------------
def create_price_filter_layout():
    """Create the layout for the price filter page."""
    return html.Div([
        create_navigation_header('/price-filter'),
        dbc.Container([
            # Header Row
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
                        className="back-btn py-2"
                    ), md=2, className="pe-lg-5 pt-3 text-end"
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
                                        value=100,
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
                dbc.Col(
                    html.Div(id='price-filter-results', className="mt-4 px-lg-5"),
                    md=12
                )
            ])
        ], fluid=True, className="dashboard-container p-4")
    ])