from .core import Graph
from typing import List, Dict, Any, Optional, Callable, Union, Tuple

class Frame:
    """Represents a single frame in an animation."""
    
    def __init__(self, graph: Graph, duration: float = 1.0, easing: str = "linear"):
        """
        Initialize an animation frame.
        
        Args:
            graph: The Graph object for this frame
            duration: Duration of this frame in seconds
            easing: Easing function to use for transition to this frame
        """
        self.graph = graph
        self.duration = max(0.01, duration)  # Minimum duration of 0.01 seconds
        self.easing = easing


class Animation:
    """Class for creating graph animations."""
    
    def __init__(self, title: str = "Graph Animation", loop: bool = False, 
                 fps: int = 30, width: int = 800, height: int = 600):
        """
        Initialize a graph animation.
        
        Args:
            title: Title of the animation
            loop: Whether to loop the animation
            fps: Frames per second
            width: Width of the animation in pixels
            height: Height of the animation in pixels
        """
        self.title = title
        self.loop = loop
        self.fps = max(1, fps)  # Minimum 1 FPS
        self.width = width
        self.height = height
        self.frames: List[Frame] = []
        
    def add_frame(self, graph: Graph, duration: float = 1.0, easing: str = "linear") -> 'Animation':
        """
        Add a frame to the animation.
        
        Args:
            graph: The Graph object for this frame
            duration: Duration of this frame in seconds
            easing: Easing function to use for transition to this frame
            
        Returns:
            Self for method chaining
        """
        frame = Frame(graph, duration, easing)
        self.frames.append(frame)
        return self
    
    def to_graph(self) -> Graph:
        """
        Convert the animation to a Graph representation for rendering.
        
        Returns:
            Graph representation of the animation
        """
        if not self.frames:
            raise ValueError("Animation must have at least one frame")
        
        # Use the first frame as the base graph
        base_graph = self.frames[0].graph
        
        # Create a new combined graph
        animation_graph = Graph()
        
        # Add metadata
        animation_graph.add_node("__meta__", 
                               type="metadata",
                               chart_type="animation",
                               title=self.title,
                               loop=self.loop,
                               fps=self.fps,
                               width=self.width,
                               height=self.height,
                               frame_count=len(self.frames))
        
        # Process each frame
        for i, frame in enumerate(self.frames):
            # Add frame metadata
            animation_graph.add_node(f"frame_{i}_meta", 
                                   type="frame_meta",
                                   index=i,
                                   duration=frame.duration,
                                   easing=frame.easing)
            
            # Get the graph for this frame
            frame_graph = frame.graph
            
            # Add all nodes from this frame with frame index
            for node_id, attrs in frame_graph.get_nodes().items():
                if node_id == "__meta__":
                    continue
                    
                # Create a new unique ID for this node
                frame_node_id = f"frame_{i}_{node_id}"
                
                # Copy node attributes and add frame index
                new_attrs = attrs.copy()
                new_attrs["frame_index"] = i
                
                # Add the node to the animation graph
                animation_graph.add_node(frame_node_id, **new_attrs)
            
            # Add all edges from this frame with frame index
            for src, dst, attrs in frame_graph.get_edges():
                frame_src = f"frame_{i}_{src}"
                frame_dst = f"frame_{i}_{dst}"
                
                # Copy edge attributes and add frame index
                new_attrs = attrs.copy()
                new_attrs["frame_index"] = i
                
                # Add the edge to the animation graph
                animation_graph.add_edge(frame_src, frame_dst, **new_attrs)
            
            # Create transitions between frames (except for the last frame if not looping)
            if i < len(self.frames) - 1 or self.loop:
                next_i = (i + 1) % len(self.frames)
                next_frame = self.frames[next_i]
                
                # Add transition metadata
                animation_graph.add_node(f"transition_{i}_to_{next_i}_meta", 
                                       type="transition_meta",
                                       from_frame=i,
                                       to_frame=next_i,
                                       duration=frame.duration,
                                       easing=frame.easing)
        
        return animation_graph


class AnimationBuilder:
    """Helper class to build animations by incrementally changing a graph."""
    
    def __init__(self, initial_graph: Graph, title: str = "Graph Animation", 
                 loop: bool = False, fps: int = 30, width: int = 800, height: int = 600):
        """
        Initialize an animation builder.
        
        Args:
            initial_graph: The starting graph for the animation
            title: Title of the animation
            loop: Whether to loop the animation
            fps: Frames per second
            width: Width of the animation in pixels
            height: Height of the animation in pixels
        """
        self.animation = Animation(title, loop, fps, width, height)
        self.current_graph = initial_graph.to_dict()  # Store as dict for manipulation
        
        # Add the initial frame
        self.animation.add_frame(initial_graph)
    
    def add_node(self, node_id: str, duration: float = 1.0, easing: str = "linear", **kwargs) -> 'AnimationBuilder':
        """
        Add a new node in the next frame.
        
        Args:
            node_id: The ID of the node to add
            duration: Duration of this frame in seconds
            easing: Easing function to use
            **kwargs: Node attributes
            
        Returns:
            Self for method chaining
        """
        # Create a copy of the current graph state
        new_graph_data = self.current_graph.copy()
        new_nodes = new_graph_data["nodes"].copy()
        
        # Add the new node
        new_nodes[node_id] = kwargs
        
        # Update the graph data
        new_graph_data["nodes"] = new_nodes
        
        # Create a new Graph object from the updated data
        new_graph = Graph.from_dict(new_graph_data)
        
        # Update current state and add frame
        self.current_graph = new_graph_data
        self.animation.add_frame(new_graph, duration, easing)
        
        return self
    
    def update_node(self, node_id: str, duration: float = 1.0, easing: str = "linear", **kwargs) -> 'AnimationBuilder':
        """
        Update an existing node in the next frame.
        
        Args:
            node_id: The ID of the node to update
            duration: Duration of this frame in seconds
            easing: Easing function to use
            **kwargs: Updated node attributes
            
        Returns:
            Self for method chaining
        """
        # Create a copy of the current graph state
        new_graph_data = self.current_graph.copy()
        new_nodes = new_graph_data["nodes"].copy()
        
        # Check if the node exists
        if node_id not in new_nodes:
            raise ValueError(f"Node {node_id} does not exist in the current frame")
        
        # Update the node attributes
        node_attrs = new_nodes[node_id].copy()
        node_attrs.update(kwargs)
        new_nodes[node_id] = node_attrs
        
        # Update the graph data
        new_graph_data["nodes"] = new_nodes
        
        # Create a new Graph object from the updated data
        new_graph = Graph.from_dict(new_graph_data)
        
        # Update current state and add frame
        self.current_graph = new_graph_data
        self.animation.add_frame(new_graph, duration, easing)
        
        return self
    
    def remove_node(self, node_id: str, duration: float = 1.0, easing: str = "linear") -> 'AnimationBuilder':
        """
        Remove a node in the next frame.
        
        Args:
            node_id: The ID of the node to remove
            duration: Duration of this frame in seconds
            easing: Easing function to use
            
        Returns:
            Self for method chaining
        """
        # Create a copy of the current graph state
        new_graph_data = self.current_graph.copy()
        new_nodes = new_graph_data["nodes"].copy()
        new_edges = []
        
        # Check if the node exists
        if node_id not in new_nodes:
            raise ValueError(f"Node {node_id} does not exist in the current frame")
        
        # Remove the node
        del new_nodes[node_id]
        
        # Remove any edges connected to this node
        for edge in new_graph_data["edges"]:
            src, dst, _ = edge
            if src != node_id and dst != node_id:
                new_edges.append(edge)
        
        # Update the graph data
        new_graph_data["nodes"] = new_nodes
        new_graph_data["edges"] = new_edges
        
        # Create a new Graph object from the updated data
        new_graph = Graph.from_dict(new_graph_data)
        
        # Update current state and add frame
        self.current_graph = new_graph_data
        self.animation.add_frame(new_graph, duration, easing)
        
        return self
    
    def add_edge(self, node1_id: str, node2_id: str, duration: float = 1.0, 
                easing: str = "linear", **kwargs) -> 'AnimationBuilder':
        """
        Add a new edge in the next frame.
        
        Args:
            node1_id: The ID of the first node
            node2_id: The ID of the second node
            duration: Duration of this frame in seconds
            easing: Easing function to use
            **kwargs: Edge attributes
            
        Returns:
            Self for method chaining
        """
        # Create a copy of the current graph state
        new_graph_data = self.current_graph.copy()
        new_edges = new_graph_data["edges"].copy()
        
        # Check if both nodes exist
        if node1_id not in new_graph_data["nodes"]:
            raise ValueError(f"Node {node1_id} does not exist in the current frame")
        if node2_id not in new_graph_data["nodes"]:
            raise ValueError(f"Node {node2_id} does not exist in the current frame")
        
        # Add the new edge
        new_edges.append((node1_id, node2_id, kwargs))
        
        # Update the graph data
        new_graph_data["edges"] = new_edges
        
        # Create a new Graph object from the updated data
        new_graph = Graph.from_dict(new_graph_data)
        
        # Update current state and add frame
        self.current_graph = new_graph_data
        self.animation.add_frame(new_graph, duration, easing)
        
        return self
    
    def update_edge(self, node1_id: str, node2_id: str, duration: float = 1.0, 
                   easing: str = "linear", **kwargs) -> 'AnimationBuilder':
        """
        Update an existing edge in the next frame.
        
        Args:
            node1_id: The ID of the first node
            node2_id: The ID of the second node
            duration: Duration of this frame in seconds
            easing: Easing function to use
            **kwargs: Updated edge attributes
            
        Returns:
            Self for method chaining
        """
        # Create a copy of the current graph state
        new_graph_data = self.current_graph.copy()
        new_edges = []
        edge_found = False
        
        # Find and update the edge
        for edge in new_graph_data["edges"]:
            src, dst, attrs = edge
            if (src == node1_id and dst == node2_id) or \
               (not new_graph_data.get("directed", False) and src == node2_id and dst == node1_id):
                # Update edge attributes
                new_attrs = attrs.copy()
                new_attrs.update(kwargs)
                new_edges.append((src, dst, new_attrs))
                edge_found = True
            else:
                new_edges.append(edge)
        
        if not edge_found:
            raise ValueError(f"Edge between {node1_id} and {node2_id} does not exist in the current frame")
        
        # Update the graph data
        new_graph_data["edges"] = new_edges
        
        # Create a new Graph object from the updated data
        new_graph = Graph.from_dict(new_graph_data)
        
        # Update current state and add frame
        self.current_graph = new_graph_data
        self.animation.add_frame(new_graph, duration, easing)
        
        return self
    
    def remove_edge(self, node1_id: str, node2_id: str, duration: float = 1.0, 
                   easing: str = "linear") -> 'AnimationBuilder':
        """
        Remove an edge in the next frame.
        
        Args:
            node1_id: The ID of the first node
            node2_id: The ID of the second node
            duration: Duration of this frame in seconds
            easing: Easing function to use
            
        Returns:
            Self for method chaining
        """
        # Create a copy of the current graph state
        new_graph_data = self.current_graph.copy()
        new_edges = []
        edge_found = False
        
        # Find and remove the edge
        for edge in new_graph_data["edges"]:
            src, dst, attrs = edge
            if (src == node1_id and dst == node2_id) or \
               (not new_graph_data.get("directed", False) and src == node2_id and dst == node1_id):
                edge_found = True
            else:
                new_edges.append(edge)
        
        if not edge_found:
            raise ValueError(f"Edge between {node1_id} and {node2_id} does not exist in the current frame")
        
        # Update the graph data
        new_graph_data["edges"] = new_edges
        
        # Create a new Graph object from the updated data
        new_graph = Graph.from_dict(new_graph_data)
        
        # Update current state and add frame
        self.current_graph = new_graph_data
        self.animation.add_frame(new_graph, duration, easing)
        
        return self
    
    def get_animation(self) -> Animation:
        """
        Get the created animation.
        
        Returns:
            The Animation object
        """
        return self.animation 