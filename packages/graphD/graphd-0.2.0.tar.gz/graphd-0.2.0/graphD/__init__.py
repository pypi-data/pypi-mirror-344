from .core import (
    Graph, plot, plot_to_base64,
    create_complete_graph, create_star_graph, 
    create_path_graph, create_cycle_graph
)
from .renderer import Color, GraphRenderer, Bitmap, WHITE, BLACK, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE
from .stats import StatsPlotter

# Import visualization types
from .visualizations import Histogram, PieChart, Heatmap

# Import subplot functionality
from .subplot import Subplot

# Import interactive features
from .interactive import InteractiveGraph, Tooltip, Highlight, PointLabel

# Import animation functionality
from .animation import Animation, AnimationBuilder

__all__ = [
    # Core classes
    "Graph", "plot", "plot_to_base64",
    # Renderer classes
    "Color", "GraphRenderer", "Bitmap",
    # Predefined colors
    "WHITE", "BLACK", "RED", "GREEN", "BLUE", "YELLOW", "ORANGE", "PURPLE",
    # Factory functions
    "create_complete_graph", "create_star_graph", 
    "create_path_graph", "create_cycle_graph",
    # Stats module
    "StatsPlotter",
    # Visualization types
    "Histogram", "PieChart", "Heatmap",
    # Subplot functionality
    "Subplot",
    # Interactive features
    "InteractiveGraph", "Tooltip", "Highlight", "PointLabel",
    # Animation
    "Animation", "AnimationBuilder"
]

"""
graphD - A Python library for drawing graphs from scratch with PixelD engine

Example usage:

```python
import graphD

# Create a graph
g = graphD.Graph()

# Add some nodes with attributes
g.add_node('A', color='#FF0000', size=20, label='Node A')  # Red node
g.add_node('B', color='#00FF00', size=15, label='Node B')  # Green node
g.add_node('C', color='#0000FF', size=25, label='Node C')  # Blue node
g.add_node('D', color='#FFFF00', label='Node D')          # Yellow node

# Add edges between nodes
g.add_edge('A', 'B', weight=5, color='#888888')  # Gray edge
g.add_edge('B', 'C')
g.add_edge('C', 'D')
g.add_edge('D', 'A')

# Add a directed edge with a dashed line
g.add_directed_edge('A', 'C', style='dashed', color='#FF00FF')

# Render the graph to an image file (supports .ppm, .bmp)
image_file = graphD.plot(g, filename="my_graph.bmp")
print(f"Graph image saved to: {image_file}")

# Generate a base64 data URL for embedding in web pages or notebooks
data_url = graphD.plot_to_base64(g, theme="dark", title="My Graph")
print(f"Data URL length: {len(data_url)}")

# Using factory functions for common graph types
complete = graphD.create_complete_graph(5)  # Complete graph with 5 nodes
star = graphD.create_star_graph(8)         # Star graph with 8 outer nodes
path = graphD.create_path_graph(10)        # Path with 10 nodes
cycle = graphD.create_cycle_graph(6)       # Cycle with 6 nodes

# Use themes for different visual styles
renderer = graphD.GraphRenderer(theme="dark")
renderer.set_title("Complete Graph")
renderer.render(complete, "complete_graph.bmp")

# Create statistical visualizations
stats = graphD.StatsPlotter(width=800, height=600)
stats.create_bar_chart([10, 25, 15, 30, 20], ["A", "B", "C", "D", "E"], 
                     title="Sample Bar Chart", save_to="bar_chart.bmp")
""" 