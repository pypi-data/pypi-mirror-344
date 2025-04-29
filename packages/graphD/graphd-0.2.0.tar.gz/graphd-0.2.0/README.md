# graphD

A Python library for drawing graphs from scratch. This library implements its own rendering system without relying on external drawing libraries.

## Features

- Pure Python implementation, no external dependencies
- Custom rendering engine with a force-directed layout algorithm
- Support for node and edge attributes (color, size, labels, etc.)
- Built from scratch, every pixel calculated individually
- **NEW:** Support for directed edges with arrowheads
- **NEW:** Various line styles (solid, dashed, dotted)
- **NEW:** BMP file format support
- **NEW:** Factory functions for common graph types
- **NEW:** Methods for graph manipulation (remove nodes/edges, neighbors)
- **NEW:** Data visualizations (histograms, pie charts, heatmaps)
- **NEW:** Multiple charts on one canvas (subplots)
- **NEW:** Animation capabilities for dynamic graphs
- **NEW:** Interactive elements (tooltips, highlights, point labels)

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
g.add_edge('A', 'C', style='dashed')   # Dashed edge

# Render the graph to an image file
image_file = graphD.plot(g, filename="my_graph.bmp")
print(f"Graph image saved to: {image_file}")
```

### Directed Graphs

```python
import graphD

# Create a directed graph
g = graphD.Graph()
g.is_directed = True  # Set the graph to be directed

# Add nodes
g.add_node('A', color='#FF0000')
g.add_node('B', color='#00FF00')
g.add_node('C', color='#0000FF')

# Add directed edges (arrows will be drawn automatically)
g.add_edge('A', 'B')
g.add_edge('B', 'C')
g.add_edge('C', 'A')

# You can also add directed edges to an undirected graph
g2 = graphD.Graph()
g2.add_node('X')
g2.add_node('Y')
g2.add_directed_edge('X', 'Y', color='#FF00FF')  # Explicitly directed edge

graphD.plot(g, "directed_graph.bmp")
```

### Factory Functions

```python
import graphD

# Create common graph types with one line
complete = graphD.create_complete_graph(5)  # Complete graph with 5 nodes
star = graphD.create_star_graph(8)         # Star graph with 8 outer nodes
path = graphD.create_path_graph(10)        # Path with 10 nodes
cycle = graphD.create_cycle_graph(6)       # Cycle with 6 nodes

# Render them
graphD.plot(complete, "complete_graph.bmp")
graphD.plot(star, "star_graph.bmp")
graphD.plot(path, "path_graph.bmp")
graphD.plot(cycle, "cycle_graph.bmp")
```

### Data Visualizations

```python
import graphD

# Create a histogram
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 7]
hist = graphD.Histogram(data, bins=7, title="Sample Histogram", 
                        x_label="Value", y_label="Frequency", color="blue")

# Create and plot a pie chart
pie_data = {"Category A": 25, "Category B": 40, "Category C": 15, "Category D": 20}
pie = graphD.PieChart(pie_data, title="Sample Pie Chart", 
                     colors=["#FF5733", "#33FF57", "#3357FF", "#F3FF33"])

# Create a heatmap
heat_data = [
    [1, 2, 3, 4, 5],
    [2, 4, 6, 8, 10],
    [3, 6, 9, 12, 15],
    [4, 8, 12, 16, 20],
    [5, 10, 15, 20, 25]
]
heatmap = graphD.Heatmap(heat_data, title="Sample Heatmap",
                        x_labels=["A", "B", "C", "D", "E"],
                        y_labels=["V", "W", "X", "Y", "Z"],
                        colormap="default", show_values=True)

# Convert to graph and plot
graphD.plot(hist.to_graph(), "histogram.ppm")
graphD.plot(pie.to_graph(), "pie_chart.ppm")
graphD.plot(heatmap.to_graph(), "heatmap.ppm")
```

### Multiple Charts (Subplots)

```python
import graphD

# Create multiple visualizations
hist = graphD.Histogram([1, 2, 2, 3, 3, 3, 4, 4, 4, 5], title="Histogram")
pie = graphD.PieChart({"A": 30, "B": 40, "C": 30}, title="Pie Chart")

# Create subplot layout (2x2 grid)
subplots = graphD.Subplot(rows=2, cols=2, width=1200, height=1000, 
                        title="Multiple Visualizations", spacing=30)

# Add the visualizations to the subplot
subplots.add_graph(hist.to_graph(), row=0, col=0, title="Data Distribution")
subplots.add_graph(pie.to_graph(), row=0, col=1, title="Data Categories")

# Create a simple graph for another subplot
graph = graphD.Graph()
graph.add_node("A", x=20, y=20)
graph.add_node("B", x=80, y=20)
graph.add_node("C", x=50, y=80)
graph.add_edge("A", "B")
graph.add_edge("B", "C")
graph.add_edge("C", "A")
subplots.add_graph(graph, row=1, col=0, title="Simple Graph")

# Plot the combined visualization
combined_graph = subplots.to_graph()
graphD.plot(combined_graph, "subplots.ppm")
```

### Interactive Elements

```python
import graphD

# Create a basic graph
graph = graphD.Graph()
graph.add_node("A", x=50, y=20, size=10, color="red")
graph.add_node("B", x=20, y=70, size=10, color="blue")
graph.add_edge("A", "B")

# Make it interactive
ig = graphD.InteractiveGraph(graph)

# Add tooltips
ig.add_tooltip("A", "Node A: Important node with detailed information")

# Add highlights on hover
ig.add_highlight("A", color="yellow", thickness=3, glow=True)

# Add always-visible point labels
ig.add_point_label("B", "Node B", position="top", always_visible=True)

# Get the enhanced graph and plot
interactive_graph = ig.get_graph()
graphD.plot(interactive_graph, "interactive.ppm")
```

### Animation

```python
import graphD

# Create initial empty graph
graph = graphD.Graph()

# Create animation builder
builder = graphD.AnimationBuilder(graph, title="Growing Graph", loop=True, fps=10)

# Add nodes one by one
builder.add_node("A", x=50, y=50, color="red", duration=0.5)
builder.add_node("B", x=150, y=50, color="blue", duration=0.5)
builder.add_node("C", x=50, y=150, color="green", duration=0.5)

# Add edges one by one
builder.add_edge("A", "B", color="gray", duration=0.3)
builder.add_edge("B", "C", color="gray", duration=0.3)
builder.add_edge("C", "A", color="gray", duration=0.3)

# Change node properties
builder.update_node("A", color="yellow", size=15, duration=0.5)

# Get the animation and render it
animation = builder.get_animation()
animation_graph = animation.to_graph()
graphD.plot(animation_graph, "animation.ppm")
```

### Node and Edge Management

```python
import graphD

g = graphD.Graph()

# Add nodes
g.add_node('A')
g.add_node('B')
g.add_node('C')
g.add_edge('A', 'B')
g.add_edge('B', 'C')

# Check existence and neighbors
print(g.has_edge('A', 'B'))        # True
print(g.get_neighbors('B'))        # ['A', 'C']

# Remove node (automatically removes connected edges)
g.remove_node('B')
print(g.get_nodes())               # {'A': {}, 'C': {}}
print(g.get_edges())               # [] (No edges remain)

# Get graph info
print(g.node_count())              # 2
print(g.edge_count())              # 0
```

### Advanced Usage

You can directly use the renderer components for more control:

```python
from graphD import Graph, GraphRenderer, Color

# Create graph and add elements
graph = Graph()
graph.add_node('1', color='#FF0000')
graph.add_node('2', color='#00FF00')
graph.add_directed_edge('1', '2', style='dotted')

# Create a custom renderer
renderer = GraphRenderer(width=1200, height=900)
renderer.node_color = Color(0, 0, 255)  # Default blue for nodes
renderer.edge_color = Color(0, 0, 0)    # Default black for edges
renderer.arrow_size = 15                # Larger arrowheads
renderer.render(graph, "custom_graph.bmp")
```

## Output Formats

The library natively supports:
- **PPM**: Simple portable pixmap format
- **BMP**: Windows bitmap format

For PNG/JPEG formats, you'll need to use external conversion tools or libraries.

## How It Works

The library uses a force-directed layout algorithm to position nodes in a visually appealing way:

1. Nodes are initially arranged in a circle
2. Repulsive forces push nodes away from each other
3. Attractive forces pull connected nodes toward each other
4. After several iterations, nodes settle into a balanced layout

Drawing is performed using basic algorithms:
- Bresenham's line algorithm for edges
- Bresenham's circle algorithm for nodes
- Pattern-based drawing for dashed and dotted lines
- Custom arrowhead drawing for directed edges

The new visualization features are built on the same underlying Graph object, allowing for a unified interface across all visualization types.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

[MIT](LICENSE) 