import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_pie_chart(data, title):
    """Generate a bar chart for governorate distribution."""
    # Sort data by values in descending order and take top 10
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:10])
    fig = px.bar(
        x=list(sorted_data.keys()),
        y=list(sorted_data.values()),
        title=title,
        labels={'x': 'Governorate', 'y': 'Number of Listings'}
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
