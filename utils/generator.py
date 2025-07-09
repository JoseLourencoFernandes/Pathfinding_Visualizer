
import random

def generate_grid_costs(size: int, min_cost: int, max_cost:int) -> list[list[int]]:
    """
    Generates a random grid of costs with specified size and cost range.
    
    :param size: The size of the grid (size x size).
    :type size: int
    :param min_cost: The minimum cost value.
    :type min_cost: int
    :param max_cost: The maximum cost value.
    :type max_cost: int
    
    :return: A 2D list representing the grid of costs.
    :rtype: list[list[int]]
    """
    return [[random.randint(min_cost, max_cost) for _ in range(size)] for _ in range(size)]