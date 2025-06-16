from definitions.global_constants import Screen

class GlobalAppState:
    """
    Class to manage the global state of the application.
    This class keeps track of the currently active screen and the state of the grid applications.
    It contains instances of Grid2DAppState and Grid2DWeightedAppState to manage their respective states.
    
    Attributes:
        currently_screen (Screen): The currently active screen in the application.
        grid2d_app_state (Grid2DAppState): The state of the 2D grid application.
        grid2d_weighted_app_state (Grid2DAppState): The state of the weighted 2D grid application.
        graph_app_state (GraphAppState): The state of the graph application.
    """
    def __init__(self):
        self.current_screen = Screen.MAIN_MENU
        self.grid2d_app_state = Grid2DAppState()
        self.grid2d_weighted_app_state = Grid2DAppState()
        self.graph_app_state = GraphAppState()

class Grid2DAppState:
    """
    Class to manage the state of the application.
    This class keeps track of various flags and variables that control the behavior of the application.
    
    Attributes:
        set_start_mode (bool): Indicates if the user is in start mode.
        set_goal_mode (bool): Indicates if the user is in goal mode.
        ignore_drag (bool): Flag to ignore mouse drag events.
        running_algorithm (bool): Indicates if an algorithm is currently running.
        grid_full_reset (bool): Indicates if the grid has to be fully reseted.
        start_time (float): Holds the start time of the algorithm execution.
        execution_time (float): Holds the execution time of the algorithm.
        runned_algorithm (bool): Indicates if an algorithm has been runned.
    """
    def __init__(self):
        self.set_start_mode = False 
        self.set_goal_mode = False
        self.ignore_drag = False
        self.running_algorithm = False
        self.grid_full_reset = True
        self.start_time = None
        self.execution_time = 0.0
        self.runned_algorithm = False

class GraphAppState:

    def __init__(self):
        self.set_start_mode = False
        self.set_goal_mode = False
        self.ignore_drag = False
        self.running_algorithm = False
        self.grid_full_reset = True
        self.start_time = None
        self.execution_time = 0.0
        self.runned_algorithm = False