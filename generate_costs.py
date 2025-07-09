import argparse
import sys
from utils.writers import write_costs_to_file
from utils.generator import generate_grid_costs

def main(size: int = 19, min_cost: int = 1, max_cost: int = 9) -> None:
    """
    Main function to generate a grid of costs and write it to a file.
    
    :param size: The size of the grid (size x size).
    :type size: int
    :param min_cost: The minimum cost value.
    :type min_cost: int
    :param max_cost: The maximum cost value.
    :type max_cost: int
    """
    costs = generate_grid_costs(size, min_cost, max_cost)
    write_costs_to_file(costs, "costs.txt")
    print(f"Costs generated and written to 'costs.txt' with size {size}x{size} and costs between {min_cost} and {max_cost}.")

if __name__ == "__main__":
    # Argument parser for command line arguments
    parser = argparse.ArgumentParser(description="Generate a grid of random costs and write to costs.txt")
    parser.add_argument("size", type=int, nargs="?", default=19, help="Grid size (default: 19)")
    parser.add_argument("min_cost", type=int, nargs="?", default=1, help="Minimum cost value (default: 1)")
    parser.add_argument("max_cost", type=int, nargs="?", default=9, help="Maximum cost value (default: 9)")
    args = parser.parse_args()
    
    # Validate arguments
    if not (0 < args.min_cost < 100):
        print("Error: min_cost must be > 0 and < 100.")
        sys.exit(1)
    if not (0 < args.max_cost < 100):
        print("Error: max_cost must be > 0 and < 100.")
        sys.exit(1)
    if args.min_cost >=  args.max_cost:
        print("Error: min_cost must be less than max_cost.")
        sys.exit(1)
    
    main(size=args.size, min_cost=args.min_cost, max_cost=args.max_cost)    
