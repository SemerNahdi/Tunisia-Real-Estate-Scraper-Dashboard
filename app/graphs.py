import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .utils import logger  # Add this import at the top

def create_pie_chart(data, title):
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:10])
    fig = px.bar(
        x=list(sorted_data.keys()),
        y=list(sorted_data.values()),
        title=title,
        labels={'x': 'Governorate', 'y': 'Number of Listings'}
    )
    
    fig.update_traces(
        marker_color='black',
        marker_line_width=0,
        marker_line_color='black',
        marker=dict(
            cornerradius=8,
            line=dict(width=0)
        )
    )
    
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        title_font_color='black',
        font_color='black',
        xaxis_title_font_color='black',
        yaxis_title_font_color='black',
        bargap=0.3,
        showlegend=False,
        height=400
    )
    return fig

def create_type_chart(data):
    """Generate a donut chart for listing types."""
    # Convert numeric types to labels and handle None values
    labels = {1: 'Sale', 0: 'Rent'}
    type_data = {}
    
    # Process data and handle None values
    for k, v in data.items():
        if k is not None and k in labels:
            type_data[labels[k]] = v
    
    # If no valid data, return empty figure
    if not type_data:
        return go.Figure()
    
    fig = px.pie(
        values=list(type_data.values()),
        names=list(type_data.keys()),
        title='Distribution of Sale vs Rent Listings',
        hole=0.6,
        color=list(type_data.keys()),
        color_discrete_map={'Sale': 'black', 'Rent': '#666666'}
    )
    
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        title_font_color='black',
        font_color='black',
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

def create_bar_chart(data, title, x_label, y_label):
    """Generate a bar chart."""
    # Sort data by values in descending order and take top 10
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:10])
    fig = px.bar(
        x=list(sorted_data.keys()),
        y=list(sorted_data.values()),
        title=title,
        labels={'x': x_label, 'y': y_label}
    )
    # Update bar style
    fig.update_traces(
        marker_color='black',
        marker_line_width=0,
        marker_line_color='black',
        marker=dict(
            cornerradius=8,
            line=dict(width=0)
        )
    )
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        title_font_color='black',
        font_color='black',
        xaxis_title_font_color='black',
        yaxis_title_font_color='black',
        bargap=0.3,
        showlegend=False,
        height=400
    )
    return fig

def create_delegation_chart(delegation_data):
    """Generate a chart showing top delegations by governorate."""
    # Process delegation data
    governorates = []
    delegations = []
    counts = []
    
    for gov in delegation_data:
        gov_name = gov['_id']
        for delg in gov['delegations']:
            governorates.append(gov_name)
            delegations.append(delg['delegation'])
            counts.append(delg['count'])
    
    # Create DataFrame and sort by count
    df = pd.DataFrame({
        'Governorate': governorates,
        'Delegation': delegations,
        'Count': counts
    })
    
    # Get top 10 delegations
    top_delegations = df.nlargest(10, 'Count')
    
    fig = px.bar(
        top_delegations,
        x='Delegation',
        y='Count',
        color='Governorate',
        title='Top 10 Delegations by Number of Listings',
        labels={'Delegation': 'Delegation', 'Count': 'Number of Listings'}
    )
    
    # Update bar style with rounded corners
    fig.update_traces(
        marker_line_width=0,
        marker=dict(
            cornerradius=8,
            line=dict(width=0)
        )
    )
    
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        title_font_color='black',
        font_color='black',
        xaxis_title_font_color='black',
        yaxis_title_font_color='black',
        bargap=0.3,
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

def create_publisher_chart(publisher_stats):
    """Generate a chart showing publisher type distribution."""
    # Convert boolean to string labels
    labels = {True: 'Shop', False: 'Individual'}
    data = {labels[k]: v for k, v in publisher_stats.items()}
    
    fig = px.pie(
        values=list(data.values()),
        names=list(data.keys()),
        title='Listings by Publisher Type',
        hole=0.4
    )
    
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        title_font_color='black',
        font_color='black',
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

def create_avg_price_line_chart(df):
    """Generate a line chart showing average prices over time, split by Rent and Sale."""
    if df.empty:
        logger.warning("No data for average price line chart")
        return go.Figure()
    
    fig = px.line(
        df,
        x='year_month',
        y='price',
        color='type_label',
        title='Average Listing Prices Over Time',
        labels={'year_month': 'Month', 'price': 'Average Price (TND)', 'type_label': 'Property Type'},
        markers=True,
        color_discrete_map={'Sale': 'black', 'Rent': '#666666'}  # Changed to match UI theme
    )
    
    # Update line and marker style for a softer look
    fig.update_traces(
        line=dict(
            shape='spline',  # Makes the lines curved
            smoothing=0.8,   # Adjust smoothing factor
            width=3         # Thicker lines
        ),
        marker=dict(
            size=10,
            symbol='circle',
            line=dict(
                width=2,
                color='white'
            )
        )
    )
    
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        title_font_color='black',
        font_color='black',
        xaxis_title_font_color='black',
        yaxis_title_font_color='black',
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        xaxis=dict(
            type='category',
            tickangle=45,
            tickmode='auto',
            nticks=12,
            tickfont=dict(size=10),
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(0,0,0,0.1)',
            tickformat=',d',  # Format numbers with commas
            title_text='Average Price (TND)',
            rangemode='tozero'  # Start y-axis from 0
        ),
        hovermode='x unified',
        margin=dict(l=50, r=50, t=50, b=100)
    )
    return fig

def create_stacked_bar_chart(df):
    """Generate a grouped bar chart showing monthly distribution by property type."""
    if df.empty:
        logger.warning("No data for grouped bar chart")
        return go.Figure()
    
    types = [col for col in df.columns if col != 'year_month']
    if not types:
        logger.warning("No property types found for grouped bar chart")
        return go.Figure()
    
    fig = px.bar(
        df,
        x='year_month',
        y=types,
        title='Monthly Distribution of Listings by Property Type',
        labels={'year_month': 'Month', 'value': 'Number of Listings'},
        barmode='group',  # Changed from 'stack' to 'group'
        color_discrete_map={'Sale': 'black', 'Rent': '#666666'}  # Changed to match UI theme
    )
    
    # Update bar style
    fig.update_traces(
        marker=dict(
            cornerradius=8,
            line=dict(width=1, color='white'),
            opacity=0.9
        ),
        width=0.35  # Adjust bar width
    )
    
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        title_font_color='black',
        font_color='black',
        xaxis_title_font_color='black',
        yaxis_title_font_color='black',
        bargap=0.15,  # Adjust gap between bar groups
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        xaxis=dict(
            type='category',
            tickangle=45,
            tickmode='auto',
            nticks=12,
            tickfont=dict(size=10),
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=0.5,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        hovermode='x unified',
        margin=dict(l=50, r=50, t=50, b=100)
    )
    return fig
