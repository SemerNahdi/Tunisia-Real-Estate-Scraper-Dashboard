from dash import Dash, dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
from .config import Config
from .data_processor import (
    load_statistics, 
    load_new_listings, 
    fetch_filtered_listings, 
    clean_data, 
    fetch_listings_by_date,
    fetch_all_listings,
    process_average_prices_over_time,
    process_monthly_distribution_by_type
)
from .layouts import (
    create_layout, 
    create_navigation_header, 
    create_new_listings_layout, 
    create_price_filter_layout,
    create_listing_details_layout,
    create_date_filter_layout,
    create_all_listings_layout
)
from datetime import datetime
from .utils import logger

# Initialize the app
app = Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    '/assets/styles.css',
    'https://use.fontawesome.com/releases/v5.15.4/css/all.css'
])

# Load and process data
url_statistics = f"{Config.FASTAPI_URL}/statistics"
url_new_listings = f"{Config.FASTAPI_URL}/annonces/new"
url_all_listings = f"{Config.FASTAPI_URL}/annonces"

raw_statistics_data = load_statistics(url_statistics)
statistics_data = clean_data(raw_statistics_data)

raw_new_listings_data = load_new_listings(url_new_listings)
new_listings_data = clean_data(raw_new_listings_data)

# After processing the data
all_listings_data = fetch_all_listings()
logger.debug(f"Fetched {len(all_listings_data)} listings")

avg_prices_df = process_average_prices_over_time(all_listings_data)
logger.debug(f"Processed average prices, dataframe shape: {avg_prices_df.shape}")

distribution_df = process_monthly_distribution_by_type(all_listings_data)
logger.debug(f"Processed distribution, dataframe shape: {distribution_df.shape}")

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
    elif pathname.startswith('/listings/'):
        listing_id = pathname.split('/')[-1]
        return create_listing_details_layout(listing_id)
    elif pathname == '/date-filter':
        return create_date_filter_layout()
    elif pathname == '/all-listings':
        return create_all_listings_layout(avg_prices_df, distribution_df)
    else:
        return html.Div("404: Page Not Found")

def create_listings_table(annonces, include_description=True):
    table_header = [
        html.Thead(
            html.Tr([
                html.Th("Title"),
                html.Th("Price"),
                html.Th("Location"),
                *(([html.Th("Description")] if include_description else []) +
                  [html.Th("Published On"),
                   html.Th("Actions")])
            ])
        )
    ]
    
    table_rows = []
    for i, annonce in enumerate(annonces):
        listing_id = annonce.get('id', 'N/A')
        published_on = annonce.get('metadata', {}).get('publishedOn', 'N/A')
        if published_on != 'N/A':
            try:
                date_format = '%B %d, %Y, %I:%M %p' if include_description else '%B %d, %Y'
                published_on = datetime.fromisoformat(published_on.replace("Z", "+00:00")).strftime(date_format)
            except ValueError:
                published_on = 'Invalid Date'
        
        location = annonce.get('location', {})
        location_str = f"{location.get('governorate', 'N/A')}, {location.get('delegation', 'N/A')}"
        
        row_data = [
            html.Td(annonce.get('title', 'N/A')),
            html.Td(f"{annonce.get('price', 'N/A')} TND"),
            html.Td(location_str)
        ]
        
        if include_description:
            description = annonce.get('description', 'N/A')
            if description != 'N/A':
                description = f"{description[:100]}..." if len(description) > 100 else description
            row_data.append(html.Td(description))
        
        row_data.extend([
            html.Td(published_on),
            html.Td(
                dbc.Button(
                    "View Details",
                    href=f"/listings/{listing_id}",
                    color="primary",
                    size="sm",
                    className="view-details-btn",
                    **({"id": f"view-details-{listing_id}", "external_link": True, "n_clicks": 0} if include_description else {})
                ),
                className="text-center"
            )
        ])
        
        row_class = "table-soft-light" if i % 2 == 0 else "table-soft-dark"
        table_rows.append(html.Tr(className=row_class, children=row_data))
    
    return dbc.Table(
        children=[*table_header, html.Tbody(children=table_rows)],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        className="rounded-table"
    )

# Then modify the callbacks to use this function:
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
    
    return html.Div([
        html.H4(f"Total Listings: {total}", className="text-center my-2"),
        create_listings_table(annonces, include_description=True)
    ])

@callback(
    Output('date-filter-results', 'children'),
    [Input('date-filter-button', 'n_clicks')],
    [State('date-range', 'start_date'),
     State('date-range', 'end_date'),
     State('location-selector', 'value'),
     State('date-product-type-selector', 'value')],
    prevent_initial_call=True
)
def update_date_filtered_listings(n_clicks, start_date, end_date, location, producttype):
    logger.debug(f"Callback triggered with dates: {start_date} to {end_date}")
    if not n_clicks or not start_date or not end_date:
        return html.Div("Select dates and click search to view listings.", className="text-center my-4")
    
    try:
        start_date = datetime.strptime(start_date.split('T')[0], '%Y-%m-%d')
        end_date = datetime.strptime(end_date.split('T')[0], '%Y-%m-%d')
        data = fetch_listings_by_date(start_date, end_date, producttype)
        annonces = data.get('annonces', [])
        total = data.get('total', 0)
        
        if not annonces:
            return html.Div([
                html.H4(f"Total Listings: {total}", className="text-center my-2"),
                html.P("No listings found for the selected criteria.", className="text-center my-2")
            ])
        
        if location:
            governorate, delegation = location.split('|')
            annonces = [
                a for a in annonces 
                if a.get('location', {}).get('governorate') == governorate 
                and a.get('location', {}).get('delegation') == delegation
            ]
        
        table_header = [
            html.Thead(
                html.Tr([
                    html.Th("Title"),
                    html.Th("Price"),
                    html.Th("Location"),
                    html.Th("Published On"),
                    html.Th("Actions")
                ])
            )
        ]
        
        table_rows = []
        for i, annonce in enumerate(annonces):
            listing_id = annonce.get('id', 'N/A')
            published_on = annonce.get('metadata', {}).get('publishedOn', 'N/A')
            if published_on != 'N/A':
                published_on = datetime.fromisoformat(published_on.replace("Z", "+00:00")).strftime('%B %d, %Y')
            
            location_str = f"{annonce.get('location', {}).get('governorate', 'N/A')}, {annonce.get('location', {}).get('delegation', 'N/A')}"
            
            row_class = "table-soft-light" if i % 2 == 0 else "table-soft-dark"
            
            table_rows.append(
                html.Tr(
                    className=row_class,
                    children=[
                        html.Td(annonce.get('title', 'N/A')),
                        html.Td(f"{annonce.get('price', 'N/A')} TND"),
                        html.Td(location_str),
                        html.Td(published_on),
                        html.Td(
                            dbc.Button(
                                "View Details",
                                href=f"/listings/{listing_id}",
                                color="primary",
                                size="sm",
                                className="view-details-btn"
                            ),
                            className="text-center"
                        )
                    ]
                )
            )
        
        return html.Div([
            html.H4(f"Total Listings: {len(annonces)}", className="text-center my-2"),
            create_listings_table(annonces, include_description=False)
        ])
        
    except Exception as e:
        logger.error(f"Error in date filter: {str(e)}")
        return html.Div("An error occurred while filtering listings.", className="text-center text-danger my-4")

if __name__ == "__main__":
    app.run(debug=False)