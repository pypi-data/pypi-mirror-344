"""
PixelD: Custom pixel-based rendering system for graphD library.
Implements rendering from scratch without external dependencies.
"""

import math
import os
from typing import Tuple, List, Dict, Any, Optional
import base64


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
    
    def blend(self, other: 'Color', factor: float) -> 'Color':
        """Linear interpolation between two colors with given factor (0-1)."""
        factor = max(0, min(1, factor))
        r = int(self.r * (1 - factor) + other.r * factor)
        g = int(self.g * (1 - factor) + other.g * factor)
        b = int(self.b * (1 - factor) + other.b * factor)
        a = int(self.a * (1 - factor) + other.a * factor)
        return Color(r, g, b, a)
    
    def __str__(self):
        return f"Color(r={self.r}, g={self.g}, b={self.b}, a={self.a})"


# Predefined colors
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
GRAY = Color(128, 128, 128)
YELLOW = Color(255, 255, 0)
CYAN = Color(0, 255, 255)
MAGENTA = Color(255, 0, 255)
ORANGE = Color(255, 165, 0)
PURPLE = Color(128, 0, 128)
BROWN = Color(165, 42, 42)
LIGHT_GRAY = Color(211, 211, 211)
DARK_GRAY = Color(64, 64, 64)
PINK = Color(255, 192, 203)
NAVY = Color(0, 0, 128)
TEAL = Color(0, 128, 128)


class Bitmap:
    """A simple bitmap image class with basic anti-aliasing support."""
    
    def __init__(self, width: int, height: int, background: Color = WHITE):
        """Initialize a bitmap with given dimensions and background color."""
        self.width = width
        self.height = height
        # Create a 2D array of pixels, each pixel is a Color object
        self.pixels = [[background for _ in range(width)] for _ in range(height)]
        self.use_antialiasing = True  # Can be toggled on/off
    
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
    
    def set_pixel_aa(self, x: float, y: float, color: Color):
        """Set a pixel with anti-aliasing using bilinear interpolation for fractional coordinates."""
        if not self.use_antialiasing:
            self.set_pixel(int(x), int(y), color)
            return
            
        # Get integer and fractional parts
        x_int, x_frac = int(x), x - int(x)
        y_int, y_frac = int(y), y - int(y)
        
        # Calculate pixel weights for the four surrounding pixels
        weight_tl = (1 - x_frac) * (1 - y_frac)
        weight_tr = x_frac * (1 - y_frac)
        weight_bl = (1 - x_frac) * y_frac
        weight_br = x_frac * y_frac
        
        # Set pixels with appropriate alpha
        if 0 <= x_int < self.width and 0 <= y_int < self.height:
            c = Color(color.r, color.g, color.b, int(color.a * weight_tl))
            self.set_pixel(x_int, y_int, c)
            
        if 0 <= x_int + 1 < self.width and 0 <= y_int < self.height:
            c = Color(color.r, color.g, color.b, int(color.a * weight_tr))
            self.set_pixel(x_int + 1, y_int, c)
            
        if 0 <= x_int < self.width and 0 <= y_int + 1 < self.height:
            c = Color(color.r, color.g, color.b, int(color.a * weight_bl))
            self.set_pixel(x_int, y_int + 1, c)
            
        if 0 <= x_int + 1 < self.width and 0 <= y_int + 1 < self.height:
            c = Color(color.r, color.g, color.b, int(color.a * weight_br))
            self.set_pixel(x_int + 1, y_int + 1, c)
    
    def draw_line(self, x0: int, y0: int, x1: int, y1: int, color: Color, line_style: str = "solid", thickness: int = 1):
        """
        Draw a line between (x0, y0) and (x1, y1) using Bresenham's algorithm.
        
        Args:
            x0, y0: Starting point coordinates
            x1, y1: Ending point coordinates
            color: Line color
            line_style: "solid", "dashed", or "dotted"
            thickness: Line thickness in pixels
        """
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        
        # Pattern for different line styles
        if line_style == "solid":
            pattern = [1]  # Always draw
        elif line_style == "dashed":
            pattern = [1, 1, 1, 1, 0, 0, 0, 0]  # Draw 4 pixels, skip 4 pixels
        elif line_style == "dotted":
            pattern = [1, 0]  # Draw 1 pixel, skip 1 pixel
        else:
            pattern = [1]  # Default to solid line
        
        pattern_index = 0
        pattern_length = len(pattern)
        
        # For thicker lines
        if thickness > 1 and self.use_antialiasing:
            # For anti-aliased thick lines, use a different approach
            length = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            if length < 0.0001:
                return  # Avoid division by zero
                
            # Unit vector perpendicular to the line
            nx = -(y1 - y0) / length
            ny = (x1 - x0) / length
            
            half_thickness = thickness / 2
            
            while True:
                if pattern[pattern_index % pattern_length]:
                    # Draw multiple pixels perpendicular to the line direction for thickness
                    for offset in range(-(thickness//2), thickness//2 + 1):
                        px = x0 + offset * nx
                        py = y0 + offset * ny
                        # Use anti-aliased pixel setting
                        self.set_pixel_aa(px, py, color)
                
                pattern_index += 1
                
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
        else:
            # Standard algorithm for single-pixel or non-anti-aliased lines
            while True:
                if pattern[pattern_index % pattern_length]:
                    if thickness == 1:
                        self.set_pixel(x0, y0, color)
                    else:
                        # Simple thick line by drawing multiple pixels
                        for i in range(thickness):
                            for j in range(thickness):
                                self.set_pixel(x0 + i - thickness//2, y0 + j - thickness//2, color)
                
                pattern_index += 1
                
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
    
    def draw_arrow(self, x0: int, y0: int, x1: int, y1: int, color: Color, size: int = 10, line_style: str = "solid", thickness: int = 1):
        """Draw an arrow from (x0, y0) to (x1, y1)."""
        # Draw the main line
        self.draw_line(x0, y0, x1, y1, color, line_style, thickness)
        
        # Calculate the arrowhead
        angle = math.atan2(y1 - y0, x1 - x0)
        # Points for the arrowhead
        arrow_angle1 = angle + math.pi * 3/4  # 135 degrees from the line
        arrow_angle2 = angle - math.pi * 3/4  # -135 degrees from the line
        
        # Calculate arrowhead points
        ax1 = int(x1 + size * math.cos(arrow_angle1))
        ay1 = int(y1 + size * math.sin(arrow_angle1))
        ax2 = int(x1 + size * math.cos(arrow_angle2))
        ay2 = int(y1 + size * math.sin(arrow_angle2))
        
        # Draw arrowhead lines
        self.draw_line(x1, y1, ax1, ay1, color, "solid", thickness)
        self.draw_line(x1, y1, ax2, ay2, color, "solid", thickness)
    
    def draw_circle(self, x_center: int, y_center: int, radius: int, color: Color, fill: bool = False, antialiased: bool = True):
        """Draw a circle centered at (x_center, y_center) with given radius."""
        if fill:
            # Fill the circle
            for y in range(y_center - radius, y_center + radius + 1):
                for x in range(x_center - radius, x_center + radius + 1):
                    # Check if point is inside circle
                    dist_squared = (x - x_center) ** 2 + (y - y_center) ** 2
                    if dist_squared <= radius ** 2:
                        self.set_pixel(x, y, color)
                    elif antialiased and self.use_antialiasing and dist_squared <= (radius+1) ** 2:
                        # Anti-aliasing: Smooth the edge with alpha
                        dist = math.sqrt(dist_squared)
                        if radius < dist <= radius + 1:
                            alpha_factor = 1 - (dist - radius)
                            aa_color = Color(color.r, color.g, color.b, int(color.a * alpha_factor))
                            self.set_pixel(x, y, aa_color)
        else:
            # Draw circle outline (Bresenham's circle algorithm)
            if antialiased and self.use_antialiasing:
                # Anti-aliased circle drawing
                num_segments = max(50, int(radius * 2))  # More segments for larger circles
                for i in range(num_segments):
                    angle = 2 * math.pi * i / num_segments
                    x = x_center + radius * math.cos(angle)
                    y = y_center + radius * math.sin(angle)
                    self.set_pixel_aa(x, y, color)
            else:
                # Standard circle algorithm
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

    def draw_text(self, x: int, y: int, text: str, color: Color, size: int = 1, font_style: str = "normal"):
        """
        Draw text at position (x, y) with enhanced styling options.
        
        Args:
            x, y: Top-left corner position
            text: The text to draw
            color: Text color
            size: Font size multiplier
            font_style: "normal", "bold", or "italic"
        """
        # Simple pixel font for basic characters
        # Each character is defined by a list of (x, y) coordinates to draw
        # relative to the top-left corner of the character
        pixel_font = {
            'A': [(0, 2), (0, 3), (0, 4), (1, 1), (2, 1), (1, 3), (2, 3), (3, 2), (3, 3), (3, 4)],
            'B': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (2, 0), (1, 2), (2, 2), (1, 4), (2, 4), (3, 1), (3, 3)],
            'C': [(1, 0), (2, 0), (3, 0), (0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)],
            'D': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (2, 0), (3, 1), (3, 2), (3, 3), (1, 4), (2, 4)],
            'E': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (2, 0), (3, 0), (1, 2), (2, 2), (1, 4), (2, 4), (3, 4)],
            'F': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (2, 0), (3, 0), (1, 2), (2, 2)],
            'G': [(1, 0), (2, 0), (3, 0), (0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4), (3, 2), (3, 3), (2, 2)],
            'H': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (1, 2), (2, 2)],
            'I': [(1, 0), (2, 0), (3, 0), (2, 1), (2, 2), (2, 3), (1, 4), (2, 4), (3, 4)],
            'J': [(3, 0), (3, 1), (3, 2), (3, 3), (0, 3), (1, 4), (2, 4)],
            'K': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (3, 0), (2, 1), (1, 2), (2, 3), (3, 4)],
            'L': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4)],
            'M': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (1, 1), (3, 1), (2, 2)],
            'N': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 1), (2, 2), (3, 3), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)],
            'O': [(1, 0), (2, 0), (0, 1), (0, 2), (0, 3), (3, 1), (3, 2), (3, 3), (1, 4), (2, 4)],
            'P': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (2, 0), (3, 1), (1, 2), (2, 2)],
            'Q': [(1, 0), (2, 0), (0, 1), (0, 2), (3, 1), (3, 2), (1, 3), (2, 3), (3, 4)],
            'R': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (2, 0), (3, 1), (1, 2), (2, 2), (3, 3), (3, 4)],
            'S': [(1, 0), (2, 0), (3, 0), (0, 1), (1, 2), (2, 2), (3, 3), (0, 4), (1, 4), (2, 4)],
            'T': [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
            'U': [(0, 0), (0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 3), (3, 2), (3, 1), (3, 0)],
            'V': [(0, 0), (0, 1), (0, 2), (1, 3), (2, 4), (3, 3), (4, 2), (4, 1), (4, 0)],
            'W': [(0, 0), (0, 1), (0, 2), (0, 3), (1, 4), (2, 3), (3, 4), (4, 3), (4, 2), (4, 1), (4, 0)],
            'X': [(0, 0), (0, 4), (1, 1), (1, 3), (2, 2), (3, 1), (3, 3), (4, 0), (4, 4)],
            'Y': [(0, 0), (0, 1), (1, 2), (2, 3), (2, 4), (3, 2), (4, 1), (4, 0)],
            'Z': [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (2, 2), (1, 3), (0, 4), (1, 4), (2, 4), (3, 4)],
            '0': [(1, 0), (2, 0), (0, 1), (0, 2), (0, 3), (3, 1), (3, 2), (3, 3), (1, 4), (2, 4), (1, 3), (2, 1)],
            '1': [(1, 0), (0, 1), (1, 1), (1, 2), (1, 3), (1, 4), (0, 4), (2, 4)],
            '2': [(0, 0), (1, 0), (2, 0), (3, 1), (2, 2), (1, 3), (0, 4), (1, 4), (2, 4), (3, 4)],
            '3': [(0, 0), (1, 0), (2, 0), (3, 1), (2, 2), (1, 2), (3, 3), (0, 4), (1, 4), (2, 4)],
            '4': [(2, 0), (1, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3), (2, 1), (2, 2), (2, 4)],
            '5': [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 3), (0, 4), (1, 4), (2, 4)],
            '6': [(1, 0), (2, 0), (0, 1), (0, 2), (0, 3), (1, 2), (2, 2), (3, 3), (1, 4), (2, 4)],
            '7': [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (2, 2), (1, 3), (1, 4)],
            '8': [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2), (0, 3), (3, 3), (1, 4), (2, 4)],
            '9': [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2), (3, 2), (3, 3), (1, 4), (2, 4)],
            ' ': [],
            '.': [(1, 4)],
            ',': [(1, 4), (0, 5)],
            ':': [(1, 1), (1, 3)],
            ';': [(1, 1), (1, 3), (0, 4)],
            '!': [(1, 0), (1, 1), (1, 2), (1, 4)],
            '?': [(1, 0), (2, 0), (3, 1), (2, 2), (1, 2), (1, 4)],
            '(': [(2, 0), (1, 1), (1, 2), (1, 3), (2, 4)],
            ')': [(1, 0), (2, 1), (2, 2), (2, 3), (1, 4)],
            '[': [(1, 0), (2, 0), (1, 1), (1, 2), (1, 3), (1, 4), (2, 4)],
            ']': [(1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (1, 4), (2, 4)],
            '+': [(1, 1), (0, 2), (1, 2), (2, 2), (1, 3)],
            '-': [(0, 2), (1, 2), (2, 2)],
            '*': [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)],
            '/': [(2, 0), (2, 1), (1, 2), (0, 3), (0, 4)],
            '\\': [(0, 0), (0, 1), (1, 2), (2, 3), (2, 4)],
            '=': [(0, 1), (1, 1), (2, 1), (0, 3), (1, 3), (2, 3)],
            '_': [(0, 4), (1, 4), (2, 4), (3, 4)],
            '&': [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (0, 3), (3, 3), (1, 4), (2, 4), (3, 5)],
            '@': [(1, 0), (2, 0), (0, 1), (3, 1), (1, 2), (2, 2), (3, 2), (3, 3), (2, 3), (1, 4), (2, 4)],
            '#': [(1, 0), (3, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (1, 2), (3, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (1, 4), (3, 4)],
            '%': [(0, 0), (1, 0), (4, 0), (0, 1), (1, 1), (3, 1), (2, 2), (1, 3), (4, 3), (4, 4), (0, 4), (3, 4)],
            '^': [(1, 0), (3, 0), (0, 1), (4, 1)],
            '<': [(3, 0), (2, 1), (1, 2), (2, 3), (3, 4)],
            '>': [(1, 0), (2, 1), (3, 2), (2, 3), (1, 4)],
            '|': [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4)],
            '~': [(0, 2), (1, 1), (2, 1), (3, 2), (4, 1)]
        }
        
        # Add additional pixels for bold style
        bold_extra = {
            'A': [(0, 1), (1, 0), (2, 0), (4, 2), (4, 3), (4, 4)],
            'B': [(3, 0), (3, 2), (3, 4)],
            # Add extra pixels for other characters as needed
        }
        
        # Add slant for italic style
        italic_offset = lambda y: 1 if y < 2 else 0
        
        char_width = 5 * size  # Increased for 'M', 'W', etc.
        x_pos = x
        
        for char in text:
            char_upper = char.upper()
            if char_upper in pixel_font:
                pixels = list(pixel_font[char_upper])
                
                # Add bold pixels if needed
                if font_style == "bold" and char_upper in bold_extra:
                    pixels.extend(bold_extra[char_upper])
                
                for px, py in pixels:
                    # Apply italic offset if needed
                    if font_style == "italic":
                        px += italic_offset(py)
                        
                    # Draw the pixel with the specified size
                    for i in range(size):
                        for j in range(size):
                            self.set_pixel(x_pos + px * size + i, y + py * size + j, color)
            
            # Adjust spacing between characters
            spacing = 6 if font_style == "bold" else 5
            x_pos += spacing * size
    
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
    
    def _write_bmp_file(self, filename: str):
        """Save the bitmap as a BMP file."""
        # BMP file header (14 bytes)
        file_header = bytearray([
            0x42, 0x4D,             # 'BM' signature
            0, 0, 0, 0,             # Size of the BMP file (filled later)
            0, 0,                   # Reserved
            0, 0,                   # Reserved
            54, 0, 0, 0             # Offset to the pixel array
        ])
        
        # DIB header (40 bytes)
        dib_header = bytearray([
            40, 0, 0, 0,            # Size of the DIB header
            0, 0, 0, 0,             # Width of the bitmap (filled later)
            0, 0, 0, 0,             # Height of the bitmap (filled later)
            1, 0,                   # Number of color planes (must be 1)
            24, 0,                  # Number of bits per pixel (24 for RGB)
            0, 0, 0, 0,             # Compression method (0 for none)
            0, 0, 0, 0,             # Size of the raw bitmap data (filled later)
            0x13, 0x0B, 0, 0,       # Horizontal resolution (2835 pixels/meter)
            0x13, 0x0B, 0, 0,       # Vertical resolution (2835 pixels/meter)
            0, 0, 0, 0,             # Number of colors in the palette (0 for 2^24)
            0, 0, 0, 0              # Number of important colors (0 for all)
        ])
        
        # Fill in the width and height fields in the DIB header
        width_bytes = self.width.to_bytes(4, byteorder='little')
        height_bytes = self.height.to_bytes(4, byteorder='little')
        
        for i in range(4):
            dib_header[4 + i] = width_bytes[i]
            dib_header[8 + i] = height_bytes[i]
        
        # Calculate row padding
        row_size = self.width * 3
        padding_size = (4 - (row_size % 4)) % 4
        padded_row_size = row_size + padding_size
        
        # Calculate the size of the raw bitmap data
        raw_data_size = padded_row_size * self.height
        raw_data_size_bytes = raw_data_size.to_bytes(4, byteorder='little')
        
        for i in range(4):
            dib_header[20 + i] = raw_data_size_bytes[i]
        
        # Calculate the total file size
        file_size = 14 + 40 + raw_data_size
        file_size_bytes = file_size.to_bytes(4, byteorder='little')
        
        for i in range(4):
            file_header[2 + i] = file_size_bytes[i]
        
        # Write the file
        with open(filename, 'wb') as f:
            # Write the file header
            f.write(file_header)
            # Write the DIB header
            f.write(dib_header)
            
            # Write the pixel data (starting from the bottom row)
            padding = bytes([0] * padding_size)
            
            for y in range(self.height - 1, -1, -1):
                for x in range(self.width):
                    color = self.pixels[y][x]
                    # BMP stores pixels in BGR order
                    f.write(bytes([color.b, color.g, color.r]))
                
                # Add padding to ensure each row is a multiple of 4 bytes
                if padding_size > 0:
                    f.write(padding)
        
        return file_size
    
    def to_base64_string(self, format: str = "bmp") -> str:
        """
        Convert the bitmap to a base64-encoded string.
        
        Args:
            format: The format to use ("bmp", "ppm")
        
        Returns:
            A base64-encoded string representation of the image
        """
        import io
        import base64
        
        # Create a memory file-like object
        buffer = io.BytesIO()
        
        if format.lower() == "bmp":
            # Write BMP to memory buffer
            # BMP file header (14 bytes)
            file_header = bytearray([
                0x42, 0x4D,             # 'BM' signature
                0, 0, 0, 0,             # Size of the BMP file (filled later)
                0, 0,                   # Reserved
                0, 0,                   # Reserved
                54, 0, 0, 0             # Offset to the pixel array
            ])
            
            # DIB header (40 bytes)
            dib_header = bytearray([
                40, 0, 0, 0,            # Size of the DIB header
                0, 0, 0, 0,             # Width of the bitmap (filled later)
                0, 0, 0, 0,             # Height of the bitmap (filled later)
                1, 0,                   # Number of color planes (must be 1)
                24, 0,                  # Number of bits per pixel (24 for RGB)
                0, 0, 0, 0,             # Compression method (0 for none)
                0, 0, 0, 0,             # Size of the raw bitmap data (filled later)
                0x13, 0x0B, 0, 0,       # Horizontal resolution (2835 pixels/meter)
                0x13, 0x0B, 0, 0,       # Vertical resolution (2835 pixels/meter)
                0, 0, 0, 0,             # Number of colors in the palette (0 for 2^24)
                0, 0, 0, 0              # Number of important colors (0 for all)
            ])
            
            # Fill in the width and height fields in the DIB header
            width_bytes = self.width.to_bytes(4, byteorder='little')
            height_bytes = self.height.to_bytes(4, byteorder='little')
            
            for i in range(4):
                dib_header[4 + i] = width_bytes[i]
                dib_header[8 + i] = height_bytes[i]
            
            # Calculate row padding
            row_size = self.width * 3
            padding_size = (4 - (row_size % 4)) % 4
            padded_row_size = row_size + padding_size
            
            # Calculate the size of the raw bitmap data
            raw_data_size = padded_row_size * self.height
            raw_data_size_bytes = raw_data_size.to_bytes(4, byteorder='little')
            
            for i in range(4):
                dib_header[20 + i] = raw_data_size_bytes[i]
            
            # Calculate the total file size
            file_size = 14 + 40 + raw_data_size
            file_size_bytes = file_size.to_bytes(4, byteorder='little')
            
            for i in range(4):
                file_header[2 + i] = file_size_bytes[i]
            
            # Write to memory buffer
            buffer.write(file_header)
            buffer.write(dib_header)
            
            # Write the pixel data (starting from the bottom row)
            padding = bytes([0] * padding_size)
            
            for y in range(self.height - 1, -1, -1):
                for x in range(self.width):
                    color = self.pixels[y][x]
                    # BMP stores pixels in BGR order
                    buffer.write(bytes([color.b, color.g, color.r]))
                
                # Add padding to ensure each row is a multiple of 4 bytes
                if padding_size > 0:
                    buffer.write(padding)
                    
            # Get mime type for data URL
            mime_type = "image/bmp"
            
        elif format.lower() == "ppm":
            # Write PPM to memory buffer
            buffer = io.StringIO()
            # PPM header: P3 means colors in ASCII
            buffer.write(f"P3\n{self.width} {self.height}\n255\n")
            # Write pixel data
            for row in self.pixels:
                for color in row:
                    buffer.write(f"{color.r} {color.g} {color.b} ")
                buffer.write("\n")
                
            # Convert string buffer to bytes
            buffer = io.BytesIO(buffer.getvalue().encode('utf-8'))
            # Get mime type for data URL
            mime_type = "image/x-portable-pixmap"
            
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        # Get the bytes from the buffer
        buffer.seek(0)
        img_bytes = buffer.getvalue()
        
        # Encode as base64
        encoded = base64.b64encode(img_bytes).decode('ascii')
        
        # Return as a data URL
        return f"data:{mime_type};base64,{encoded}"
    
    def save_as(self, filename: str):
        """Save the bitmap in a format determined by the file extension."""
        extension = os.path.splitext(filename)[1].lower()
        
        if extension == '.ppm':
            self.save_ppm(filename)
        elif extension == '.bmp':
            self._write_bmp_file(filename)
        elif extension in ['.png', '.jpg', '.jpeg']:
            # For PNG/JPEG formats, first save as BMP and then convert
            # This is a placeholder for a true PNG/JPEG encoder
            # In a real implementation, you would want to use a library or write a more sophisticated encoder
            temp_bmp = os.path.splitext(filename)[0] + '.bmp'
            self._write_bmp_file(temp_bmp)
            print(f"Image saved as BMP: {temp_bmp}")
            print(f"Note: To save as {extension}, you would need to install the Pillow library and use:")
            print(f"    from PIL import Image")
            print(f"    img = Image.open('{temp_bmp}')")
            print(f"    img.save('{filename}')")
        else:
            self.save_ppm(filename)  # Default to PPM
            print(f"Unknown extension '{extension}', saved as PPM instead")


class GraphRenderer:
    """PixelD Graph Renderer - Renders a Graph object to a bitmap image using PixelD engine."""
    
    def __init__(self, width: int = 800, height: int = 600, background: Color = WHITE, theme: str = "default"):
        """
        Initialize a renderer with given dimensions and theme.
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
            background: Background color
            theme: Visual theme ("default", "dark", "neon", "pastel", "monochrome")
        """
        self.width = width
        self.height = height
        self.background = background
        self.node_radius = 15
        self.node_color = BLUE
        self.edge_color = BLACK
        self.label_color = BLACK
        self.arrow_size = 10  # Size of arrowheads for directed edges
        self.title = None
        self.title_color = BLACK
        self.edge_thickness = 1
        self.antialiasing = True
        self.grid_visible = False
        self.grid_color = LIGHT_GRAY
        
        # Apply theme
        self.set_theme(theme)
    
    def set_theme(self, theme: str):
        """
        Apply a predefined visual theme to the renderer.
        
        Args:
            theme: The theme name ("default", "dark", "neon", "pastel", "monochrome")
        """
        if theme == "default":
            self.background = WHITE
            self.node_color = BLUE
            self.edge_color = BLACK
            self.label_color = BLACK
            self.title_color = BLACK
            self.grid_color = LIGHT_GRAY
        elif theme == "dark":
            self.background = DARK_GRAY
            self.node_color = CYAN
            self.edge_color = LIGHT_GRAY
            self.label_color = WHITE
            self.title_color = WHITE
            self.grid_color = Color(80, 80, 80)
        elif theme == "neon":
            self.background = BLACK
            self.node_color = Color(0, 255, 128)  # Neon green
            self.edge_color = Color(255, 0, 255)  # Neon pink
            self.label_color = Color(0, 255, 255) # Neon cyan
            self.title_color = Color(255, 255, 0) # Neon yellow
            self.grid_color = Color(64, 0, 64)
        elif theme == "pastel":
            self.background = Color(245, 245, 245)
            self.node_color = Color(173, 216, 230)  # Light blue
            self.edge_color = Color(188, 143, 143)  # Rosy brown
            self.label_color = Color(105, 105, 105)  # Dim gray
            self.title_color = Color(95, 158, 160)  # Cadet blue
            self.grid_color = Color(220, 220, 220)
        elif theme == "monochrome":
            self.background = WHITE
            self.node_color = Color(100, 100, 100)
            self.edge_color = Color(50, 50, 50)
            self.label_color = BLACK
            self.title_color = BLACK
            self.grid_color = Color(200, 200, 200)
        else:
            # Unknown theme, use default
            print(f"Unknown theme '{theme}', using 'default' instead")
            self.set_theme("default")
    
    def set_title(self, title: str):
        """Set the title of the graph visualization."""
        self.title = title
    
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
    
    def _draw_grid(self, bitmap: Bitmap):
        """Draw a grid on the bitmap for better visual orientation."""
        if not self.grid_visible:
            return
            
        # Draw horizontal lines
        grid_spacing = 50
        for y in range(0, self.height, grid_spacing):
            bitmap.draw_line(0, y, self.width, y, self.grid_color, "dashed")
            
        # Draw vertical lines
        for x in range(0, self.width, grid_spacing):
            bitmap.draw_line(x, 0, x, self.height, self.grid_color, "dashed")
    
    def render(self, graph, filename: str = None):
        """
        Render the graph to a bitmap image.
        
        Args:
            graph: The Graph object to render
            filename: Output file path (if None, returns the bitmap without saving)
            
        Returns:
            If filename is provided, returns the filename.
            If filename is None, returns the Bitmap object.
        """
        from .core import Graph
        
        if not isinstance(graph, Graph):
            raise TypeError("Expected a Graph object")
        
        # Create bitmap
        bitmap = Bitmap(self.width, self.height, self.background)
        bitmap.use_antialiasing = self.antialiasing
        
        # Draw grid if enabled
        self._draw_grid(bitmap)
        
        # Calculate node positions
        positions = self._calculate_positions(graph)
        
        # Draw edges
        for edge in graph.get_edges():
            node1_id, node2_id, attrs = edge
            if node1_id in positions and node2_id in positions:
                x1, y1 = positions[node1_id]
                x2, y2 = positions[node2_id]
                
                # Get edge attributes
                edge_color = self.edge_color
                if 'color' in attrs:
                    try:
                        edge_color = Color.from_hex(attrs['color'])
                    except ValueError:
                        pass
                
                # Get line style
                line_style = "solid"
                if 'style' in attrs:
                    if attrs['style'] in ["solid", "dashed", "dotted"]:
                        line_style = attrs['style']
                
                # Get edge thickness
                thickness = self.edge_thickness
                if 'thickness' in attrs:
                    try:
                        thickness = int(attrs['thickness'])
                    except (ValueError, TypeError):
                        pass
                
                # Check if the edge is directed
                directed = False
                if 'directed' in attrs:
                    directed = bool(attrs['directed'])
                
                # Draw edge (either as arrow or line)
                if directed:
                    bitmap.draw_arrow(x1, y1, x2, y2, edge_color, self.arrow_size, line_style, thickness)
                else:
                    bitmap.draw_line(x1, y1, x2, y2, edge_color, line_style, thickness)
                
                # Draw edge weight/label if provided
                if 'weight' in attrs or 'label' in attrs:
                    label = str(attrs.get('label', attrs.get('weight', '')))
                    # Position the label at the midpoint of the edge
                    mid_x = (x1 + x2) // 2
                    mid_y = (y1 + y2) // 2
                    bitmap.draw_text(mid_x, mid_y, label, self.label_color)
        
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
                
                # Get node border color
                border_color = BLACK
                if 'border_color' in attrs:
                    try:
                        border_color = Color.from_hex(attrs['border_color'])
                    except ValueError:
                        pass
                
                # Draw node
                bitmap.draw_circle(x, y, radius, node_color, fill=True, antialiased=self.antialiasing)
                bitmap.draw_circle(x, y, radius, border_color, fill=False, antialiased=self.antialiasing)
                
                # Draw node label
                label = str(node_id)
                if 'label' in attrs:
                    label = str(attrs['label'])
                
                # Simple centering based on label length
                text_offset_x = len(label) * 2
                bitmap.draw_text(x - text_offset_x, y - 2, label, self.label_color)
        
        # Draw title if set
        if self.title:
            title_y = 20
            title_x = self.width // 2 - len(self.title) * 5  # Simple centering
            bitmap.draw_text(title_x, title_y, self.title.upper(), self.title_color, size=2)
        
        # Save to file if filename provided
        if filename:
            bitmap.save_as(filename)
            return filename
        
        # Otherwise return the bitmap
        return bitmap
    
    def render_to_base64(self, graph, format: str = "bmp") -> str:
        """
        Render the graph and return a base64-encoded string.
        
        Args:
            graph: The Graph object to render
            format: Output format ("bmp" or "ppm")
            
        Returns:
            A base64-encoded data URL string
        """
        bitmap = self.render(graph)
        return bitmap.to_base64_string(format) 