from .core import Graph
from typing import Dict, List, Tuple, Optional, Any, Callable

class InteractiveElement:
    """Base class for interactive elements."""
    
    def __init__(self, target_id: str, event_type: str = "hover"):
        """
        Initialize an interactive element.
        
        Args:
            target_id: ID of the target node or edge
            event_type: Type of event that triggers the interaction ("hover", "click")
        """
        self.target_id = target_id
        self.event_type = event_type
    
    def apply_to_graph(self, graph: Graph) -> None:
        """Apply the interactive element to a graph."""
        # To be implemented by subclasses
        pass


class Tooltip(InteractiveElement):
    """Class for adding tooltips to graph elements."""
    
    def __init__(self, target_id: str, text: str, 
                 event_type: str = "hover", 
                 position: str = "auto",
                 style: Dict[str, Any] = None):
        """
        Initialize a tooltip.
        
        Args:
            target_id: ID of the target node or edge to attach tooltip to
            text: Text to display in the tooltip
            event_type: Type of event that triggers the tooltip ("hover", "click")
            position: Position of the tooltip relative to target ("auto", "top", "right", "bottom", "left")
            style: Custom styling for the tooltip (e.g., {"background": "black", "color": "white"})
        """
        super().__init__(target_id, event_type)
        self.text = text
        self.position = position
        self.style = style or {}
    
    def apply_to_graph(self, graph: Graph) -> None:
        """Apply the tooltip to the graph."""
        # Check if target exists
        if self.target_id not in graph.get_nodes():
            # Check if it's an edge
            found = False
            for src, dst, _ in graph.get_edges():
                if src == self.target_id or dst == self.target_id:
                    found = True
                    break
            
            if not found:
                raise ValueError(f"Target element {self.target_id} not found in graph")
        
        # Create a tooltip node
        tooltip_id = f"tooltip_{self.target_id}"
        
        # Add tooltip node with all the data
        graph.add_node(tooltip_id, 
                      type="tooltip",
                      target_id=self.target_id,
                      text=self.text,
                      event_type=self.event_type,
                      position=self.position,
                      style=self.style)
        
        # Link tooltip to target (for easy querying)
        if self.target_id in graph.get_nodes():
            graph.add_edge(self.target_id, tooltip_id, type="tooltip_link", visible=False)


class Highlight(InteractiveElement):
    """Class for highlighting elements on interaction."""
    
    def __init__(self, target_id: str, 
                 color: str = "red", 
                 thickness: int = 2,
                 glow: bool = False,
                 event_type: str = "hover",
                 highlight_connected: bool = False):
        """
        Initialize a highlight effect.
        
        Args:
            target_id: ID of the target node or edge
            color: Color to use for highlighting
            thickness: Thickness of the highlight border/line
            glow: Whether to add a glow effect
            event_type: Type of event that triggers the highlight ("hover", "click")
            highlight_connected: Whether to also highlight nodes/edges connected to the target
        """
        super().__init__(target_id, event_type)
        self.color = color
        self.thickness = thickness
        self.glow = glow
        self.highlight_connected = highlight_connected
    
    def apply_to_graph(self, graph: Graph) -> None:
        """Apply the highlight to the graph."""
        # Check if target exists
        if self.target_id not in graph.get_nodes():
            # Check if it's an edge
            found = False
            for src, dst, _ in graph.get_edges():
                if src == self.target_id or dst == self.target_id:
                    found = True
                    break
            
            if not found:
                raise ValueError(f"Target element {self.target_id} not found in graph")
        
        # Create a highlight node
        highlight_id = f"highlight_{self.target_id}"
        
        # Add highlight node with all the data
        graph.add_node(highlight_id, 
                      type="highlight",
                      target_id=self.target_id,
                      color=self.color,
                      thickness=self.thickness,
                      glow=self.glow,
                      event_type=self.event_type,
                      highlight_connected=self.highlight_connected)
        
        # Link highlight to target (for easy querying)
        if self.target_id in graph.get_nodes():
            graph.add_edge(self.target_id, highlight_id, type="highlight_link", visible=False)


class PointLabel(InteractiveElement):
    """Class for adding data point labels to graph elements."""
    
    def __init__(self, target_id: str, 
                 text: str,
                 position: str = "top",
                 offset_x: int = 0,
                 offset_y: int = -10,
                 font_size: int = 10,
                 always_visible: bool = True,
                 event_type: str = "hover"):
        """
        Initialize a point label.
        
        Args:
            target_id: ID of the target node
            text: Text to display in the label
            position: Position of the label relative to target ("top", "right", "bottom", "left", "center")
            offset_x: Additional x offset in pixels
            offset_y: Additional y offset in pixels
            font_size: Font size of the label text
            always_visible: Whether the label is always visible or only on interaction
            event_type: Type of event that shows the label if not always visible ("hover", "click")
        """
        super().__init__(target_id, event_type)
        self.text = text
        self.position = position
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.font_size = font_size
        self.always_visible = always_visible
    
    def apply_to_graph(self, graph: Graph) -> None:
        """Apply the point label to the graph."""
        # Check if target exists
        if self.target_id not in graph.get_nodes():
            raise ValueError(f"Target node {self.target_id} not found in graph")
        
        # Create a label node
        label_id = f"label_{self.target_id}"
        
        # Add label node with all the data
        graph.add_node(label_id, 
                      type="point_label",
                      target_id=self.target_id,
                      text=self.text,
                      position=self.position,
                      offset_x=self.offset_x,
                      offset_y=self.offset_y,
                      font_size=self.font_size,
                      always_visible=self.always_visible,
                      event_type=self.event_type)
        
        # Link label to target
        graph.add_edge(self.target_id, label_id, type="label_link", visible=False)


class InteractiveGraph:
    """Wrapper class to add interactive features to a graph."""
    
    def __init__(self, graph: Graph):
        """
        Initialize with a base graph.
        
        Args:
            graph: The base Graph object to add interactivity to
        """
        self.graph = graph
        self.interactive_elements: List[InteractiveElement] = []
    
    def add_tooltip(self, target_id: str, text: str, 
                   event_type: str = "hover", 
                   position: str = "auto",
                   style: Dict[str, Any] = None) -> 'InteractiveGraph':
        """
        Add a tooltip to a graph element.
        
        Args:
            target_id: ID of the target node or edge
            text: Text to display in the tooltip
            event_type: Type of event that triggers the tooltip
            position: Position of the tooltip relative to target
            style: Custom styling for the tooltip
            
        Returns:
            Self for method chaining
        """
        tooltip = Tooltip(target_id, text, event_type, position, style)
        self.interactive_elements.append(tooltip)
        return self
    
    def add_highlight(self, target_id: str, 
                     color: str = "red", 
                     thickness: int = 2,
                     glow: bool = False,
                     event_type: str = "hover",
                     highlight_connected: bool = False) -> 'InteractiveGraph':
        """
        Add a highlight effect to a graph element.
        
        Args:
            target_id: ID of the target node or edge
            color: Color to use for highlighting
            thickness: Thickness of the highlight border/line
            glow: Whether to add a glow effect
            event_type: Type of event that triggers the highlight
            highlight_connected: Whether to also highlight connected elements
            
        Returns:
            Self for method chaining
        """
        highlight = Highlight(target_id, color, thickness, glow, event_type, highlight_connected)
        self.interactive_elements.append(highlight)
        return self
    
    def add_point_label(self, target_id: str, 
                       text: str,
                       position: str = "top",
                       offset_x: int = 0,
                       offset_y: int = -10,
                       font_size: int = 10,
                       always_visible: bool = True,
                       event_type: str = "hover") -> 'InteractiveGraph':
        """
        Add a point label to a graph node.
        
        Args:
            target_id: ID of the target node
            text: Text to display in the label
            position: Position of the label relative to target
            offset_x: Additional x offset in pixels
            offset_y: Additional y offset in pixels
            font_size: Font size of the label text
            always_visible: Whether the label is always visible
            event_type: Type of event that shows the label if not always visible
            
        Returns:
            Self for method chaining
        """
        label = PointLabel(target_id, text, position, offset_x, offset_y, 
                          font_size, always_visible, event_type)
        self.interactive_elements.append(label)
        return self
    
    def get_graph(self) -> Graph:
        """
        Get the graph with all interactive elements applied.
        
        Returns:
            The modified Graph object
        """
        # Apply all interactive elements to the graph
        for element in self.interactive_elements:
            element.apply_to_graph(self.graph)
        
        # Mark this graph as interactive
        if "__meta__" not in self.graph.get_nodes():
            self.graph.add_node("__meta__", type="metadata", interactive=True)
        else:
            # Update existing metadata
            self.graph.get_nodes()["__meta__"]["interactive"] = True
        
        return self.graph 