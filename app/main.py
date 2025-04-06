from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from .config import Config
from .data_processor import load_statistics, load_new_listings, clean_data
from app.layouts import create_layout, create_new_listings_layout 

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/custom.css'])

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
    else:
        return html.Div("404: Page Not Found")

if __name__ == "__main__":
    app.run(debug=True)