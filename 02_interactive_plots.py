"""
Interactive Bokeh Visualization Examples
This file demonstrates interactive features like widgets, callbacks, and dynamic updates.
"""

import numpy as np
from bokeh.plotting import figure, show, curdoc
from bokeh.models import (ColumnDataSource, HoverTool, Select, Slider, 
                         Button, CheckboxGroup, RadioGroup, Div)
from bokeh.layouts import column, row
from bokeh.io import output_file
from bokeh.transform import factor_cmap
from bokeh.palettes import Category10

def create_interactive_sine_wave():
    """Create an interactive sine wave with frequency and amplitude controls"""
    # Initial data
    x = np.linspace(0, 4*np.pi, 100)
    y = np.sin(x)
    
    source = ColumnDataSource(data=dict(x=x, y=y))
    
    # Create plot
    p = figure(title="Interactive Sine Wave", 
               x_axis_label='x', 
               y_axis_label='y',
               width=700, 
               height=400)
    
    line = p.line('x', 'y', source=source, line_width=2, color='blue')
    
    # Create widgets
    freq_slider = Slider(start=0.1, end=5.0, value=1.0, step=0.1, title="Frequency")
    amp_slider = Slider(start=0.1, end=3.0, value=1.0, step=0.1, title="Amplitude")
    phase_slider = Slider(start=0, end=2*np.pi, value=0, step=0.1, title="Phase")
    
    # JavaScript callback for real-time updates
    callback_code = """
    const data = source.data;
    const freq = freq_slider.value;
    const amp = amp_slider.value;
    const phase = phase_slider.value;
    
    const x = data['x'];
    const y = data['y'];
    
    for (let i = 0; i < x.length; i++) {
        y[i] = amp * Math.sin(freq * x[i] + phase);
    }
    
    source.change.emit();
    """
    
    from bokeh.models import CustomJS
    callback = CustomJS(args=dict(source=source, 
                                 freq_slider=freq_slider,
                                 amp_slider=amp_slider,
                                 phase_slider=phase_slider), 
                       code=callback_code)
    
    freq_slider.js_on_change('value', callback)
    amp_slider.js_on_change('value', callback)
    phase_slider.js_on_change('value', callback)
    
    return column(p, row(freq_slider, amp_slider, phase_slider))

def create_selection_plot():
    """Create a plot with selection and highlighting"""
    N = 200
    x = np.random.random(N) * 100
    y = np.random.random(N) * 100
    colors = np.random.choice(['red', 'green', 'blue', 'orange'], N)
    
    source = ColumnDataSource(data=dict(
        x=x, y=y, colors=colors,
        alpha=[0.6]*N,
        size=[15]*N
    ))
    
    p = figure(title="Selection and Highlighting", 
               tools="pan,wheel_zoom,box_select,lasso_select,reset",
               width=600, 
               height=400)
    
    circles = p.scatter('x', 'y', 
                       color='colors', 
                       size='size',
                       alpha='alpha',
                       source=source,
                       selection_color='red',
                       nonselection_alpha=0.2)
    
    # Add hover tool
    hover = HoverTool(tooltips=[("Index", "$index"), ("(X,Y)", "($x, $y)")])
    p.add_tools(hover)
    
    return p

def create_data_table_plot():
    """Create a plot with linked data table"""
    from bokeh.models import DataTable, TableColumn
    
    # Sample data
    countries = ['USA', 'China', 'Japan', 'Germany', 'India', 'UK', 'France', 'Brazil']
    gdp = [21.43, 14.34, 4.94, 3.85, 2.87, 2.83, 2.72, 1.87]  # in trillions
    population = [331, 1439, 126, 83, 1380, 67, 65, 213]  # in millions
    
    source = ColumnDataSource(data=dict(
        countries=countries,
        gdp=gdp,
        population=population,
        gdp_per_capita=[g*1000000/p for g, p in zip(gdp, population)]
    ))
    
    # Create scatter plot
    p = figure(title="GDP vs Population", 
               x_axis_label='Population (millions)', 
               y_axis_label='GDP (trillions USD)',
               width=600, 
               height=400)
    
    circles = p.scatter('population', 'gdp', 
                       size=20, 
                       color='navy', 
                       alpha=0.6,
                       source=source)
    
    # Add hover tool
    hover = HoverTool(tooltips=[
        ("Country", "@countries"),
        ("GDP", "$@gdp trillion"),
        ("Population", "@population million"),
        ("GDP per capita", "$@gdp_per_capita{0,0}")
    ])
    p.add_tools(hover)
    
    # Create data table
    columns = [
        TableColumn(field="countries", title="Country"),
        TableColumn(field="gdp", title="GDP (Trillions)"),
        TableColumn(field="population", title="Population (Millions)"),
        TableColumn(field="gdp_per_capita", title="GDP per Capita")
    ]
    
    data_table = DataTable(source=source, columns=columns, width=600, height=200)
    
    return column(p, data_table)

def create_crossfilter_plot():
    """Create linked plots that filter each other"""
    # Generate sample data
    N = 300
    x = np.random.normal(0, 1, N)
    y = np.random.normal(0, 1, N)
    colors = np.random.choice(['red', 'green', 'blue'], N)
    
    source = ColumnDataSource(data=dict(x=x, y=y, colors=colors))
    
    # Create two linked plots
    p1 = figure(title="Plot 1: X vs Y", 
                tools="pan,wheel_zoom,box_select,reset",
                width=400, 
                height=300)
    
    p1.scatter('x', 'y', 
               color='colors', 
               size=8, 
               alpha=0.6,
               source=source,
               selection_color='red',
               nonselection_alpha=0.1)
    
    p2 = figure(title="Plot 2: Histogram of X", 
                tools="pan,wheel_zoom,box_select,reset",
                width=400, 
                height=300)
    
    # Create histogram data
    hist, edges = np.histogram(x, bins=20)
    hist_source = ColumnDataSource(data=dict(
        top=hist,
        left=edges[:-1],
        right=edges[1:]
    ))
    
    p2.quad(top='top', bottom=0, left='left', right='right',
            source=hist_source, fill_color='navy', alpha=0.7)
    
    return row(p1, p2)

def main():
    """Main function to create and display all interactive plots"""
    output_file("interactive_plots.html")
    
    # Create all interactive plots
    sine_wave = create_interactive_sine_wave()
    selection_plot = create_selection_plot()
    data_table_plot = create_data_table_plot()
    crossfilter_plot = create_crossfilter_plot()
    
    # Add title
    title = Div(text="<h1>Interactive Bokeh Visualizations</h1>")
    
    # Arrange in layout
    layout = column(
        title,
        sine_wave,
        row(selection_plot, column(data_table_plot)),
        crossfilter_plot
    )
    
    show(layout)
    print("Interactive plots saved to 'interactive_plots.html'")

if __name__ == "__main__":
    main()
