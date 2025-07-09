"""
This module defines constants related to the graphical representation of the grid.
It includes constants for the graph area size, node radius, and safe area margins.
"""

from definitions.global_constants import SCREEN_WIDTH, SCREEN_HEIGHT

GRAPH_AREA_MARGIN = 5   # Horizontal margin from the window edge

GRAPH_AREA_SIZE = SCREEN_HEIGHT - 2 * GRAPH_AREA_MARGIN

NODE_RADIUS = 15

SAFE_MIN_AREA = GRAPH_AREA_MARGIN + NODE_RADIUS
SAFE_MAX_AREA = GRAPH_AREA_MARGIN + GRAPH_AREA_SIZE - NODE_RADIUS