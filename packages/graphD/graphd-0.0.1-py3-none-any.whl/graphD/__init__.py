from .core import Graph, plot
from .renderer import Color, GraphRenderer, Bitmap

__all__ = ["Graph", "plot", "Color", "GraphRenderer", "Bitmap"]

"""
graphD - A Python library for drawing graphs from scratch

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
g.add_edge('A', 'C')

# Render the graph to an image file
image_file = graphD.plot(g, filename="my_graph.ppm")
print(f"Graph image saved to: {image_file}")
```

The PPM format is a simple image format that can be viewed with many image viewers.
For more complex rendering, you can directly use the GraphRenderer class.
""" 