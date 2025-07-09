
def write_costs_to_file(costs: list[list[int]], filename: str = "costs.txt") -> None:
    """
    Writes a 2D list of costs to a file in the expected format (one row per line, values space-separated).

    :param costs: 2D list of costs.
    :type costs: list[list[int]]
    :param filename: Output filename.
    :type filename: str
    """
    with open(filename, "w") as f:
        for row in costs:
            f.write(" ".join(str(val) for val in row) + "\n")