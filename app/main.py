# main.py

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from data_processor import load_data
from graphs import (
    create_pie_chart, create_bar_chart,
    create_delegation_chart, create_publisher_chart, create_type_chart
)

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load and process data
data = load_data()

# Check data format
if isinstance(data, dict):  # Ensure that the data is a dictionary
    total_listings = data.get('total_listings', 0)
    governorate_stats = {item['_id']: item['count'] for item in data.get('governorate_stats', [])}
    type_stats = {item['_id']: item['count'] for item in data.get('type_stats', [])}
    avg_price_sale = round(data.get('avg_price_sale', 0), 2)
    avg_price_rent = round(data.get('avg_price_rent', 0), 2)
    publisher_stats = {item['_id']: item['count'] for item in data.get('publisher_stats', [])}
    delegation_data = data.get('delegation_by_governorate', [])
    listings_data = data.get('listings_data', [])    
    # Calculate additional metrics
    total_shops = sum(count for is_shop, count in publisher_stats.items() if is_shop)
    total_individuals = sum(count for is_shop, count in publisher_stats.items() if not is_shop)
    shop_percentage = round((total_shops / total_listings) * 100, 1) if total_listings > 0 else 0
else:
    print("Error: Data is not in the expected format.")

# Define layout
app.layout = dbc.Container([
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

   
], fluid=True, className="dashboard-container")

if __name__ == "__main__":
    app.run(debug=True)
