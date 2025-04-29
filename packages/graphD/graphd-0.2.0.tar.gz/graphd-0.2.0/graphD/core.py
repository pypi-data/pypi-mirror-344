# Placeholder for graph drawing logic

class Graph:
    """Represents a graph with nodes and edges."""
    def __init__(self):
        self._nodes = {}  # Dictionary to store nodes {node_id: {attributes}}
        self._edges = []  # List to store edges [(node1_id, node2_id, {attributes})]
        self._neighbors_cache = {}  # Cache for fast neighbor lookups
        self._directed = False  # Default to undirected graph
    
    @property
    def is_directed(self):
        """Returns whether the graph is directed."""
        return self._directed
    
    @is_directed.setter
    def is_directed(self, value):
        """Sets whether the graph is directed."""
        self._directed = bool(value)
    
    def add_node(self, node_id, **kwargs):
        """Adds a node to the graph.

        Args:
            node_id: The unique identifier for the node.
            **kwargs: Arbitrary keyword arguments representing node attributes (e.g., color='red', size=10).
        """
        if node_id in self._nodes:
            # Optionally update existing node attributes or raise an error
            print(f"Warning: Node {node_id} already exists. Updating attributes.")
            self._nodes[node_id].update(kwargs)
        else:
            self._nodes[node_id] = kwargs
            # Initialize empty neighbors list for this node
            self._neighbors_cache[node_id] = []

    def remove_node(self, node_id):
        """Removes a node and all its connected edges from the graph.
        
        Args:
            node_id: The ID of the node to remove.
            
        Returns:
            bool: True if node was removed, False if node didn't exist.
        """
        if node_id not in self._nodes:
            return False
        
        # Remove the node
        del self._nodes[node_id]
        
        # Remove all edges connected to this node
        self._edges = [edge for edge in self._edges 
                       if edge[0] != node_id and edge[1] != node_id]
        
        # Update neighbors cache
        del self._neighbors_cache[node_id]
        for nid in self._neighbors_cache:
            self._neighbors_cache[nid] = [n for n in self._neighbors_cache[nid] if n != node_id]
        
        return True

    def add_edge(self, node1_id, node2_id, **kwargs):
        """Adds an edge between two nodes.

        Args:
            node1_id: The ID of the starting node.
            node2_id: The ID of the ending node.
            **kwargs: Arbitrary keyword arguments representing edge attributes (e.g., weight=5, style='dashed').

        Raises:
            ValueError: If either node does not exist in the graph.
        """
        if node1_id not in self._nodes:
            raise ValueError(f"Node {node1_id} does not exist.")
        if node2_id not in self._nodes:
            raise ValueError(f"Node {node2_id} does not exist.")

        # Set directed attribute based on graph's setting
        if self._directed and 'directed' not in kwargs:
            kwargs['directed'] = True
            
        # Add the edge
        self._edges.append((node1_id, node2_id, kwargs))
        
        # Update neighbors cache
        self._neighbors_cache[node1_id].append(node2_id)
        if not self._directed and not kwargs.get('directed', False):
            # For undirected edges, add both directions to neighbors cache
            self._neighbors_cache[node2_id].append(node1_id)
    
    def add_directed_edge(self, from_node_id, to_node_id, **kwargs):
        """Adds a directed edge from one node to another.
        
        Args:
            from_node_id: The ID of the source node.
            to_node_id: The ID of the target node.
            **kwargs: Arbitrary keyword arguments representing edge attributes.
            
        Raises:
            ValueError: If either node does not exist in the graph.
        """
        kwargs['directed'] = True
        self.add_edge(from_node_id, to_node_id, **kwargs)
    
    def remove_edge(self, node1_id, node2_id, directed=None):
        """Removes an edge between two nodes.
        
        Args:
            node1_id: The ID of the first node.
            node2_id: The ID of the second node.
            directed: If None, matches graph setting. If True, only removes edge from node1 to node2.
                     If False, removes edges in both directions.
                     
        Returns:
            bool: True if at least one edge was removed, False otherwise.
        """
        if directed is None:
            directed = self._directed
        
        found = False
        new_edges = []
        
        for edge in self._edges:
            src, dst, attrs = edge
            is_match = False
            
            if directed:
                # Only match the specific direction
                is_match = (src == node1_id and dst == node2_id)
            else:
                # Match either direction
                is_match = ((src == node1_id and dst == node2_id) or 
                           (src == node2_id and dst == node1_id))
            
            if is_match:
                found = True
                # Update neighbors cache
                if node1_id in self._neighbors_cache:
                    self._neighbors_cache[node1_id] = [n for n in self._neighbors_cache[node1_id] 
                                                    if n != node2_id]
                if node2_id in self._neighbors_cache:
                    self._neighbors_cache[node2_id] = [n for n in self._neighbors_cache[node2_id] 
                                                    if n != node1_id]
            else:
                new_edges.append(edge)
        
        self._edges = new_edges
        return found
    
    def get_neighbors(self, node_id):
        """Returns a list of node IDs that are neighbors of the given node.
        
        Args:
            node_id: The ID of the node to get neighbors for.
            
        Returns:
            list: List of neighbor node IDs.
            
        Raises:
            ValueError: If the node does not exist.
        """
        if node_id not in self._nodes:
            raise ValueError(f"Node {node_id} does not exist.")
        
        return self._neighbors_cache[node_id]
    
    def has_edge(self, node1_id, node2_id, directed=None):
        """Checks if an edge exists between two nodes.
        
        Args:
            node1_id: The ID of the first node.
            node2_id: The ID of the second node.
            directed: If None, matches graph setting. If True, checks only from node1 to node2.
                     If False, checks both directions.
                     
        Returns:
            bool: True if the edge exists, False otherwise.
        """
        if directed is None:
            directed = self._directed
            
        for edge in self._edges:
            src, dst, _ = edge
            if directed:
                if src == node1_id and dst == node2_id:
                    return True
            else:
                if (src == node1_id and dst == node2_id) or (src == node2_id and dst == node1_id):
                    return True
        
        return False
    
    def get_nodes(self):
        """Returns a dictionary of all nodes and their attributes."""
        return self._nodes

    def get_edges(self):
        """Returns a list of all edges and their attributes."""
        return self._edges
    
    def clear(self):
        """Removes all nodes and edges from the graph."""
        self._nodes = {}
        self._edges = []
        self._neighbors_cache = {}
    
    def node_count(self):
        """Returns the number of nodes in the graph."""
        return len(self._nodes)
    
    def edge_count(self):
        """Returns the number of edges in the graph."""
        return len(self._edges)
    
    def to_dict(self):
        """Returns a dictionary representation of the graph."""
        return {
            "directed": self._directed,
            "nodes": self._nodes,
            "edges": self._edges
        }
    
    @classmethod
    def from_dict(cls, data):
        """Creates a Graph instance from a dictionary.
        
        Args:
            data: Dictionary with "nodes" and "edges" keys.
            
        Returns:
            Graph: A new Graph instance.
        """
        graph = cls()
        graph.is_directed = data.get("directed", False)
        
        # Add nodes
        for node_id, attrs in data.get("nodes", {}).items():
            graph.add_node(node_id, **attrs)
            
        # Add edges
        for edge in data.get("edges", []):
            node1_id, node2_id, attrs = edge
            graph.add_edge(node1_id, node2_id, **attrs)
            
        return graph

    def __str__(self):
        return f"Graph(Nodes: {len(self._nodes)}, Edges: {len(self._edges)}, Directed: {self._directed})"


def plot(graph: Graph, filename: str = "graph.ppm", width: int = 800, height: int = 600, 
         theme: str = "default", title: str = None, antialiasing: bool = True, 
         show_grid: bool = False, edge_thickness: int = 1):
    """
    Render the graph to an image file using the PixelD engine.
    
    Args:
        graph: The Graph object to render.
        filename: The name of the output file (default: "graph.ppm").
        width: The width of the output image (default: 800).
        height: The height of the output image (default: 600).
        theme: Visual theme to use ("default", "dark", "neon", "pastel", "monochrome").
        title: Optional title to display on the graph.
        antialiasing: Whether to use antialiasing for smoother rendering (default: True).
        show_grid: Whether to show a grid in the background (default: False).
        edge_thickness: Thickness of edges in pixels (default: 1).
        
    Returns:
        The path to the generated image file.
    """
    from .renderer import GraphRenderer
    
    # Print basic graph information
    print(f"Rendering graph with {len(graph.get_nodes())} nodes and {len(graph.get_edges())} edges.")
    
    # Create a renderer and configure it
    renderer = GraphRenderer(width=width, height=height, theme=theme)
    
    if title:
        renderer.set_title(title)
    
    renderer.antialiasing = antialiasing
    renderer.grid_visible = show_grid
    renderer.edge_thickness = edge_thickness
    
    # Render the graph
    rendered_file = renderer.render(graph, filename)
    
    print(f"Graph rendered to {rendered_file}")
    return rendered_file

def plot_to_base64(graph: Graph, width: int = 800, height: int = 600, theme: str = "default", 
                 title: str = None, format: str = "bmp"):
    """
    Render the graph and return a base64-encoded data URL string.
    
    Args:
        graph: The Graph object to render.
        width: The width of the output image (default: 800).
        height: The height of the output image (default: 600).
        theme: Visual theme to use ("default", "dark", "neon", "pastel", "monochrome").
        title: Optional title to display on the graph.
        format: Output format ("bmp" or "ppm").
        
    Returns:
        A base64-encoded data URL string that can be embedded in HTML or displayed in notebooks.
    """
    from .renderer import GraphRenderer
    
    # Create a renderer and configure it
    renderer = GraphRenderer(width=width, height=height, theme=theme)
    
    if title:
        renderer.set_title(title)
    
    # Render to base64
    return renderer.render_to_base64(graph, format)

# Factory functions to create common graph types
def create_complete_graph(n):
    """Creates a complete graph with n nodes."""
    graph = Graph()
    
    # Add nodes
    for i in range(n):
        graph.add_node(str(i))
    
    # Add edges between all pairs of nodes
    for i in range(n):
        for j in range(i+1, n):
            graph.add_edge(str(i), str(j))
    
    return graph

def create_star_graph(n):
    """Creates a star graph with n outer nodes and 1 center node."""
    graph = Graph()
    
    # Add center node
    graph.add_node("center")
    
    # Add outer nodes and connect to center
    for i in range(n):
        node_id = f"node_{i}"
        graph.add_node(node_id)
        graph.add_edge("center", node_id)
    
    return graph

def create_path_graph(n):
    """Creates a path graph with n nodes connected in sequence."""
    graph = Graph()
    
    # Add nodes
    for i in range(n):
        graph.add_node(str(i))
    
    # Connect nodes in sequence
    for i in range(n-1):
        graph.add_edge(str(i), str(i+1))
    
    return graph

def create_cycle_graph(n):
    """Creates a cycle graph with n nodes connected in a cycle."""
    graph = create_path_graph(n)
    
    # Connect the last node to the first to form a cycle
    if n > 2:
        graph.add_edge(str(n-1), "0")
    
    return graph 