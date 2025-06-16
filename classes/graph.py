import pygame
from definitions.states import SquareState
from definitions.colors import Color
from definitions.graph_constants import NODE_RADIUS

class GraphNode:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.state = SquareState.ACTIVATED
        
    def draw(self, screen):
        if self.state.is_activated():
            pygame.draw.circle(screen, Color.WHITE, (self.x, self.y), NODE_RADIUS)
        elif self.state.is_start():
            pygame.draw.circle(screen, Color.GREEN, (self.x, self.y), NODE_RADIUS)
        elif self.state.is_goal():
            pygame.draw.circle(screen, Color.RED, (self.x, self.y), NODE_RADIUS)
        elif self.state.is_visited():
            pygame.draw.circle(screen, Color.PALEGREEN, (self.x, self.y), NODE_RADIUS)
        elif self.state.is_path():
            pygame.draw.circle(screen, Color.LIGHTBLUE, (self.x, self.y), NODE_RADIUS)
        elif self.state.is_frontier():
            pygame.draw.circle(screen, Color.ORANGE, (self.x, self.y), NODE_RADIUS)
        
    def is_point_inside(self, x, y):
        dx = self.x - x
        dy = self.y - y
        return (dx*dx + dy*dy) <= NODE_RADIUS*NODE_RADIUS
    
    def change_state(self, new_state):
        if not isinstance(new_state, SquareState):
            raise ValueError("new_state must be an instance of SquareState")
        
        self.state = new_state
        
class Graph:
    def __init__(self):
        self.id_counter = 1
        
        self.nodes = []
        self.edges = []

    def can_place_node(self, x, y):
        for node in self.nodes:
            dx = node.x - x
            dy = node.y - y
            if (dx*dx + dy*dy) < (2*NODE_RADIUS)**2:
                return False
        return True

    def add_node(self, x, y):
        node = GraphNode(x, y, self.id_counter)
        self.id_counter += 1
        self.nodes.append(node)
        
        return node
    
    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            # Remove edges connected to this node
            self.edges = [edge for edge in self.edges if edge[0] != node and edge[1] != node]
    
    def get_node(self, x, y):
        for node in self.nodes:
            if node.is_point_inside(x, y):
                return node
        return None
    
    def print_edges(self):
        for edge in self.edges:
            print(f"Edge from Node {edge[0].id} to Node {edge[1].id}")
    
    def add_edge(self, node1, node2):
        if node1 in self.nodes and node2 in self.nodes and node1 != node2 and (node1, node2) not in self.edges and (node2, node1) not in self.edges:
            self.edges.append((node1, node2))

    def remove_edge(self, node1, node2):
        if (node1, node2) in self.edges:
            self.edges.remove((node1, node2))
        elif (node2, node1) in self.edges:
            self.edges.remove((node2, node1))
        else:
            raise ValueError("Edge not found in the graph")
        
    def get_edge(self, node1, node2):
        for edge in self.edges:
            if (edge[0] == node1 and edge[1] == node2) or (edge[0] == node2 and edge[1] == node1):
                return edge
        return None
    
    def draw(self, screen):
        for edge in self.edges:
            pygame.draw.line(screen, Color.WHITE, (edge[0].x, edge[0].y), (edge[1].x, edge[1].y), 2)

        for node in self.nodes:
            node.draw(screen)
        

    def change_state(self, node, new_state):
        if node in self.nodes:
            node.change_state(new_state)
        else:
            raise ValueError("Node not found in the graph")
    