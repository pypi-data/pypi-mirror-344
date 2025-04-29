from .core import Graph
from typing import List, Dict, Tuple, Optional, Union, Any

class Subplot:
    """Class for creating multiple graphs on a single canvas."""
    
    def __init__(self, rows: int = 1, cols: int = 1, width: int = 800, height: int = 600,
                 title: str = None, spacing: int = 20, shared_axes: bool = False):
        """
        Initialize a subplot layout.
        
        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid
            width: Total width of the canvas
            height: Total height of the canvas
            title: Main title for the entire plot
            spacing: Spacing between subplots in pixels
            shared_axes: Whether subplots should share axis scales
        """
        self.rows = max(1, rows)
        self.cols = max(1, cols)
        self.width = max(100, width)
        self.height = max(100, height)
        self.title = title
        self.spacing = max(0, spacing)
        self.shared_axes = shared_axes
        
        # Calculate subplot dimensions
        self.subplot_width = (self.width - (self.cols + 1) * self.spacing) / self.cols
        self.subplot_height = (self.height - (self.rows + 1) * self.spacing) / self.rows
        
        # Initialize subplot grid
        self.subplots: Dict[Tuple[int, int], Optional[Graph]] = {}
        for row in range(self.rows):
            for col in range(self.cols):
                self.subplots[(row, col)] = None
                
        # Track metadata for each subplot
        self.subplot_metadata: Dict[Tuple[int, int], Dict[str, Any]] = {}
        
    def add_graph(self, graph: Graph, row: int, col: int, title: str = None, 
                  x_label: str = None, y_label: str = None):
        """
        Add a graph to a specific position in the grid.
        
        Args:
            graph: The Graph object to add
            row: Row index (0-based)
            col: Column index (0-based)
            title: Title for this subplot
            x_label: Label for x-axis
            y_label: Label for y-axis
            
        Raises:
            ValueError: If the position is out of bounds
        """
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise ValueError(f"Position ({row}, {col}) is out of bounds for grid size {self.rows}x{self.cols}")
        
        self.subplots[(row, col)] = graph
        
        # Store metadata
        self.subplot_metadata[(row, col)] = {
            "title": title,
            "x_label": x_label,
            "y_label": y_label
        }
    
    def set_title(self, title: str):
        """Set the main title for the entire plot."""
        self.title = title
    
    def to_graph(self) -> Graph:
        """Combine all subplots into a single Graph for rendering."""
        combined_graph = Graph()
        
        # Add metadata node for the entire subplot
        combined_graph.add_node("__meta__", 
                               type="metadata",
                               chart_type="subplot",
                               rows=self.rows,
                               cols=self.cols,
                               width=self.width,
                               height=self.height,
                               spacing=self.spacing,
                               shared_axes=self.shared_axes,
                               title=self.title)
        
        # Process each subplot
        for (row, col), graph in self.subplots.items():
            if graph is None:
                continue
                
            # Calculate the position of this subplot
            x_offset = self.spacing + col * (self.subplot_width + self.spacing)
            y_offset = self.spacing + row * (self.subplot_height + self.spacing)
            
            # Add subplot metadata
            metadata = self.subplot_metadata.get((row, col), {})
            combined_graph.add_node(f"subplot_{row}_{col}_meta",
                                  type="subplot_meta",
                                  row=row,
                                  col=col,
                                  x_offset=x_offset,
                                  y_offset=y_offset,
                                  width=self.subplot_width,
                                  height=self.subplot_height,
                                  title=metadata.get("title"),
                                  x_label=metadata.get("x_label"),
                                  y_label=metadata.get("y_label"))
            
            # Add boundary nodes for the subplot area
            combined_graph.add_node(f"subplot_{row}_{col}_tl", 
                                  x=x_offset, y=y_offset, 
                                  type="subplot_corner")
            combined_graph.add_node(f"subplot_{row}_{col}_tr", 
                                  x=x_offset + self.subplot_width, y=y_offset, 
                                  type="subplot_corner")
            combined_graph.add_node(f"subplot_{row}_{col}_bl", 
                                  x=x_offset, y=y_offset + self.subplot_height, 
                                  type="subplot_corner")
            combined_graph.add_node(f"subplot_{row}_{col}_br", 
                                  x=x_offset + self.subplot_width, y=y_offset + self.subplot_height, 
                                  type="subplot_corner")
            
            # Add border edges
            combined_graph.add_edge(f"subplot_{row}_{col}_tl", f"subplot_{row}_{col}_tr", 
                                  type="subplot_border")
            combined_graph.add_edge(f"subplot_{row}_{col}_tr", f"subplot_{row}_{col}_br", 
                                  type="subplot_border")
            combined_graph.add_edge(f"subplot_{row}_{col}_br", f"subplot_{row}_{col}_bl", 
                                  type="subplot_border")
            combined_graph.add_edge(f"subplot_{row}_{col}_bl", f"subplot_{row}_{col}_tl", 
                                  type="subplot_border")
            
            # Get all the nodes and edges from the subplot graph
            for node_id, attrs in graph.get_nodes().items():
                # Skip metadata nodes from the original graph
                if node_id == "__meta__":
                    continue
                    
                # Create a new unique ID for this node in the combined graph
                combined_node_id = f"subplot_{row}_{col}_{node_id}"
                
                # Transform coordinates to fit in the subplot area
                new_attrs = attrs.copy()
                if 'x' in new_attrs and 'y' in new_attrs:
                    # Scale the coordinates to fit the subplot dimensions
                    # Assuming original graph is in a standard 0-100 coordinate space
                    # This will need adjustment based on the actual coordinate system used
                    x_scale = self.subplot_width / 100
                    y_scale = self.subplot_height / 100
                    
                    new_attrs['x'] = x_offset + new_attrs['x'] * x_scale
                    new_attrs['y'] = y_offset + new_attrs['y'] * y_scale
                    
                # Add subplot info to the node
                new_attrs['subplot_row'] = row
                new_attrs['subplot_col'] = col
                
                # Add the transformed node
                combined_graph.add_node(combined_node_id, **new_attrs)
            
            # Add transformed edges
            for src, dst, attrs in graph.get_edges():
                combined_src = f"subplot_{row}_{col}_{src}"
                combined_dst = f"subplot_{row}_{col}_{dst}"
                
                # Copy edge attributes
                new_attrs = attrs.copy()
                
                # Transform any coordinate-based attributes
                if 'arc_center' in new_attrs:
                    # Transform arc center coordinates
                    x_scale = self.subplot_width / 100
                    y_scale = self.subplot_height / 100
                    
                    cx, cy = new_attrs['arc_center']
                    new_attrs['arc_center'] = (
                        x_offset + cx * x_scale,
                        y_offset + cy * y_scale
                    )
                
                # Scale radius if present
                if 'radius' in new_attrs:
                    radius_scale = min(x_scale, y_scale)
                    new_attrs['radius'] = new_attrs['radius'] * radius_scale
                
                # Add subplot info to the edge
                new_attrs['subplot_row'] = row
                new_attrs['subplot_col'] = col
                
                # Add the transformed edge
                combined_graph.add_edge(combined_src, combined_dst, **new_attrs)
        
        return combined_graph 