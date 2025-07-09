import sys
import os
import pygame
import math
import copy
import time
from definitions.global_constants import Screen, SCREEN_WIDTH, SCREEN_HEIGHT
from definitions.grid_constants import SQUARE_SIZE, SPACING, GRID_BUTTON_X, GRID_BUTTON_Y, GRID_BUTTON_WIDTH, GRID_BUTTON_HEIGHT, GRID_BUTTON_SPACING, TIME_TEXT_X, TIME_TEXT_Y
from definitions.colors import Color
from definitions.states import State
from algorithms import BFSAlgorithm, DFSAlgorithm, DijkstraAlgorithm, AStarAlgorithm, GreedyBestFirstAlgorithm, generate_maze_prim
from classes.grid import Grid
from classes.button import Button
from screens.screen_interface import ScreenInterface
from classes.graph import Graph, GraphNode
from definitions.graph_constants import  GRAPH_AREA_MARGIN, GRAPH_AREA_SIZE, SAFE_MIN_AREA, SAFE_MAX_AREA
from screens.button_panel_mixin import ButtonPanelMixin
from classes.graph import euclidean_graph_heuristic

class GraphScreen(ScreenInterface, ButtonPanelMixin):
    

    def __init__(self, screen, app_state):
        super().__init__(screen, app_state)
        
        self.local_app_state = app_state.graph_app_state
        
        self.graph = Graph()
        
        
        #TEST GRAPH
        self.graph = Graph()
        # Create nodes
        node1 = self.graph.add_node(150, 200)
        node2 = self.graph.add_node(300, 150)
        node3 = self.graph.add_node(450, 200)
        node4 = self.graph.add_node(600, 150)
        node5 = self.graph.add_node(500, 600)
        node6 = self.graph.add_node(600, 300)
        node7 = self.graph.add_node(450, 350)
        node8 = self.graph.add_node(300, 300)
        # Set states
        node1.change_state(State.START)
        node5.change_state(State.GOAL)
        # Connect nodes (zig-zag path)
        self.graph.add_edge(node1, node2)
        self.graph.add_edge(node2, node3)
        self.graph.add_edge(node3, node4)
        self.graph.add_edge(node4, node5)
        self.graph.add_edge(node5, node6)
        self.graph.add_edge(node6, node7)
        self.graph.add_edge(node7, node8)
        # Add some extra connections for more complexity
        self.graph.add_edge(node2, node8)
        self.graph.add_edge(node3, node7)
        self.graph.add_edge(node4, node6)
        self.graph.add_edge(node1, node8)
        self.graph.add_edge(node3, node6)
        self.graph.add_edge(node4, node7)
        
        
        
        
        self.drag_start_node = None
        self.dragging = False
        
        self.font = pygame.font.SysFont(None, 32)
        
        # Load the arrow image for the back button
        arrow_path = os.path.join("assets", "arrow_left.png")
        self.arrow_img = pygame.image.load(arrow_path).convert_alpha()
        self.arrow_img = pygame.transform.smoothscale(self.arrow_img, (30, 30))

        # Back button to return to the main menu
        self.back_button = Button(pygame.Rect(SCREEN_WIDTH - 50, 10, 40, 40), color=Color.LIGHTBLUE, icon=self.arrow_img)

        # Create buttons
        self.buttons = self.create_default_buttons(object="Node", include_maze_button=False)
        
        
    def handle_event(self, event):
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
        
            if self.back_button.is_clicked((mouse_x, mouse_y)):
                self.app_state.current_screen = Screen.MAIN_MENU
                return
            
            for idx, button in enumerate(self.buttons):
                    if button.is_clicked((mouse_x, mouse_y)):
                        self.handle_button_click(idx)
                        
            node = self.graph.get_node(mouse_x, mouse_y)
            
            if node:
                if event.button == 1:  # Left click: set start/goal or select
                        # Set Start Mode
                    if self.local_app_state.set_start_mode:
                        # Clear previous start
                        for n in self.graph.nodes:
                            if n.state == State.START:
                                n.change_state(State.ACTIVATED)
                        node.change_state(State.START)
                        self.local_app_state.set_start_mode = False
                        self.local_app_state.set_goal_mode = False

                    # Set Goal Mode
                    elif self.local_app_state.set_goal_mode:
                        for n in self.graph.nodes:
                            if n.state.is_goal():
                                n.change_state(State.ACTIVATED)
                        node.change_state(State.GOAL)
                        self.local_app_state.set_goal_mode = False
                        self.local_app_state.set_start_mode = False   
                
                self.local_app_state.set_start_mode = False
                self.local_app_state.set_goal_mode = False
                
    
                if node and event.button == 1 and not (self.local_app_state.set_start_mode or self.local_app_state.set_goal_mode):
                    # Start dragging the node
                    self.drag_start_node = node
                    self.dragging = True   
                    
        # Ensure that when entering the screen, the ignore_drag flag is set to False              
        elif event.type == pygame.MOUSEBUTTONUP:
            self.local_app_state.ignore_drag = False
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.dragging and self.drag_start_node:
                node = self.graph.get_node(mouse_x, mouse_y)
                if event.button == 3 and node:
                    self.graph.remove_node(self.drag_start_node)  
                if event.button == 1 and node and node != self.drag_start_node:
                    # Add edge between drag_start_node and node
                    self.graph.add_edge(self.drag_start_node, node)
                self.drag_start_node = None
                self.dragging = False             
                
            else:
                if event.button == 1  and (SAFE_MIN_AREA <= mouse_x <= SAFE_MAX_AREA and
                SAFE_MIN_AREA + 10 <= mouse_y <= SAFE_MAX_AREA and
                self.graph.can_place_node(mouse_x, mouse_y)):
                    self.graph.add_node(mouse_x, mouse_y)
                    
                
    def handle_button_click(self, idx):
        
        # Deselect start and goal modes if any button is clicked
        self.local_app_state.set_start_mode = False
        self.local_app_state.set_goal_mode = False
        self.local_app_state.ignore_drag = True
        
        if idx == 0:
            # Set Start Mode
            self.local_app_state.set_start_mode = not self.local_app_state.set_start_mode
            self.local_app_state.set_goal_mode = False
        elif idx == 1:
            # Set Goal Mode
            self.local_app_state.set_goal_mode = not self.local_app_state.set_goal_mode
            self.local_app_state.set_start_mode = False
        elif idx == 7:
            # Reset Graph
            self.graph = Graph()
            
        else: # Algorithm buttons
            # Manage the state of the application
            if self.graph.get_start() is None or self.graph.get_goal() is None:
                return


            # Set the application state
            self.local_app_state.runned_algorithm = True
            self.local_app_state.grid_full_reset = False
            self.local_app_state.start_time = time.time()
            self.local_app_state.running_algorithm = True

            if idx == 2:
                self.algorithm = BFSAlgorithm(self.graph, self.graph.get_neighbors)
            elif idx == 3:
                self.algorithm = DFSAlgorithm(self.graph, self.graph.get_neighbors)
            elif idx == 4:
                self.algorithm = DijkstraAlgorithm(self.graph, self.graph.get_neighbors,self.graph.get_cost)
            elif idx == 5:
                self.algorithm = AStarAlgorithm(self.graph, self.graph.get_neighbors, self.graph.get_cost, euclidean_graph_heuristic)
            elif idx == 6:
                self.algorithm = GreedyBestFirstAlgorithm(self.graph, self.graph.get_neighbors, euclidean_graph_heuristic)


    def run(self):
        
        self.handle_mouse_drag()

        
        if self.local_app_state.running_algorithm:
            self.update_algorithm()
            time.sleep(1)

    def update_algorithm(self):

        self.local_app_state.execution_time = time.time() - self.local_app_state.start_time  
        if not self.algorithm.step():
            self.local_app_state.running_algorithm = False
            self.algorithm.highlight_path()  
    
    def is_mouse_near_edge(self, x1, y1, x2, y2, mouse_x, mouse_y, threshold=8):
        # Compute the distance from the mouse to the line segment (x1, y1)-(x2, y2)
        px = x2 - x1
        py = y2 - y1
        norm = px*px + py*py
        if norm == 0:
            # The edge is a point
            dist = math.hypot(mouse_x - x1, mouse_y - y1)
            return dist <= threshold
        u = ((mouse_x - x1) * px + (mouse_y - y1) * py) / norm
        u = max(0, min(1, u))
        closest_x = x1 + u * px
        closest_y = y1 + u * py
        dist = math.hypot(mouse_x - closest_x, mouse_y - closest_y)
        return dist <= threshold
    
    def get_edge_under_mouse(self, mouse_x, mouse_y, threshold=8):
        for edge in self.graph.edges:
            if self.is_mouse_near_edge(edge.node1.x, edge.node1.y, edge.node2.x, edge.node2.y, mouse_x, mouse_y, threshold):
                return edge
        return None

    def handle_mouse_drag(self):

        pos_x, pos_y = pygame.mouse.get_pos()
        
        # Get the mouse state
        mouse_state = pygame.mouse.get_pressed()
        # Handle mouse dragging action

        #If draggin with the right button, we can delete nodes
        if mouse_state[2]:

            # Reset the grid if an algorithm has been runned before
            node = self.graph.get_node(pos_x, pos_y)
            if node:
                self.graph.remove_node(node)
                
            edge = self.get_edge_under_mouse(pos_x, pos_y)
            if edge:
                self.graph.remove_edge(edge.node1, edge.node2)

        
    def draw(self):
        self.screen.fill(Color.BLACK)
        
        # Draw graph area
        pygame.draw.rect(
            self.screen,
            Color.GRAY,
            (GRAPH_AREA_MARGIN, GRAPH_AREA_MARGIN, GRAPH_AREA_SIZE, GRAPH_AREA_SIZE),
        )

        if self.dragging and self.drag_start_node:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            pygame.draw.line(
                self.screen,
                Color.WHITE,
                (self.drag_start_node.x, self.drag_start_node.y),
                (mouse_x, mouse_y),
                2
            )
    
        self.graph.draw(self.screen)
    
        # Draw buttons
        for idx, button in enumerate(self.buttons):
            if idx == 0:
                button.draw(self.screen, self.font, active=self.local_app_state.set_start_mode or self.local_app_state.running_algorithm)
            elif idx == 1:
                button.draw(self.screen, self.font, active=self.local_app_state.set_goal_mode or self.local_app_state.running_algorithm)
            elif idx >= 2 and idx <= 7:
                button.draw(self.screen, self.font, active=self.local_app_state.running_algorithm)
        
        self.back_button.draw(self.screen, self.font)