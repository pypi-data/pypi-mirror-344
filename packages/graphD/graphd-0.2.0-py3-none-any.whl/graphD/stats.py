"""
Statistical graph visualization module for graphD library.
Provides tools for generating statistical charts without external dependencies.
"""

import math
import random
from typing import Dict, List, Tuple, Optional, Union, Any
from .renderer import Bitmap, Color, WHITE, BLACK, RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN, MAGENTA


class StatsPlotter:
    """Class for creating statistical graphs and charts."""
    
    def __init__(self, width: int = 800, height: int = 600, background: Color = WHITE, title: str = ""):
        """
        Initialize a StatsPlotter with given dimensions and background color.
        
        Args:
            width: Width of the image in pixels
            height: Height of the image in pixels
            background: Background color of the image
            title: Title of the chart
        """
        self.width = width
        self.height = height
        self.background = background
        self.title = title
        self.bitmap = None
        self._initialize_bitmap()
        
        # Chart margins
        self.margin_top = 60 if title else 40
        self.margin_bottom = 60
        self.margin_left = 80
        self.margin_right = 40
        
        # Calculated chart area
        self.chart_width = self.width - self.margin_left - self.margin_right
        self.chart_height = self.height - self.margin_top - self.margin_bottom
        
    def _initialize_bitmap(self):
        """Initialize the bitmap for drawing."""
        self.bitmap = Bitmap(self.width, self.height, self.background)
        
        # Draw title if present
        if self.title:
            self.bitmap.draw_text(self.width // 2 - len(self.title) * 3, 20, self.title, BLACK, size=2)
    
    def _draw_axes(self, x_label: str = "", y_label: str = "", 
                  x_ticks: List[str] = None, y_ticks: List[str] = None,
                  x_min: float = 0, x_max: float = 0, 
                  y_min: float = 0, y_max: float = 0):
        """
        Draw X and Y axes with optional labels and tick marks.
        
        Args:
            x_label: Label for the X axis
            y_label: Label for the Y axis
            x_ticks: List of labels for X-axis tick marks
            y_ticks: List of labels for Y-axis tick marks
            x_min, x_max: Min and max values for X-axis
            y_min, y_max: Min and max values for Y-axis
        """
        # Draw X and Y axes
        # X-axis
        self.bitmap.draw_line(
            self.margin_left, self.height - self.margin_bottom,
            self.width - self.margin_right, self.height - self.margin_bottom,
            BLACK
        )
        
        # Y-axis
        self.bitmap.draw_line(
            self.margin_left, self.height - self.margin_bottom,
            self.margin_left, self.margin_top,
            BLACK
        )
        
        # Draw X-axis label
        if x_label:
            x_pos = self.margin_left + self.chart_width // 2 - len(x_label) * 3
            y_pos = self.height - 20
            self.bitmap.draw_text(x_pos, y_pos, x_label, BLACK)
        
        # Draw Y-axis label
        if y_label:
            # Vertical text is challenging with our simple text renderer
            # Place it horizontally near the Y-axis
            x_pos = 10
            y_pos = self.margin_top + self.chart_height // 2 - len(y_label) * 3
            self.bitmap.draw_text(x_pos, y_pos, y_label, BLACK)
        
        # Draw X-axis tick marks and values
        if x_ticks:
            tick_width = self.chart_width / len(x_ticks)
            for i, label in enumerate(x_ticks):
                x_pos = self.margin_left + i * tick_width + tick_width / 2
                # Tick mark
                self.bitmap.draw_line(
                    int(x_pos), self.height - self.margin_bottom,
                    int(x_pos), self.height - self.margin_bottom + 5,
                    BLACK
                )
                # Tick label
                self.bitmap.draw_text(
                    int(x_pos - len(label) * 3), self.height - self.margin_bottom + 10,
                    label, BLACK
                )
        
        # Draw Y-axis tick marks and values
        if y_ticks:
            tick_height = self.chart_height / len(y_ticks)
            for i, label in enumerate(y_ticks):
                y_pos = self.height - self.margin_bottom - i * tick_height - tick_height / 2
                # Tick mark
                self.bitmap.draw_line(
                    self.margin_left - 5, int(y_pos),
                    self.margin_left, int(y_pos),
                    BLACK
                )
                # Tick label
                self.bitmap.draw_text(
                    self.margin_left - 10 - len(label) * 6, int(y_pos - 6),
                    label, BLACK
                )
    
    def bar_chart(self, data: Dict[str, float], x_label: str = "Category", 
                 y_label: str = "Value", color: Color = BLUE, sort: bool = False):
        """
        Create a bar chart from a dictionary of data.
        
        Args:
            data: Dictionary mapping categories to values
            x_label: Label for the X axis
            y_label: Label for the Y axis
            color: Color of the bars
            sort: Whether to sort the data by value
        """
        if not data:
            raise ValueError("No data provided for bar chart")
        
        # Sort data if requested
        if sort:
            items = sorted(data.items(), key=lambda x: x[1])
            categories = [item[0] for item in items]
            values = [item[1] for item in items]
        else:
            categories = list(data.keys())
            values = list(data.values())
        
        # Calculate Y-axis scale
        max_value = max(values)
        y_max = max_value * 1.1  # Add 10% padding
        
        # Create tick marks for Y-axis
        num_ticks = 5
        y_ticks = []
        for i in range(num_ticks + 1):
            tick_value = y_max * i / num_ticks
            y_ticks.append(f"{tick_value:.1f}")
        
        # Draw axes
        self._draw_axes(
            x_label=x_label, 
            y_label=y_label,
            x_ticks=categories,
            y_ticks=y_ticks,
            y_max=y_max
        )
        
        # Draw bars
        bar_width = self.chart_width / len(data) * 0.8
        spacing = self.chart_width / len(data) * 0.2
        
        for i, (category, value) in enumerate(zip(categories, values)):
            # Calculate bar dimensions
            bar_height = (value / y_max) * self.chart_height
            x_pos = self.margin_left + i * (bar_width + spacing) + spacing / 2
            y_pos = self.height - self.margin_bottom - bar_height
            
            # Draw the bar
            for y in range(int(y_pos), int(self.height - self.margin_bottom)):
                for x in range(int(x_pos), int(x_pos + bar_width)):
                    self.bitmap.set_pixel(x, y, color)
            
            # Draw value on top of the bar
            value_text = f"{value:.1f}"
            self.bitmap.draw_text(
                int(x_pos + bar_width / 2 - len(value_text) * 3),
                int(y_pos - 15),
                value_text, BLACK
            )
    
    def line_chart(self, data: List[Tuple[float, float]], x_label: str = "X", 
                  y_label: str = "Y", color: Color = RED, line_width: int = 2,
                  x_min: float = None, x_max: float = None,
                  y_min: float = None, y_max: float = None):
        """
        Create a line chart from a list of (x, y) points.
        
        Args:
            data: List of (x, y) data points
            x_label: Label for the X axis
            y_label: Label for the Y axis
            color: Color of the line
            line_width: Width of the line in pixels
            x_min, x_max: Optional min and max values for X-axis
            y_min, y_max: Optional min and max values for Y-axis
        """
        if not data:
            raise ValueError("No data provided for line chart")
        
        # Sort data by x-value
        data = sorted(data)
        
        # Extract x and y values
        x_values = [point[0] for point in data]
        y_values = [point[1] for point in data]
        
        # Calculate axis limits if not provided
        if x_min is None:
            x_min = min(x_values)
        if x_max is None:
            x_max = max(x_values)
            x_max += (x_max - x_min) * 0.1  # Add 10% padding
        
        if y_min is None:
            y_min = min(y_values)
            y_min = min(0, y_min)  # Start from 0 if all values are positive
        if y_max is None:
            y_max = max(y_values)
            y_max += (y_max - y_min) * 0.1  # Add 10% padding
        
        # Create tick marks for axes
        num_x_ticks = min(10, len(data))
        num_y_ticks = 5
        
        x_ticks = []
        for i in range(num_x_ticks + 1):
            tick_value = x_min + (x_max - x_min) * i / num_x_ticks
            x_ticks.append(f"{tick_value:.1f}")
        
        y_ticks = []
        for i in range(num_y_ticks + 1):
            tick_value = y_min + (y_max - y_min) * i / num_y_ticks
            y_ticks.append(f"{tick_value:.1f}")
        
        # Draw axes
        self._draw_axes(
            x_label=x_label, 
            y_label=y_label,
            x_ticks=x_ticks,
            y_ticks=y_ticks,
            x_min=x_min, x_max=x_max,
            y_min=y_min, y_max=y_max
        )
        
        # Draw the line
        prev_point = None
        for x, y in data:
            # Convert data coordinates to pixel coordinates
            pixel_x = self.margin_left + ((x - x_min) / (x_max - x_min)) * self.chart_width
            pixel_y = self.height - self.margin_bottom - ((y - y_min) / (y_max - y_min)) * self.chart_height
            
            # Draw a point
            self.bitmap.draw_circle(int(pixel_x), int(pixel_y), 3, color, fill=True)
            
            # Draw line segment to previous point
            if prev_point:
                prev_x, prev_y = prev_point
                for i in range(line_width):
                    offset = (line_width - 1) // 2 - i
                    self.bitmap.draw_line(
                        int(prev_x), int(prev_y + offset),
                        int(pixel_x), int(pixel_y + offset),
                        color
                    )
            
            prev_point = (pixel_x, pixel_y)
    
    def scatter_plot(self, data: List[Tuple[float, float]], x_label: str = "X", 
                    y_label: str = "Y", point_color: Color = BLUE, 
                    point_size: int = 4, x_min: float = None, x_max: float = None,
                    y_min: float = None, y_max: float = None):
        """
        Create a scatter plot from a list of (x, y) points.
        
        Args:
            data: List of (x, y) data points
            x_label: Label for the X axis
            y_label: Label for the Y axis
            point_color: Color of the points
            point_size: Size of each point
            x_min, x_max: Optional min and max values for X-axis
            y_min, y_max: Optional min and max values for Y-axis
        """
        if not data:
            raise ValueError("No data provided for scatter plot")
        
        # Extract x and y values
        x_values = [point[0] for point in data]
        y_values = [point[1] for point in data]
        
        # Calculate axis limits if not provided
        if x_min is None:
            x_min = min(x_values)
        if x_max is None:
            x_max = max(x_values)
            x_max += (x_max - x_min) * 0.1  # Add 10% padding
        
        if y_min is None:
            y_min = min(y_values)
        if y_max is None:
            y_max = max(y_values)
            y_max += (y_max - y_min) * 0.1  # Add 10% padding
        
        # Create tick marks for axes
        num_ticks = 5
        
        x_ticks = []
        for i in range(num_ticks + 1):
            tick_value = x_min + (x_max - x_min) * i / num_ticks
            x_ticks.append(f"{tick_value:.1f}")
        
        y_ticks = []
        for i in range(num_ticks + 1):
            tick_value = y_min + (y_max - y_min) * i / num_ticks
            y_ticks.append(f"{tick_value:.1f}")
        
        # Draw axes
        self._draw_axes(
            x_label=x_label, 
            y_label=y_label,
            x_ticks=x_ticks,
            y_ticks=y_ticks,
            x_min=x_min, x_max=x_max,
            y_min=y_min, y_max=y_max
        )
        
        # Draw points
        for x, y in data:
            # Convert data coordinates to pixel coordinates
            pixel_x = self.margin_left + ((x - x_min) / (x_max - x_min)) * self.chart_width
            pixel_y = self.height - self.margin_bottom - ((y - y_min) / (y_max - y_min)) * self.chart_height
            
            # Draw a point
            self.bitmap.draw_circle(int(pixel_x), int(pixel_y), point_size, point_color, fill=True)
    
    def histogram(self, data: List[float], bins: int = 10, x_label: str = "Value", 
                 y_label: str = "Frequency", color: Color = GREEN,
                 x_min: float = None, x_max: float = None):
        """
        Create a histogram from a list of values.
        
        Args:
            data: List of numeric values
            bins: Number of bins to divide the data into
            x_label: Label for the X axis
            y_label: Label for the Y axis
            color: Color of the bars
            x_min, x_max: Optional min and max values for X-axis
        """
        if not data:
            raise ValueError("No data provided for histogram")
        
        # Calculate min and max values if not provided
        if x_min is None:
            x_min = min(data)
        if x_max is None:
            x_max = max(data)
            x_max += (x_max - x_min) * 0.05  # Add 5% padding
        
        # Create bins
        bin_width = (x_max - x_min) / bins
        bin_counts = [0] * bins
        
        # Count values in each bin
        for value in data:
            if x_min <= value < x_max:
                bin_index = min(bins - 1, int((value - x_min) / bin_width))
                bin_counts[bin_index] += 1
        
        # Calculate max frequency for Y-axis scale
        max_count = max(bin_counts) if bin_counts else 0
        y_max = max_count * 1.1  # Add 10% padding
        
        # Create tick marks for axes
        x_ticks = []
        for i in range(bins + 1):
            tick_value = x_min + bin_width * i
            x_ticks.append(f"{tick_value:.1f}")
        
        num_y_ticks = 5
        y_ticks = []
        for i in range(num_y_ticks + 1):
            tick_value = y_max * i / num_y_ticks
            y_ticks.append(f"{int(tick_value)}")
        
        # Draw axes
        self._draw_axes(
            x_label=x_label, 
            y_label=y_label,
            x_ticks=x_ticks[::max(1, bins // 5)],  # Show subset of x ticks to avoid crowding
            y_ticks=y_ticks,
            x_min=x_min, x_max=x_max,
            y_max=y_max
        )
        
        # Draw bars
        bar_width = self.chart_width / bins
        
        for i, count in enumerate(bin_counts):
            # Calculate bar dimensions
            bar_height = (count / y_max) * self.chart_height if y_max > 0 else 0
            x_pos = self.margin_left + i * bar_width
            y_pos = self.height - self.margin_bottom - bar_height
            
            # Draw the bar
            for y in range(int(y_pos), int(self.height - self.margin_bottom)):
                for x in range(int(x_pos), int(x_pos + bar_width)):
                    self.bitmap.set_pixel(x, y, color)
            
            # Draw count on top of the bar if there's enough space
            if count > 0 and bar_height > 15:
                count_text = str(count)
                self.bitmap.draw_text(
                    int(x_pos + bar_width / 2 - len(count_text) * 3),
                    int(y_pos - 10),
                    count_text, BLACK
                )
    
    def pie_chart(self, data: Dict[str, float], colors: List[Color] = None):
        """
        Create a pie chart from a dictionary of data.
        
        Args:
            data: Dictionary mapping categories to values
            colors: List of colors for each slice (will cycle if fewer colors than categories)
        """
        if not data:
            raise ValueError("No data provided for pie chart")
        
        # Use default colors if none provided
        if colors is None:
            colors = [RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, CYAN, MAGENTA]
        
        # Calculate total for percentages
        total = sum(data.values())
        if total <= 0:
            raise ValueError("Total of values must be positive")
        
        # Calculate center and radius
        center_x = self.width // 2
        center_y = (self.height - self.margin_top) // 2 + self.margin_top
        radius = min(self.chart_width, self.chart_height) // 2 - 20
        
        # Draw pie chart
        start_angle = 0
        color_index = 0
        
        for category, value in data.items():
            # Skip zero or negative values
            if value <= 0:
                continue
                
            # Calculate slice angles
            slice_angle = 2 * math.pi * value / total
            end_angle = start_angle + slice_angle
            
            # Draw slice
            color = colors[color_index % len(colors)]
            color_index += 1
            
            # Fill the slice
            for r in range(radius):
                for angle in [a/100 for a in range(int(start_angle*100), int(end_angle*100))]:
                    x = int(center_x + r * math.cos(angle))
                    y = int(center_y + r * math.sin(angle))
                    self.bitmap.set_pixel(x, y, color)
            
            # Draw slice border
            for angle in [a/100 for a in range(int(start_angle*100), int(end_angle*100))]:
                x = int(center_x + radius * math.cos(angle))
                y = int(center_y + radius * math.sin(angle))
                self.bitmap.set_pixel(x, y, BLACK)
            
            # Draw radius lines
            self.bitmap.draw_line(center_x, center_y, 
                                 int(center_x + radius * math.cos(start_angle)), 
                                 int(center_y + radius * math.sin(start_angle)), 
                                 BLACK)
            self.bitmap.draw_line(center_x, center_y, 
                                 int(center_x + radius * math.cos(end_angle)), 
                                 int(center_y + radius * math.sin(end_angle)), 
                                 BLACK)
            
            # Calculate position for label
            mid_angle = start_angle + slice_angle / 2
            label_radius = radius * 0.7
            label_x = int(center_x + label_radius * math.cos(mid_angle))
            label_y = int(center_y + label_radius * math.sin(mid_angle))
            
            # Draw percentage
            percentage = f"{value/total*100:.1f}%"
            self.bitmap.draw_text(
                label_x - len(percentage) * 3,
                label_y,
                percentage, BLACK
            )
            
            # Move to next slice
            start_angle = end_angle
        
        # Draw legend
        legend_x = self.width - self.margin_right + 10
        legend_y = self.margin_top
        legend_square_size = 10
        legend_spacing = 25
        
        color_index = 0
        for category, value in data.items():
            if value <= 0:
                continue
                
            # Draw color square
            color = colors[color_index % len(colors)]
            color_index += 1
            
            for y in range(legend_y, legend_y + legend_square_size):
                for x in range(legend_x, legend_x + legend_square_size):
                    self.bitmap.set_pixel(x, y, color)
            
            # Draw category name
            label = f"{category} ({value/total*100:.1f}%)"
            self.bitmap.draw_text(
                legend_x + legend_square_size + 5,
                legend_y + 2,
                label, BLACK
            )
            
            # Move to next legend item
            legend_y += legend_spacing
    
    def save(self, filename: str):
        """Save the chart to a file."""
        self.bitmap.save_as(filename)
        return filename


# Helper functions to create different types of charts
def create_bar_chart(data: Dict[str, float], filename: str, width: int = 800, height: int = 600,
                    title: str = "", x_label: str = "Category", y_label: str = "Value",
                    color: Color = BLUE, sort: bool = False, background: Color = WHITE):
    """
    Create a bar chart and save it to a file.
    
    Args:
        data: Dictionary mapping categories to values
        filename: Output file path
        width, height: Dimensions of the image
        title: Chart title
        x_label, y_label: Axis labels
        color: Bar color
        sort: Whether to sort the data by value
        background: Background color
    
    Returns:
        Path to the saved image file
    """
    plotter = StatsPlotter(width, height, background, title)
    plotter.bar_chart(data, x_label, y_label, color, sort)
    return plotter.save(filename)


def create_line_chart(data: List[Tuple[float, float]], filename: str, width: int = 800, height: int = 600,
                     title: str = "", x_label: str = "X", y_label: str = "Y",
                     color: Color = RED, line_width: int = 2, background: Color = WHITE,
                     x_min: float = None, x_max: float = None,
                     y_min: float = None, y_max: float = None):
    """
    Create a line chart and save it to a file.
    
    Args:
        data: List of (x, y) data points
        filename: Output file path
        width, height: Dimensions of the image
        title: Chart title
        x_label, y_label: Axis labels
        color: Line color
        line_width: Width of the line in pixels
        background: Background color
        x_min, x_max: Optional min and max values for X-axis
        y_min, y_max: Optional min and max values for Y-axis
    
    Returns:
        Path to the saved image file
    """
    plotter = StatsPlotter(width, height, background, title)
    plotter.line_chart(data, x_label, y_label, color, line_width, x_min, x_max, y_min, y_max)
    return plotter.save(filename)


def create_scatter_plot(data: List[Tuple[float, float]], filename: str, width: int = 800, height: int = 600,
                       title: str = "", x_label: str = "X", y_label: str = "Y",
                       point_color: Color = BLUE, point_size: int = 4, background: Color = WHITE,
                       x_min: float = None, x_max: float = None,
                       y_min: float = None, y_max: float = None):
    """
    Create a scatter plot and save it to a file.
    
    Args:
        data: List of (x, y) data points
        filename: Output file path
        width, height: Dimensions of the image
        title: Chart title
        x_label, y_label: Axis labels
        point_color: Color of the points
        point_size: Size of each point
        background: Background color
        x_min, x_max: Optional min and max values for X-axis
        y_min, y_max: Optional min and max values for Y-axis
    
    Returns:
        Path to the saved image file
    """
    plotter = StatsPlotter(width, height, background, title)
    plotter.scatter_plot(data, x_label, y_label, point_color, point_size, x_min, x_max, y_min, y_max)
    return plotter.save(filename)


def create_histogram(data: List[float], filename: str, width: int = 800, height: int = 600,
                    title: str = "", x_label: str = "Value", y_label: str = "Frequency",
                    bins: int = 10, color: Color = GREEN, background: Color = WHITE,
                    x_min: float = None, x_max: float = None):
    """
    Create a histogram and save it to a file.
    
    Args:
        data: List of numeric values
        filename: Output file path
        width, height: Dimensions of the image
        title: Chart title
        x_label, y_label: Axis labels
        bins: Number of bins to divide the data into
        color: Bar color
        background: Background color
        x_min, x_max: Optional min and max values for X-axis
    
    Returns:
        Path to the saved image file
    """
    plotter = StatsPlotter(width, height, background, title)
    plotter.histogram(data, bins, x_label, y_label, color, x_min, x_max)
    return plotter.save(filename)


def create_pie_chart(data: Dict[str, float], filename: str, width: int = 800, height: int = 600,
                    title: str = "", colors: List[Color] = None, background: Color = WHITE):
    """
    Create a pie chart and save it to a file.
    
    Args:
        data: Dictionary mapping categories to values
        filename: Output file path
        width, height: Dimensions of the image
        title: Chart title
        colors: List of colors for each slice
        background: Background color
    
    Returns:
        Path to the saved image file
    """
    plotter = StatsPlotter(width, height, background, title)
    plotter.pie_chart(data, colors)
    return plotter.save(filename) 