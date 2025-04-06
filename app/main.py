from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from .config import Config
from .data_processor import load_statistics, load_new_listings, fetch_filtered_listings, clean_data
from .layouts import create_layout, create_new_listings_layout, create_price_filter_layout
from datetime import datetime

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/styles.css'])

# Load and process data
url_statistics = f"{Config.FASTAPI_URL}/statistics"
url_new_listings = f"{Config.FASTAPI_URL}/annonces/new"

raw_statistics_data = load_statistics(url_statistics)
statistics_data = clean_data(raw_statistics_data)

raw_new_listings_data = load_new_listings(url_new_listings)
new_listings_data = clean_data(raw_new_listings_data)

# Define layout
app.layout = dcc.Location(id='url', refresh=False), html.Div(id='page-content')

# Callback to display the correct page
@callback(Output('page-content', 'children'),
          [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return create_layout(statistics_data, new_listings_data)
    elif pathname == '/new-listings':
        return create_new_listings_layout(new_listings_data)
    elif pathname == '/price-filter':
        return create_price_filter_layout()
    else:
        return html.Div("404: Page Not Found")

# Callback to fetch and display filtered listings
@callback(
    Output('price-filter-results', 'children'),
    [Input('min-price-input', 'value'),
     Input('max-price-input', 'value'),
     Input('product-type-selector', 'value')]
)

def update_filtered_listings(min_price, max_price, producttype):
    data = fetch_filtered_listings(min_price, max_price, producttype)
    annonces = data.get('annonces', [])
    total = data.get('total', 0)
    
    if not annonces:
        return html.Div([
            html.H4(f"Total Listings: {total}", className="text-center my-2"),
            html.P("No listings found.", className="text-center my-2")
        ])
    
    # Table header without the Listing ID
    table_header = [
        html.Thead(
            html.Tr([
                html.Th("Title"),
                html.Th("Price"),
                html.Th("Location"),
                html.Th("Description"),
                html.Th("Published On")
            ])
        )
    ]
    
    # Table body with alternating row colors
    table_rows = []
    for i, annonce in enumerate(annonces):
        # Format the publication date
        published_on = annonce.get('metadata', {}).get('publishedOn', 'N/A')
        if published_on != 'N/A':
            try:
                # Parse the ISO 8601 date string and format it to a readable format
                published_on = datetime.fromisoformat(published_on.replace("Z", "+00:00")).strftime('%B %d, %Y, %I:%M %p')
            except ValueError:
                published_on = 'Invalid Date'
        
        # Alternate row classes
        row_class = "table-soft-light" if i % 2 == 0 else "table-soft-dark"
        
        # Add rows to the table
        table_rows.append(
            html.Tr(
                className=row_class,
                children=[
                    html.Td(annonce.get('title', 'N/A')),
                    html.Td(f"{annonce.get('price', 'N/A')} TND"),
                    html.Td(f"{annonce.get('location', {}).get('governorate', 'N/A')}, "
                            f"{annonce.get('location', {}).get('delegation', 'N/A')}"),
                    html.Td(f"{annonce.get('description', 'N/A')[:100]}..."),
                    html.Td(published_on)
                ]
            )
        )
    
    return html.Div([
        html.H4(f"Total Listings: {total}", className="text-center my-2"),
        dbc.Table(
            children=[
                *table_header,
                html.Tbody(children=table_rows)
            ],
            bordered=True,
            hover=True,
            responsive=True,
            striped=True,
            className="rounded-table"
        )
    ])

if __name__ == "__main__":
    app.run(debug=False)