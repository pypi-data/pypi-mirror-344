"""
Custom pixel-based rendering system for graphD library.
Implements rendering from scratch without external dependencies.
"""

import math
import os
from typing import Tuple, List, Dict, Any, Optional


class Color:
    """Simple color class with RGBA components."""
    
    def __init__(self, r: int, g: int, b: int, a: int = 255):
        """Initialize color with RGBA values (0-255)."""
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))
        self.a = max(0, min(255, a))
    
    @classmethod
    def from_hex(cls, hex_color: str):
        """Create color from hex string (#RRGGBB or #RRGGBBAA)."""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return cls(r, g, b)
        elif len(hex_color) == 8:
            r, g, b, a = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6))
            return cls(r, g, b, a)
        else:
            raise ValueError(f"Invalid hex color: {hex_color}")
    
    def __str__(self):
        return f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})"


# Predefined colors
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
GRAY = Color(128, 128, 128)


class Bitmap:
    """A simple bitmap image class."""
    
    def __init__(self, width: int, height: int, background: Color = WHITE):
        """Initialize a bitmap with given dimensions and background color."""
        self.width = width
        self.height = height
        # Create a 2D array of pixels, each pixel is a Color object
        self.pixels = [[background for _ in range(width)] for _ in range(height)]
    
    def set_pixel(self, x: int, y: int, color: Color):
        """Set the color of a pixel at (x, y) coordinates."""
        if 0 <= x < self.width and 0 <= y < self.height:
            # Basic alpha blending
            if color.a == 255:
                self.pixels[y][x] = color
            elif color.a > 0:
                bg = self.pixels[y][x]
                alpha = color.a / 255.0
                r = int(color.r * alpha + bg.r * (1 - alpha))
                g = int(color.g * alpha + bg.g * (1 - alpha))
                b = int(color.b * alpha + bg.b * (1 - alpha))
                self.pixels[y][x] = Color(r, g, b)
    
    def draw_line(self, x0: int, y0: int, x1: int, y1: int, color: Color):
        """Draw a line between (x0, y0) and (x1, y1) using Bresenham's algorithm."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        
        while True:
            self.set_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                if x0 == x1:
                    break
                err += dy
                x0 += sx
            if e2 <= dx:
                if y0 == y1:
                    break
                err += dx
                y0 += sy
    
    def draw_circle(self, x_center: int, y_center: int, radius: int, color: Color, fill: bool = False):
        """Draw a circle centered at (x_center, y_center) with given radius."""
        if fill:
            # Fill the circle
            for y in range(y_center - radius, y_center + radius + 1):
                for x in range(x_center - radius, x_center + radius + 1):
                    # Check if point is inside circle
                    if (x - x_center) ** 2 + (y - y_center) ** 2 <= radius ** 2:
                        self.set_pixel(x, y, color)
        else:
            # Draw circle outline (Bresenham's circle algorithm)
            x = radius
            y = 0
            err = 0
            
            while x >= y:
                self.set_pixel(x_center + x, y_center + y, color)
                self.set_pixel(x_center + y, y_center + x, color)
                self.set_pixel(x_center - y, y_center + x, color)
                self.set_pixel(x_center - x, y_center + y, color)
                self.set_pixel(x_center - x, y_center - y, color)
                self.set_pixel(x_center - y, y_center - x, color)
                self.set_pixel(x_center + y, y_center - x, color)
                self.set_pixel(x_center + x, y_center - y, color)
                
                y += 1
                if err <= 0:
                    err += 2 * y + 1
                if err > 0:
                    x -= 1
                    err -= 2 * x + 1

    def draw_text(self, x: int, y: int, text: str, color: Color, size: int = 1):
        """
        Draw text at position (x, y).
        This is a very simple implementation using basic pixel art for characters.
        For a real application, you'd want to use proper font rendering.
        """
        # Simple pixel font for basic characters (limited character set)
        # Each character is defined by a list of (x, y) coordinates to draw
        # relative to the top-left corner of the character
        pixel_font = {
            'A': [(0, 2), (0, 3), (0, 4), (1, 1), (2, 1), (1, 3), (2, 3), (3, 2), (3, 3), (3, 4)],
            'B': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (2, 0), (1, 2), (2, 2), (1, 4), (2, 4), (3, 1), (3, 3)],
            'C': [(1, 0), (2, 0), (3, 0), (0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)],
            # Add more characters as needed
            ' ': []
        }
        
        char_width = 4 * size
        x_pos = x
        
        for char in text:
            char_upper = char.upper()
            if char_upper in pixel_font:
                for px, py in pixel_font[char_upper]:
                    for i in range(size):
                        for j in range(size):
                            self.set_pixel(x_pos + px * size + i, y + py * size + j, color)
            x_pos += char_width
    
    def save_ppm(self, filename: str):
        """Save the bitmap as a PPM file (a simple image format)."""
        with open(filename, 'w') as f:
            # PPM header: P3 means colors in ASCII
            f.write(f"P3\n{self.width} {self.height}\n255\n")
            # Write pixel data
            for row in self.pixels:
                for color in row:
                    f.write(f"{color.r} {color.g} {color.b} ")
                f.write("\n")
        
        print(f"Image saved to {filename}")


class GraphRenderer:
    """Class for rendering a Graph object to a bitmap image."""
    
    def __init__(self, width: int = 800, height: int = 600, background: Color = WHITE):
        """Initialize a renderer with given dimensions."""
        self.width = width
        self.height = height
        self.background = background
        self.node_radius = 15
        self.node_color = BLUE
        self.edge_color = BLACK
        self.label_color = BLACK
    
    def _calculate_positions(self, graph):
        """
        Calculate node positions using a simple force-directed layout algorithm.
        """
        from .core import Graph
        
        if not isinstance(graph, Graph):
            raise TypeError("Expected a Graph object")
        
        # Initialize random positions
        positions = {}
        nodes = graph.get_nodes()
        
        # Start with nodes in a circle
        node_count = len(nodes)
        if node_count == 0:
            return positions
        
        # Circle layout for initial positions
        radius = min(self.width, self.height) * 0.4
        center_x = self.width // 2
        center_y = self.height // 2
        
        i = 0
        for node_id in nodes:
            angle = 2 * math.pi * i / node_count
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            positions[node_id] = (int(x), int(y))
            i += 1
        
        # Simple force-directed algorithm
        # For a more complex graph, you'd want a better layout algorithm
        if node_count > 1:
            iterations = 50
            k = math.sqrt(self.width * self.height / node_count)  # Optimal distance
            
            for _ in range(iterations):
                # Calculate repulsive forces between all nodes
                forces = {node_id: [0, 0] for node_id in nodes}
                
                # Repulsive forces (nodes repel each other)
                for i, node1_id in enumerate(nodes):
                    x1, y1 = positions[node1_id]
                    for j, node2_id in enumerate(nodes):
                        if i == j:
                            continue
                        
                        x2, y2 = positions[node2_id]
                        dx = x1 - x2
                        dy = y1 - y2
                        distance = max(0.1, math.sqrt(dx*dx + dy*dy))
                        
                        if distance < 1:
                            distance = 1
                        
                        # Repulsive force is proportional to 1/distance
                        force = k*k / distance
                        forces[node1_id][0] += dx / distance * force
                        forces[node1_id][1] += dy / distance * force
                
                # Attractive forces (connected nodes attract)
                for edge in graph.get_edges():
                    node1_id, node2_id, _ = edge
                    x1, y1 = positions[node1_id]
                    x2, y2 = positions[node2_id]
                    dx = x2 - x1
                    dy = y2 - y1
                    distance = max(0.1, math.sqrt(dx*dx + dy*dy))
                    
                    # Attractive force is proportional to distance
                    force = distance * distance / k
                    
                    # Apply force to both nodes
                    forces[node1_id][0] += dx / distance * force
                    forces[node1_id][1] += dy / distance * force
                    forces[node2_id][0] -= dx / distance * force
                    forces[node2_id][1] -= dy / distance * force
                
                # Apply forces to update positions
                for node_id in nodes:
                    fx, fy = forces[node_id]
                    x, y = positions[node_id]
                    
                    # Limit maximum movement
                    max_force = 10
                    fx = max(-max_force, min(max_force, fx))
                    fy = max(-max_force, min(max_force, fy))
                    
                    # Update position
                    new_x = int(x + fx)
                    new_y = int(y + fy)
                    
                    # Keep nodes within the image
                    padding = self.node_radius + 10
                    new_x = max(padding, min(self.width - padding, new_x))
                    new_y = max(padding, min(self.height - padding, new_y))
                    
                    positions[node_id] = (new_x, new_y)
        
        return positions
    
    def render(self, graph, filename: str):
        """Render the graph to a bitmap image and save it to a file."""
        from .core import Graph
        
        if not isinstance(graph, Graph):
            raise TypeError("Expected a Graph object")
        
        # Create bitmap
        bitmap = Bitmap(self.width, self.height, self.background)
        
        # Calculate node positions
        positions = self._calculate_positions(graph)
        
        # Draw edges
        for edge in graph.get_edges():
            node1_id, node2_id, attrs = edge
            if node1_id in positions and node2_id in positions:
                x1, y1 = positions[node1_id]
                x2, y2 = positions[node2_id]
                
                # Get edge color and other attributes
                edge_color = self.edge_color
                if 'color' in attrs:
                    try:
                        edge_color = Color.from_hex(attrs['color'])
                    except ValueError:
                        pass
                
                # Draw edge
                bitmap.draw_line(x1, y1, x2, y2, edge_color)
        
        # Draw nodes
        nodes = graph.get_nodes()
        for node_id, attrs in nodes.items():
            if node_id in positions:
                x, y = positions[node_id]
                
                # Get node color and other attributes
                node_color = self.node_color
                if 'color' in attrs:
                    try:
                        node_color = Color.from_hex(attrs['color'])
                    except ValueError:
                        pass
                
                # Get node radius
                radius = self.node_radius
                if 'size' in attrs:
                    try:
                        radius = int(attrs['size'])
                    except (ValueError, TypeError):
                        pass
                
                # Draw node
                bitmap.draw_circle(x, y, radius, node_color, fill=True)
                bitmap.draw_circle(x, y, radius, BLACK, fill=False)  # Border
                
                # Draw node label
                label = str(node_id)
                if 'label' in attrs:
                    label = str(attrs['label'])
                
                # Simple centering based on label length
                text_offset_x = len(label) * 2
                bitmap.draw_text(x - text_offset_x, y - 2, label, self.label_color)
        
        # Save to file
        bitmap.save_ppm(filename)
        return filename 