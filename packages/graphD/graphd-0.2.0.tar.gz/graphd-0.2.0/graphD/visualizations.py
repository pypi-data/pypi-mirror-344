from .core import Graph
import math
from typing import List, Dict, Tuple, Optional, Union, Any

class Histogram:
    """Class for creating and rendering histograms."""
    
    def __init__(self, data: List[float], bins: int = 10, 
                 title: str = "Histogram", x_label: str = "Value", 
                 y_label: str = "Frequency", color: str = "blue"):
        """
        Initialize a histogram visualization.
        
        Args:
            data: List of numeric values to create histogram from
            bins: Number of bins to divide data into
            title: Title of the histogram
            x_label: Label for x-axis
            y_label: Label for y-axis
            color: Color of the bars
        """
        self.data = data
        self.bins = bins
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.color = color
        self._calculate_bins()
        
    def _calculate_bins(self):
        """Calculate histogram bins and frequencies."""
        if not self.data:
            self.bin_edges = []
            self.frequencies = []
            return
            
        min_val = min(self.data)
        max_val = max(self.data)
        
        # Handle case where all values are the same
        if min_val == max_val:
            self.bin_edges = [min_val - 0.5, min_val + 0.5]
            self.frequencies = [len(self.data)]
            return
            
        bin_width = (max_val - min_val) / self.bins
        self.bin_edges = [min_val + i * bin_width for i in range(self.bins + 1)]
        
        # Initialize frequencies
        self.frequencies = [0] * self.bins
        
        # Count values in each bin
        for value in self.data:
            # Special case for the maximum value
            if value == max_val:
                self.frequencies[self.bins - 1] += 1
                continue
                
            bin_index = int((value - min_val) / bin_width)
            self.frequencies[bin_index] += 1
    
    def to_graph(self) -> Graph:
        """Convert histogram to a Graph representation for rendering."""
        graph = Graph()
        
        # Add nodes for each bin rectangle (corners)
        for i in range(self.bins):
            left = self.bin_edges[i]
            right = self.bin_edges[i+1]
            height = self.frequencies[i]
            
            # Bottom corners
            graph.add_node(f"bin_{i}_bl", x=left, y=0, type="histogram_point")
            graph.add_node(f"bin_{i}_br", x=right, y=0, type="histogram_point")
            
            # Top corners
            graph.add_node(f"bin_{i}_tl", x=left, y=height, type="histogram_point")
            graph.add_node(f"bin_{i}_tr", x=right, y=height, type="histogram_point")
            
            # Add edges to form rectangle
            graph.add_edge(f"bin_{i}_bl", f"bin_{i}_br", type="histogram_edge", color=self.color)
            graph.add_edge(f"bin_{i}_br", f"bin_{i}_tr", type="histogram_edge", color=self.color)
            graph.add_edge(f"bin_{i}_tr", f"bin_{i}_tl", type="histogram_edge", color=self.color)
            graph.add_edge(f"bin_{i}_tl", f"bin_{i}_bl", type="histogram_edge", color=self.color)
            
            # Fill attribute
            for edge in graph.get_edges():
                if "type" in edge[2] and edge[2]["type"] == "histogram_edge":
                    edge[2]["fill"] = True
        
        # Add metadata for rendering
        graph.add_node("__meta__", type="metadata", 
                       chart_type="histogram", 
                       title=self.title,
                       x_label=self.x_label,
                       y_label=self.y_label,
                       bin_edges=self.bin_edges,
                       frequencies=self.frequencies)
        
        return graph

class PieChart:
    """Class for creating and rendering pie charts."""
    
    def __init__(self, data: Dict[str, float], title: str = "Pie Chart", 
                 colors: Optional[List[str]] = None, start_angle: float = 0,
                 explode: Optional[Dict[str, float]] = None, donut: bool = False,
                 donut_ratio: float = 0.5):
        """
        Initialize a pie chart visualization.
        
        Args:
            data: Dictionary mapping labels to values
            title: Title of the pie chart
            colors: List of colors for each slice (will cycle if fewer colors than slices)
            start_angle: Starting angle in degrees
            explode: Dictionary mapping labels to explosion distance (0.0-1.0)
            donut: Whether to render as a donut chart
            donut_ratio: Inner radius ratio for donut charts (0.0-1.0)
        """
        self.data = data
        self.title = title
        self.colors = colors or ["red", "green", "blue", "yellow", "purple", "orange", "cyan"]
        self.start_angle = start_angle
        self.explode = explode or {}
        self.donut = donut
        self.donut_ratio = max(0.0, min(0.9, donut_ratio))  # Clamp between 0 and 0.9
        
        # Calculate total and percentages
        self.total = sum(data.values())
        if self.total == 0:
            self.percentages = {k: 0 for k in data}
        else:
            self.percentages = {k: v / self.total for k, v in data.items()}
    
    def to_graph(self) -> Graph:
        """Convert pie chart to a Graph representation for rendering."""
        graph = Graph()
        
        # Define center and radius
        center_x, center_y = 0, 0
        radius = 100
        
        # Add center node
        graph.add_node("center", x=center_x, y=center_y, type="pie_center")
        
        # Convert start angle to radians and initialize current angle
        current_angle = math.radians(self.start_angle)
        
        # Generate nodes and edges for each slice
        for i, (label, value) in enumerate(self.data.items()):
            if value <= 0:  # Skip zero or negative values
                continue
                
            color = self.colors[i % len(self.colors)]
            angle_size = 2 * math.pi * self.percentages[label]
            
            # Calculate explosion offset if any
            explosion = self.explode.get(label, 0.0) * radius * 0.2
            explosion_x = explosion * math.cos(current_angle + angle_size / 2)
            explosion_y = explosion * math.sin(current_angle + angle_size / 2)
            
            # Add nodes for start and end points of the arc
            start_x = center_x + explosion_x + radius * math.cos(current_angle)
            start_y = center_y + explosion_y + radius * math.sin(current_angle)
            end_x = center_x + explosion_x + radius * math.cos(current_angle + angle_size)
            end_y = center_y + explosion_y + radius * math.sin(current_angle + angle_size)
            
            slice_center_x = center_x + explosion_x
            slice_center_y = center_y + explosion_y
            
            # Add nodes
            center_node = f"slice_{i}_center"
            start_node = f"slice_{i}_start"
            end_node = f"slice_{i}_end"
            
            graph.add_node(center_node, x=slice_center_x, y=slice_center_y, type="pie_slice_center")
            graph.add_node(start_node, x=start_x, y=start_y, type="pie_slice_point")
            graph.add_node(end_node, x=end_x, y=end_y, type="pie_slice_point")
            
            # Add slice metadata node
            graph.add_node(f"slice_{i}_meta", 
                          type="pie_slice_meta", 
                          label=label, 
                          value=value, 
                          percentage=self.percentages[label],
                          start_angle=current_angle,
                          end_angle=current_angle + angle_size,
                          color=color)
            
            # Add edges
            graph.add_edge(center_node, start_node, 
                         type="pie_radius", color=color, fill=True)
            graph.add_edge(center_node, end_node, 
                         type="pie_radius", color=color, fill=True)
            graph.add_edge(start_node, end_node, 
                         type="pie_arc", color=color, fill=True, 
                         is_arc=True, arc_center=(slice_center_x, slice_center_y), 
                         radius=radius, start_angle=current_angle, 
                         end_angle=current_angle + angle_size)
            
            # Handle donut if enabled
            if self.donut:
                inner_radius = radius * self.donut_ratio
                inner_start_x = slice_center_x + inner_radius * math.cos(current_angle)
                inner_start_y = slice_center_y + inner_radius * math.sin(current_angle)
                inner_end_x = slice_center_x + inner_radius * math.cos(current_angle + angle_size)
                inner_end_y = slice_center_y + inner_radius * math.sin(current_angle + angle_size)
                
                inner_start_node = f"slice_{i}_inner_start"
                inner_end_node = f"slice_{i}_inner_end"
                
                graph.add_node(inner_start_node, x=inner_start_x, y=inner_start_y, 
                              type="pie_inner_point")
                graph.add_node(inner_end_node, x=inner_end_x, y=inner_end_y, 
                              type="pie_inner_point")
                
                # Connect inner arc
                graph.add_edge(inner_start_node, inner_end_node, 
                              type="pie_inner_arc", color=color, fill=True,
                              is_arc=True, arc_center=(slice_center_x, slice_center_y),
                              radius=inner_radius, start_angle=current_angle,
                              end_angle=current_angle + angle_size)
                
                # Connect inner to outer
                graph.add_edge(start_node, inner_start_node, 
                              type="pie_connector", color=color, fill=True)
                graph.add_edge(end_node, inner_end_node, 
                              type="pie_connector", color=color, fill=True)
            
            # Update angle for next slice
            current_angle += angle_size
        
        # Add metadata for rendering
        graph.add_node("__meta__", type="metadata", 
                      chart_type="pie", 
                      title=self.title,
                      is_donut=self.donut,
                      donut_ratio=self.donut_ratio,
                      labels=list(self.data.keys()),
                      values=list(self.data.values()),
                      percentages=[self.percentages[k] for k in self.data.keys()],
                      colors=[self.colors[i % len(self.colors)] for i in range(len(self.data))])
        
        return graph

class Heatmap:
    """Class for creating and rendering heatmaps."""
    
    def __init__(self, data: List[List[float]], 
                 title: str = "Heatmap",
                 x_labels: Optional[List[str]] = None, 
                 y_labels: Optional[List[str]] = None,
                 colormap: str = "default", 
                 show_values: bool = True,
                 min_value: Optional[float] = None,
                 max_value: Optional[float] = None):
        """
        Initialize a heatmap visualization.
        
        Args:
            data: 2D list of numeric values
            title: Title of the heatmap
            x_labels: Labels for the x-axis
            y_labels: Labels for the y-axis
            colormap: Color scheme to use
            show_values: Whether to display values in cells
            min_value: Minimum value for color scaling (auto-detected if None)
            max_value: Maximum value for color scaling (auto-detected if None)
        """
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0
        self.title = title
        self.x_labels = x_labels or [str(i) for i in range(self.cols)]
        self.y_labels = y_labels or [str(i) for i in range(self.rows)]
        self.colormap = colormap
        self.show_values = show_values
        
        # Ensure consistent dimensions
        if len(self.x_labels) != self.cols:
            self.x_labels = self.x_labels[:self.cols] if len(self.x_labels) > self.cols else self.x_labels + [str(i) for i in range(len(self.x_labels), self.cols)]
        
        if len(self.y_labels) != self.rows:
            self.y_labels = self.y_labels[:self.rows] if len(self.y_labels) > self.rows else self.y_labels + [str(i) for i in range(len(self.y_labels), self.rows)]
        
        # Find min and max values for scaling if not provided
        all_values = [val for row in data for val in row if val is not None]
        self.min_value = min_value if min_value is not None and all_values else min(all_values) if all_values else 0
        self.max_value = max_value if max_value is not None and all_values else max(all_values) if all_values else 1
    
    def _get_color(self, value: float) -> str:
        """Get color based on value and chosen colormap."""
        if value is None:
            return "transparent"
            
        # Normalize value between 0 and 1
        normalized = max(0, min(1, (value - self.min_value) / (self.max_value - self.min_value) if self.max_value != self.min_value else 0.5))
        
        # Different colormaps
        if self.colormap == "default":
            # Blue to red gradient
            r = int(normalized * 255)
            b = int((1 - normalized) * 255)
            g = 0
            return f"#{r:02x}{g:02x}{b:02x}"
        elif self.colormap == "grayscale":
            # Black to white gradient
            v = int(normalized * 255)
            return f"#{v:02x}{v:02x}{v:02x}"
        elif self.colormap == "viridis":
            # Approximate viridis colormap (simplified)
            if normalized < 0.25:
                return "#440154"  # Dark purple
            elif normalized < 0.5:
                return "#3b528b"  # Purple-blue
            elif normalized < 0.75:
                return "#21918c"  # Green-blue
            else:
                return "#fde725"  # Yellow
        else:
            # Default fallback
            return f"rgb({int(normalized * 255)}, 0, {int((1 - normalized) * 255)})"
    
    def to_graph(self) -> Graph:
        """Convert heatmap to a Graph representation for rendering."""
        graph = Graph()
        
        cell_width = 50
        cell_height = 50
        
        # Create cells
        for row in range(self.rows):
            for col in range(self.cols):
                # Cell corners
                top_left = f"cell_{row}_{col}_tl"
                top_right = f"cell_{row}_{col}_tr"
                bottom_left = f"cell_{row}_{col}_bl"
                bottom_right = f"cell_{row}_{col}_br"
                
                # Calculate coordinates
                x_left = col * cell_width
                x_right = (col + 1) * cell_width
                y_top = row * cell_height
                y_bottom = (row + 1) * cell_height
                
                # Add nodes for corners
                graph.add_node(top_left, x=x_left, y=y_top, type="heatmap_point")
                graph.add_node(top_right, x=x_right, y=y_top, type="heatmap_point")
                graph.add_node(bottom_left, x=x_left, y=y_bottom, type="heatmap_point")
                graph.add_node(bottom_right, x=x_right, y=y_bottom, type="heatmap_point")
                
                # Get value and color
                value = self.data[row][col]
                color = self._get_color(value)
                
                # Add cell value node (for center of cell)
                cell_center = f"cell_{row}_{col}_center"
                graph.add_node(cell_center, 
                              x=(x_left + x_right) / 2, 
                              y=(y_top + y_bottom) / 2,
                              type="heatmap_cell",
                              value=value,
                              color=color,
                              row=row,
                              col=col,
                              x_label=self.x_labels[col],
                              y_label=self.y_labels[row],
                              show_value=self.show_values)
                
                # Add edges to form cell
                graph.add_edge(top_left, top_right, type="heatmap_edge", color=color, fill=True)
                graph.add_edge(top_right, bottom_right, type="heatmap_edge", color=color, fill=True)
                graph.add_edge(bottom_right, bottom_left, type="heatmap_edge", color=color, fill=True)
                graph.add_edge(bottom_left, top_left, type="heatmap_edge", color=color, fill=True)
        
        # Add metadata for rendering
        graph.add_node("__meta__", type="metadata", 
                      chart_type="heatmap", 
                      title=self.title,
                      x_labels=self.x_labels,
                      y_labels=self.y_labels,
                      rows=self.rows,
                      cols=self.cols,
                      min_value=self.min_value,
                      max_value=self.max_value,
                      colormap=self.colormap,
                      show_values=self.show_values)
        
        return graph 