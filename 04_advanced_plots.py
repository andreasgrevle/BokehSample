"""
Advanced Bokeh Visualization Examples
This file demonstrates sophisticated plotting techniques including heatmaps and network graphs.
"""

import numpy as np
import pandas as pd
from bokeh.plotting import figure, show, output_file
from bokeh.models import (ColumnDataSource, HoverTool, ColorBar, LinearColorMapper,
                         LabelSet, Circle, MultiLine, Range1d)
from bokeh.layouts import column, row
from bokeh.palettes import Viridis256, RdYlBu11, Category20
from bokeh.transform import transform
import networkx as nx

def create_correlation_heatmap():
    """Create an advanced correlation heatmap with annotations"""
    # Generate sample correlation data
    np.random.seed(42)
    variables = ['Revenue', 'Profit', 'Employees', 'R&D_Spend', 'Marketing', 
                'Customer_Sat', 'Market_Share', 'Innovation_Index']
    n_vars = len(variables)
    
    # Create realistic correlation matrix
    base_corr = np.random.randn(n_vars, n_vars)
    correlation_matrix = np.corrcoef(base_corr)
    
    # Make some correlations more realistic
    correlation_matrix[0, 1] = 0.85  # Revenue-Profit strong correlation
    correlation_matrix[1, 0] = 0.85
    correlation_matrix[0, 6] = 0.72  # Revenue-Market_Share correlation
    correlation_matrix[6, 0] = 0.72
    correlation_matrix[3, 7] = 0.68  # R&D-Innovation correlation
    correlation_matrix[7, 3] = 0.68
    
    # Prepare data for plotting
    x_coords = []
    y_coords = []
    correlations = []
    colors = []
    text_colors = []
    
    for i, var1 in enumerate(variables):
        for j, var2 in enumerate(variables):
            x_coords.append(var1)
            y_coords.append(var2)
            corr_val = correlation_matrix[i, j]
            correlations.append(f"{corr_val:.2f}")
            colors.append(corr_val)
            # White text for dark backgrounds, black for light
            text_colors.append('white' if abs(corr_val) > 0.5 else 'black')
    
    # Create the plot
    p = figure(title="Business Metrics Correlation Heatmap",
               x_range=variables, y_range=list(reversed(variables)),
               width=700, height=600,
               toolbar_location=None,
               tools="hover", tooltips=[("Variables", "@x, @y"), ("Correlation", "@correlations")])
    
    # Color mapper
    color_mapper = LinearColorMapper(palette=RdYlBu11, low=-1, high=1)
    
    # Create data source
    source = ColumnDataSource(data=dict(
        x=x_coords,
        y=y_coords,
        correlations=correlations,
        colors=colors,
        text_colors=text_colors
    ))
    
    # Add rectangles
    p.rect(x="x", y="y", width=1, height=1, source=source,
           fill_color=transform('colors', color_mapper), line_color=None)
    
    # Add text annotations
    labels = LabelSet(x='x', y='y', text='correlations', 
                     text_font_size='10pt', text_align='center',
                     text_baseline='middle', text_color='text_colors',
                     source=source)
    p.add_layout(labels)
    
    # Add color bar
    color_bar = ColorBar(color_mapper=color_mapper, width=8, location=(0,0),
                        title="Correlation Coefficient")
    p.add_layout(color_bar, 'right')
    
    # Styling
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "10pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = 45
    
    return p

def create_network_graph():
    """Create an interactive network graph visualization"""
    # Create a sample social network
    G = nx.karate_club_graph()
    
    # Calculate layout positions
    pos = nx.spring_layout(G, k=1, iterations=50)
    
    # Calculate node metrics
    degree_centrality = nx.degree_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)
    clustering_coeff = nx.clustering(G)
    
    # Prepare node data
    node_indices = list(G.nodes())
    node_x = [pos[node][0] for node in node_indices]
    node_y = [pos[node][1] for node in node_indices]
    node_sizes = [degree_centrality[node] * 500 + 10 for node in node_indices]
    node_colors = [betweenness_centrality[node] for node in node_indices]
    node_labels = [f"Node {node}" for node in node_indices]
    
    # Prepare edge data
    edge_start = []
    edge_end = []
    edge_x = []
    edge_y = []
    
    for edge in G.edges():
        edge_start.append(edge[0])
        edge_end.append(edge[1])
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append([x0, x1])
        edge_y.append([y0, y1])
    
    # Create the plot
    p = figure(title="Social Network Analysis - Karate Club Graph",
               width=800, height=600,
               tools="pan,wheel_zoom,box_zoom,reset,hover,tap",
               tooltips=[("Node", "@labels"), 
                        ("Degree Centrality", "@degree{0.000}"),
                        ("Betweenness", "@betweenness{0.000}"),
                        ("Clustering", "@clustering{0.000}")])
    
    # Create data sources
    node_source = ColumnDataSource(data=dict(
        x=node_x, y=node_y, 
        sizes=node_sizes, 
        colors=node_colors,
        labels=node_labels,
        degree=[degree_centrality[node] for node in node_indices],
        betweenness=[betweenness_centrality[node] for node in node_indices],
        clustering=[clustering_coeff[node] for node in node_indices]
    ))
    
    edge_source = ColumnDataSource(data=dict(
        xs=edge_x, ys=edge_y
    ))
    
    # Color mapper for nodes
    node_color_mapper = LinearColorMapper(palette=Viridis256, 
                                         low=min(node_colors), 
                                         high=max(node_colors))
    
    # Add edges
    p.multi_line('xs', 'ys', source=edge_source, 
                line_color='gray', line_alpha=0.5, line_width=1)
    
    # Add nodes
    nodes = p.scatter('x', 'y', size='sizes', source=node_source,
                     fill_color=transform('colors', node_color_mapper),
                     line_color='black', line_width=1, alpha=0.8)
    
    # Add node labels
    node_labels = LabelSet(x='x', y='y', text='labels',
                          text_font_size='8pt', text_align='center',
                          text_baseline='middle', source=node_source)
    p.add_layout(node_labels)
    
    # Add color bar
    color_bar = ColorBar(color_mapper=node_color_mapper, width=8, location=(0,0),
                        title="Betweenness Centrality")
    p.add_layout(color_bar, 'right')
    
    # Styling
    p.axis.visible = False
    p.grid.visible = False
    
    # Add selection callback for highlighting
    from bokeh.models import CustomJS
    callback = CustomJS(args=dict(source=node_source), code="""
        const selected = source.selected.indices;
        const data = source.data;
        
        // Reset all alphas
        for (let i = 0; i < data['x'].length; i++) {
            data['alpha'] = data['alpha'] || [];
            data['alpha'][i] = 0.8;
        }
        
        // Highlight selected nodes
        for (let i = 0; i < selected.length; i++) {
            data['alpha'][selected[i]] = 1.0;
        }
        
        source.change.emit();
    """)
    
    node_source.selected.js_on_change('indices', callback)
    
    return p

def main():
    """Main function to create and display advanced plots"""
    output_file("advanced_plots.html")
    
    # Create advanced plots
    heatmap = create_correlation_heatmap()
    network = create_network_graph()
    
    # Create layout with descriptions
    from bokeh.models import Div
    
    title = Div(text="<h1>Advanced Bokeh Visualizations</h1>")
    
    heatmap_desc = Div(text="""
    <h3>Correlation Heatmap</h3>
    <p>This heatmap shows correlations between business metrics with color-coded values and annotations. 
    Hover over cells to see exact correlation values. Red indicates negative correlation, 
    blue indicates positive correlation.</p>
    """)
    
    network_desc = Div(text="""
    <h3>Network Graph</h3>
    <p>This interactive network graph visualizes the famous Karate Club dataset. Node size represents 
    degree centrality, color represents betweenness centrality. You can pan, zoom, and hover over 
    nodes to see detailed metrics. Click on nodes to highlight them.</p>
    """)
    
    # Arrange in layout
    layout = column(
        title,
        heatmap_desc,
        heatmap,
        network_desc,
        network
    )
    
    show(layout)
    print("Advanced plots saved to 'advanced_plots.html'")

if __name__ == "__main__":
    main()
