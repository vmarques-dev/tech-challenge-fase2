# -*- coding: utf-8 -*-
"""
Created on Fri Dec 22 16:03:11 2023

@author: SérgioPolimante
"""
import pylab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib
import pygame
from typing import List, Tuple
from models import Delivery

matplotlib.use("Agg")


def draw_plot(screen: pygame.Surface, x: list, y: list, x_label: str = 'Generation', y_label: str = 'Fitness') -> None:
    """
    Draw a plot on a Pygame screen using Matplotlib.

    Parameters:
    - screen (pygame.Surface): The Pygame surface to draw the plot on.
    - x (list): The x-axis values.
    - y (list): The y-axis values.
    - x_label (str): Label for the x-axis (default is 'Generation').
    - y_label (str): Label for the y-axis (default is 'Fitness').
    """
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    ax.plot(x, y)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    plt.tight_layout()

    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (0, 0))

    plt.close(fig)

def get_coordinates(location):
    if isinstance(location, Delivery):
        return int(location.x), int(location.y)

    return location
    
def draw_cities(screen: pygame.Surface, cities_locations, rgb_color: Tuple[int, int, int], node_radius: int) -> None:
    """
    Draws circles representing cities or hospital deliveries
    on the given Pygame screen.
    """
    for city_location in cities_locations:
        coordinates = get_coordinates(city_location)
        pygame.draw.circle(screen, rgb_color, coordinates, node_radius)



def draw_paths(screen: pygame.Surface, path, rgb_color: Tuple[int, int, int], width: int = 1):
    """
    Draw a route containing coordinate tuples or Delivery objects.
    """
    coordinates = [get_coordinates(location) for location in path]

    pygame.draw.lines(
        screen,
        rgb_color,
        True,
        coordinates,
        width=width
    )

def draw_text(screen: pygame.Surface, text: str, color: pygame.Color) -> None:
    """
    Draw text on a Pygame screen.

    Parameters:
    - screen (pygame.Surface): The Pygame surface to draw the text on.
    - text (str): The text to be displayed.
    - color (pygame.Color): The color of the text.
    """
    pygame.font.init()  # You have to call this at the start

    font_size = 15
    my_font = pygame.font.SysFont('Arial', font_size)
    text_surface = my_font.render(text, False, color)
    
    cities_locations = []  # Assuming you have this list defined somewhere
    text_position = (np.average(np.array(cities_locations)[:, 0]), HEIGHT - 1.5 * font_size)
    
    screen.blit(text_surface, text_position)

