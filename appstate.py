# AppState class to manage the state of the application
class AppState:
    def __init__(self):
        self.set_start_mode = False # Variable to check if the user is in start mode
        self.set_goal_mode = False # Variable to check if the user is in goal mode
        self.ignore_drag = False # Variable to ignore mouse drag events
        self.running_algorithm = False # Variable to check if an algorithm is currently running
        self.grid_state = 0 # Variable to track the state of the grid (0: initial, 1: algorithm runned)
        self.start_time = None # Variable to hold the start time of the algorithm execution
        self.execution_time = 0.0 # Variable to hold the execution time of the algorithm
        self.runned_algorithm = False # Variable to check if an algorithm has been runned
