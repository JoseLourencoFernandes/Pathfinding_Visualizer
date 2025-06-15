
import random

def generate_grid_costs(size, min_cost, max_cost):
    """
    Generates a random grid of costs with specified size and cost range.
    
    Arguments:
        size (int): The size of the grid (size x size).
        min_cost (int): The minimum cost value.
        max_cost (int): The maximum cost value.
        
    Returns:
        list: A 2D list representing the grid of costs.
    """
    return [[random.randint(min_cost, max_cost) for _ in range(size)] for _ in range(size)]