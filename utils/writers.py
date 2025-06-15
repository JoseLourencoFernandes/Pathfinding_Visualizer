
def write_costs_to_file(costs, filename="costs.txt"):
    """
    Writes a 2D list of costs to a file in the expected format (one row per line, values space-separated).

    Arguments:
        costs (list): 2D list of costs.
        filename (str): Output filename.
    """
    with open(filename, "w") as f:
        for row in costs:
            f.write(" ".join(str(val) for val in row) + "\n")