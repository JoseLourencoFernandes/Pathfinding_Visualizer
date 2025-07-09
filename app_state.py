from definitions.global_constants import Screen

class GlobalAppState:
    """
    Class to manage the global state of the application.
    This class keeps track of the currently active screen and the state of the grid applications.
    It contains instances of Grid2DAppState and Grid2DWeightedAppState to manage their respective states.
    
    :param currently_screen: The currently active screen in the application.
    :type currently_screen: Screen
    :param grid2d_app_state: The state of the 2D grid application.
    :type grid2d_app_state: Grid2DAppState
    :param grid2d_weighted_app_state: The state of the weighted 2D grid application.
    :type grid2d_weighted_app_state: Grid2DAppState
    :param graph_app_state: The state of the graph application.
    :type graph_app_state: GraphAppState
    """
    current_screen: Screen
    grid2d_app_state: 'Grid2DAppState'
    grid2d_weighted_app_state: 'Grid2DAppState'
    graph_app_state: 'GraphAppState'
    
    def __init__(self):
        self.current_screen = Screen.MAIN_MENU
        self.grid2d_app_state = Grid2DAppState()
        self.grid2d_weighted_app_state = Grid2DAppState()
        self.graph_app_state = GraphAppState()

class Grid2DAppState:
    """
    Class to manage the state of the application.
    This class keeps track of various flags and variables that control the behavior of the application.
    
    :param set_start_mode: Indicates if the user is in start mode.
    :type set_start_mode: bool
    :param set_goal_mode: Indicates if the user is in goal mode.
    :type set_goal_mode: bool
    :param ignore_drag: Flag to ignore mouse drag events.
    :type ignore_drag: bool
    :param running_algorithm: Indicates if an algorithm is currently running.
    :type running_algorithm: bool
    :param grid_full_reset: Indicates if the grid has to be fully reseted.
    :type grid_full_reset: bool
    :param start_time: Holds the start time of the algorithm execution.
    :type start_time: float
    :param execution_time: Holds the execution time of the algorithm.
    :type execution_time: float
    :param runned_algorithm: Indicates if an algorithm has been runned.
    :type runned_algorithm: bool
    """
    set_start_mode: bool
    set_goal_mode: bool
    ignore_drag: bool
    running_algorithm: bool
    grid_full_reset: bool
    start_time: float
    execution_time: float
    runned_algorithm: bool
    
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
    """
    Class to manage the state of the graph application.
    This class keeps track of various flags and variables that control the behavior of the graph application.
    
    :param set_start_mode: Indicates if the user is in start mode.
    :type set_start_mode: bool
    :param set_goal_mode: Indicates if the user is in goal mode.
    :type set_goal_mode: bool
    :param ignore_drag: Flag to ignore mouse drag events.
    :type ignore_drag: bool
    :param running_algorithm: Indicates if an algorithm is currently running.
    :type running_algorithm: bool
    :param grid_full_reset: Indicates if the grid has to be fully reseted.
    :type grid_full_reset: bool
    :param start_time: Holds the start time of the algorithm execution.
    :type start_time: float
    :param execution_time: Holds the execution time of the algorithm.
    :type execution_time: float
    :param runned_algorithm: Indicates if an algorithm has been runned.
    :type runned_algorithm: bool  
    """
    set_start_mode: bool
    set_goal_mode: bool
    ignore_drag: bool
    running_algorithm: bool
    grid_full_reset: bool
    start_time: float
    execution_time: float
    runned_algorithm: bool

    def __init__(self):
        self.set_start_mode = False
        self.set_goal_mode = False
        self.ignore_drag = False
        self.running_algorithm = False
        self.grid_full_reset = True
        self.start_time = None
        self.execution_time = 0.0
        self.runned_algorithm = False