# graphD

A Python library for drawing graphs from scratch. This library implements its own rendering system without relying on external drawing libraries.

## Features

- Pure Python implementation, no external dependencies
- Custom rendering engine with a force-directed layout algorithm
- Support for node and edge attributes (color, size, labels, etc.)
- Outputs to PPM image format (viewable in most image viewers)
- Built from scratch, every pixel calculated individually

## Installation

```bash
pip install graphD
```

## Usage

### Basic Example

```python
import graphD

# Create a graph
g = graphD.Graph()

# Add nodes with attributes
g.add_node('A', color='#FF0000', size=20, label='Node A')  # Red node
g.add_node('B', color='#00FF00', size=15, label='Node B')  # Green node
g.add_node('C', color='#0000FF', size=25, label='Node C')  # Blue node

# Add edges
g.add_edge('A', 'B', color='#888888')  # Gray edge
g.add_edge('B', 'C')
g.add_edge('A', 'C')

# Render the graph to an image file
image_file = graphD.plot(g, filename="my_graph.ppm")
print(f"Graph image saved to: {image_file}")
```

### Advanced Usage

You can directly use the renderer components for more control:

```python
from graphD import Graph, GraphRenderer, Color

# Create graph and add elements
graph = Graph()
graph.add_node('1', color='#FF0000')
graph.add_node('2', color='#00FF00')
graph.add_edge('1', '2')

# Create a custom renderer
renderer = GraphRenderer(width=1200, height=900)
renderer.node_color = Color(0, 0, 255)  # Default blue for nodes
renderer.edge_color = Color(0, 0, 0)     # Default black for edges
renderer.render(graph, "custom_graph.ppm")
```

## How It Works

The library uses a force-directed layout algorithm to position nodes in a visually appealing way:

1. Nodes are initially arranged in a circle
2. Repulsive forces push nodes away from each other
3. Attractive forces pull connected nodes toward each other
4. After several iterations, nodes settle into a balanced layout

Drawing is performed using basic algorithms:
- Bresenham's line algorithm for edges
- Circle drawing for nodes
- Simple pixel-based font for labels

The output is saved in PPM (Portable Pixmap) format, which is a simple image format supported by many image viewers.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

[MIT](LICENSE) 