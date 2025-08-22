"""
Basic Bokeh Plotting Examples
This file demonstrates fundamental plotting capabilities in Bokeh.
"""

import numpy as np
from bokeh.plotting import figure, show, save, output_file
from bokeh.models import HoverTool
from bokeh.layouts import column, row
from bokeh.io import curdoc

# Generate sample data
x = np.linspace(0, 4*np.pi, 100)
y = np.sin(x)
y2 = np.cos(x)

# Sample data for scatter plot
N = 100
colors = np.random.choice(['red', 'green', 'blue', 'orange', 'purple'], N)
x_scatter = np.random.random(N) * 100
y_scatter = np.random.random(N) * 100
sizes = np.random.randint(10, 30, N)

def create_line_plot():
    """Create a basic line plot with multiple lines"""
    p = figure(title="Line Plot Example", 
               x_axis_label='x', 
               y_axis_label='y',
               width=600, 
               height=400)
    
    # Add line renderers
    p.line(x, y, legend_label="sin(x)", line_width=2, color='blue')
    p.line(x, y2, legend_label="cos(x)", line_width=2, color='red', line_dash='dashed')
    
    # Customize legend
    p.legend.location = "top_right"
    p.legend.click_policy = "hide"
    
    return p

def create_scatter_plot():
    """Create a scatter plot with hover tooltips"""
    p = figure(title="Scatter Plot with Hover", 
               x_axis_label='X Value', 
               y_axis_label='Y Value',
               width=600, 
               height=400)
    
    # Add scatter renderer
    scatter = p.scatter(x_scatter, y_scatter, 
                       size=sizes, 
                       color=colors, 
                       alpha=0.6)
    
    # Add hover tool
    hover = HoverTool(tooltips=[
        ("Index", "$index"),
        ("(X,Y)", "($x, $y)"),
        ("Size", "@size")
    ])
    p.add_tools(hover)
    
    return p

def create_bar_chart():
    """Create a bar chart"""
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [20, 35, 30, 25, 40]
    
    p = figure(x_range=categories, 
               title="Bar Chart Example",
               x_axis_label='Categories', 
               y_axis_label='Values',
               width=600, 
               height=400)
    
    p.vbar(x=categories, top=values, width=0.8, color='navy', alpha=0.7)
    
    # Rotate x-axis labels
    p.xaxis.major_label_orientation = 45
    
    return p

def create_area_plot():
    """Create an area plot"""
    x_area = np.linspace(0, 2*np.pi, 50)
    y1 = np.sin(x_area)
    y2 = np.sin(x_area) + 1
    
    p = figure(title="Area Plot Example",
               x_axis_label='x', 
               y_axis_label='y',
               width=600, 
               height=400)
    
    # Create area between two curves
    p.varea(x=x_area, y1=y1, y2=y2, alpha=0.5, color='lightblue')
    p.line(x_area, y1, line_width=2, color='blue')
    p.line(x_area, y2, line_width=2, color='red')
    
    return p

def main():
    """Main function to create and display all plots"""
    # Set output file
    output_file("basic_plots.html")
    
    # Create all plots
    line_plot = create_line_plot()
    scatter_plot = create_scatter_plot()
    bar_chart = create_bar_chart()
    area_plot = create_area_plot()
    
    # Arrange plots in a grid layout
    layout = column(
        row(line_plot, scatter_plot),
        row(bar_chart, area_plot)
    )
    
    # Show the result
    show(layout)
    print("Basic plots saved to 'basic_plots.html'")

if __name__ == "__main__":
    main()
