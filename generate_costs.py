import argparse
import sys
from utils.writers import write_costs_to_file
from utils.generator import generate_grid_costs

def main(size = 19, min_cost = 1, max_cost = 9):
    """
    Main function to generate a grid of costs and write it to a file.
    
    Arguments:
        size (int): The size of the grid (size x size).
        min_cost (int): The minimum cost value.
        max_cost (int): The maximum cost value.
    """
    # Generate the grid costs
    costs = generate_grid_costs(size, min_cost, max_cost)

    # Write the costs to a file
    write_costs_to_file(costs, "costs.txt")
    
    # Print confirmation message
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
    
    # Call the main function with parsed arguments
    main(size=args.size, min_cost=args.min_cost, max_cost=args.max_cost)    
