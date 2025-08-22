"""
Dashboard and Layout Examples
This file demonstrates how to create complex layouts and dashboards in Bokeh.
"""

import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, curdoc
from bokeh.models import (ColumnDataSource, Select, Slider, Button, Div, 
                         Panel, Tabs, DataTable, TableColumn)
from bokeh.layouts import column, row, gridplot
from bokeh.io import output_file
from bokeh.palettes import Category20, Spectral6
from bokeh.transform import cumsum
from math import pi

def create_financial_dashboard():
    """Create a financial dashboard with multiple charts"""
    # Generate sample financial data
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    prices = 100 + np.cumsum(np.random.randn(100) * 0.5)
    volume = np.random.randint(1000, 10000, 100)
    
    # Create main price chart
    p1 = figure(title="Stock Price", x_axis_type='datetime', 
                width=800, height=300, tools="pan,wheel_zoom,reset")
    p1.line(dates, prices, line_width=2, color='blue')
    p1.circle(dates, prices, size=3, color='blue', alpha=0.5)
    
    # Create volume chart
    p2 = figure(title="Trading Volume", x_axis_type='datetime',
                width=800, height=200, tools="pan,wheel_zoom,reset")
    p2.vbar(x=dates, top=volume, width=0.8, color='green', alpha=0.7)
    
    # Create moving average
    window = 10
    moving_avg = pd.Series(prices).rolling(window=window).mean()
    p1.line(dates, moving_avg, line_width=2, color='red', 
            legend_label=f'{window}-day MA', line_dash='dashed')
    
    # Create price distribution histogram
    p3 = figure(title="Price Distribution", width=300, height=300,
                tools="pan,wheel_zoom,reset")
    hist, edges = np.histogram(prices, bins=20)
    p3.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
            fill_color='navy', alpha=0.7)
    
    # Create summary statistics
    stats_data = {
        'Metric': ['Current Price', 'Max Price', 'Min Price', 'Avg Volume'],
        'Value': [f'${prices[-1]:.2f}', f'${np.max(prices):.2f}', 
                 f'${np.min(prices):.2f}', f'{np.mean(volume):.0f}']
    }
    stats_source = ColumnDataSource(stats_data)
    
    columns = [
        TableColumn(field="Metric", title="Metric"),
        TableColumn(field="Value", title="Value")
    ]
    stats_table = DataTable(source=stats_source, columns=columns, 
                           width=300, height=150)
    
    # Layout
    left_column = column(p1, p2)
    right_column = column(p3, stats_table)
    dashboard = row(left_column, right_column)
    
    return dashboard

def create_sales_dashboard():
    """Create a sales dashboard with different chart types"""
    # Sample sales data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    products = ['Product A', 'Product B', 'Product C', 'Product D']
    
    # Sales by month
    sales_by_month = [120, 150, 180, 160, 200, 220]
    
    # Sales by product (pie chart data)
    product_sales = [450, 320, 280, 150]
    angles = [x/sum(product_sales) * 2*pi for x in product_sales]
    
    # Monthly sales line chart
    p1 = figure(title="Monthly Sales Trend", x_range=months,
                width=400, height=300, tools="pan,wheel_zoom,reset")
    p1.line(months, sales_by_month, line_width=3, color='blue')
    p1.circle(months, sales_by_month, size=8, color='blue')
    p1.y_range.start = 0
    
    # Product sales bar chart
    p2 = figure(title="Sales by Product", x_range=products,
                width=400, height=300, tools="pan,wheel_zoom,reset")
    p2.vbar(x=products, top=product_sales, width=0.8, 
            color=Category20[4], alpha=0.8)
    p2.xaxis.major_label_orientation = 45
    
    # Pie chart for product distribution
    p3 = figure(title="Product Sales Distribution", 
                width=400, height=300, tools="hover", 
                tooltips="@products: @value (@percent%)")
    
    # Calculate pie chart data
    colors = Category20[len(products)]
    start_angle = 0
    for i, (product, angle, color) in enumerate(zip(products, angles, colors)):
        end_angle = start_angle + angle
        p3.wedge(x=0, y=0, radius=0.8, start_angle=start_angle, 
                end_angle=end_angle, color=color, alpha=0.8,
                legend_label=product)
        start_angle = end_angle
    
    # Heatmap of sales by month and product
    months_rep = []
    products_rep = []
    sales_values = []
    
    for month in months:
        for product in products:
            months_rep.append(month)
            products_rep.append(product)
            sales_values.append(np.random.randint(20, 100))
    
    p4 = figure(title="Sales Heatmap", x_range=months, y_range=products,
                width=400, height=300, tools="hover",
                tooltips=[('Month-Product', '@x @y'), ('Sales', '@sales')])
    
    source = ColumnDataSource(data=dict(
        x=months_rep, y=products_rep, sales=sales_values,
        colors=[Spectral6[min(5, max(0, int(val/20)))] for val in sales_values]
    ))
    
    p4.rect(x='x', y='y', width=1, height=1, source=source,
            fill_color='colors', line_color=None)
    
    # Layout in grid
    grid = gridplot([[p1, p2], [p3, p4]], sizing_mode='scale_width')
    
    return grid

def create_tabbed_dashboard():
    """Create a dashboard with tabs"""
    # Tab 1: Overview
    overview_data = np.random.randn(1000)
    p_overview = figure(title="Data Overview", width=600, height=400)
    hist, edges = np.histogram(overview_data, bins=50)
    p_overview.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
                   fill_color='skyblue', alpha=0.7)
    
    tab1 = Panel(child=p_overview, title="Overview")
    
    # Tab 2: Time Series
    dates = pd.date_range('2023-01-01', periods=365, freq='D')
    values = np.cumsum(np.random.randn(365))
    
    p_timeseries = figure(title="Time Series Data", x_axis_type='datetime',
                         width=600, height=400)
    p_timeseries.line(dates, values, line_width=2, color='green')
    
    tab2 = Panel(child=p_timeseries, title="Time Series")
    
    # Tab 3: Correlation Matrix
    data = np.random.randn(100, 4)
    corr_matrix = np.corrcoef(data.T)
    
    p_corr = figure(title="Correlation Matrix", 
                   x_range=['Var1', 'Var2', 'Var3', 'Var4'],
                   y_range=['Var1', 'Var2', 'Var3', 'Var4'],
                   width=400, height=400)
    
    # Create correlation heatmap
    x_coords = []
    y_coords = []
    colors = []
    correlations = []
    
    variables = ['Var1', 'Var2', 'Var3', 'Var4']
    for i, var1 in enumerate(variables):
        for j, var2 in enumerate(variables):
            x_coords.append(var1)
            y_coords.append(var2)
            corr_val = corr_matrix[i, j]
            correlations.append(corr_val)
            # Color based on correlation strength
            color_idx = int((corr_val + 1) * 2.5)  # Scale to 0-5
            colors.append(Spectral6[min(5, max(0, color_idx))])
    
    source = ColumnDataSource(data=dict(
        x=x_coords, y=y_coords, colors=colors, correlations=correlations
    ))
    
    p_corr.rect(x='x', y='y', width=1, height=1, source=source,
               fill_color='colors', line_color='white')
    
    # Add text annotations
    from bokeh.models import LabelSet
    labels = LabelSet(x='x', y='y', text='correlations', 
                     text_font_size='10pt', text_align='center',
                     text_baseline='middle', source=source)
    p_corr.add_layout(labels)
    
    tab3 = Panel(child=p_corr, title="Correlations")
    
    # Create tabs
    tabs = Tabs(tabs=[tab1, tab2, tab3])
    
    return tabs

def main():
    """Main function to create and display dashboard examples"""
    output_file("dashboard_layouts.html")
    
    # Create dashboards
    financial_dash = create_financial_dashboard()
    sales_dash = create_sales_dashboard()
    tabbed_dash = create_tabbed_dashboard()
    
    # Add titles
    title1 = Div(text="<h2>Financial Dashboard</h2>")
    title2 = Div(text="<h2>Sales Dashboard</h2>")
    title3 = Div(text="<h2>Tabbed Dashboard</h2>")
    
    # Main layout
    layout = column(
        Div(text="<h1>Bokeh Dashboard Examples</h1>"),
        title1, financial_dash,
        title2, sales_dash,
        title3, tabbed_dash
    )
    
    show(layout)
    print("Dashboard layouts saved to 'dashboard_layouts.html'")

if __name__ == "__main__":
    main()
