def load_grid_costs(filename: str) -> list[list[int]]:
    """
    Loads costs from a file where each line represents a row of costs.
    Each line is a string of digits, where each digit represents the cost of a square.
    The costs are stored in a 2D list.
    
    :param filename: The name of the file containing the costs.
    :type filename: str
    
    :return: A 2D list of costs, where each inner list represents a row of costs.
    :rtype: list[list[int]]
    """
    costs = []
    with open(filename, 'r') as f:
        for line in f:
            # Each line is a string of digits, convert each to int
            costs.append([int(char) for char in line.strip().split()])
    return costs