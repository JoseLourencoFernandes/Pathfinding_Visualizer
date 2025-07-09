import pygame
from definitions.states import State
from definitions.colors import Color
from definitions.graph_constants import NODE_RADIUS

class GraphNode:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.cost = 1
        self.state = State.ACTIVATED
        
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
        if not isinstance(new_state, State):
            raise ValueError("new_state must be an instance of SquareState")
        
        self.state = new_state
        
class Edge:
    def __init__(self, node1, node2, cost=1):
        if not isinstance(node1, GraphNode) or not isinstance(node2, GraphNode):
            raise ValueError("node1 and node2 must be instances of GraphNode")
        
        self.node1 = node1
        self.node2 = node2
        self.cost = cost
        self.state = State.ACTIVATED
        
    def draw(self, screen):
        if self.state.is_activated():
            pygame.draw.line(screen, Color.WHITE, (self.node1.x, self.node1.y), (self.node2.x, self.node2.y), 2)
        elif self.state.is_visited():
            pygame.draw.line(screen, Color.PALEGREEN, (self.node1.x, self.node1.y), (self.node2.x, self.node2.y), 2)
        elif self.state.is_path():
            pygame.draw.line(screen, Color.LIGHTBLUE, (self.node1.x, self.node1.y), (self.node2.x, self.node2.y), 2)
        elif self.state.is_frontier():
            pygame.draw.line(screen, Color.ORANGE, (self.node1.x, self.node1.y), (self.node2.x, self.node2.y), 2)
        
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
            self.edges = [edge for edge in self.edges if edge.node1 != node and edge.node2 != node]
    
    def get_node(self, x, y):
        for node in self.nodes:
            if node.is_point_inside(x, y):
                return node
        return None
    
    def print_edges(self):
        for edge in self.edges:
            print(f"Edge from Node {edge[0].id} to Node {edge[1].id}")
    
    def add_edge(self, node1, node2):
        if node1 in self.nodes and node2 in self.nodes and node1 != node2 and not self.get_edge(node1, node2):
            edge = Edge(node1, node2)
            self.edges.append(edge)

    def remove_edge(self, node1, node2):
        edge = self.get_edge(node1, node2)
        if edge:
            self.edges.remove(edge)
        else:
            raise ValueError("Edge not found between the specified nodes")
        
    def get_edge(self, node1, node2):
        for edge in self.edges:
            if (edge.node1 == node1 and edge.node2 == node2) or (edge.node1 == node2 and edge.node2 == node1):
                return edge
        return None
    
    def draw(self, screen):
        for edge in self.edges:
            edge.draw(screen)

        for node in self.nodes:
            node.draw(screen)
        

    def change_state(self, node, new_state):
        if node in self.nodes:
            node.change_state(new_state)
        else:
            raise ValueError("Node not found in the graph")
        
    def get_start(self):
        for node in self.nodes:
            if node.state.is_start():
                return node
        return None
    
    def get_goal(self):
        for node in self.nodes:
            if node.state.is_goal():
                return node
        return None
    
    def get_neighbors(self, node):
        neighbors = []
        for edge in self.edges:
            if edge.node1 == node:
                neighbors.append(edge.node2)
            elif edge.node2 == node:
                neighbors.append(edge.node1)
        return neighbors
    
    def get_cost(self, node1, node2):
        edge = self.get_edge(node1, node2)
        if edge:
            return edge.cost
        else:
            raise ValueError("Edge not found between the specified nodes")
        
    def mark_edge_visited(self, node1, node2):
        edge = self.get_edge(node1, node2)
        if edge:
            edge.state = State.VISITED
    
    def mark_edge_path(self, node1, node2):
        edge = self.get_edge(node1, node2)
        if edge:
            edge.state = State.PATH
            
    def mark_edge_frontier(self, node1, node2):
        edge = self.get_edge(node1, node2)
        if edge:
            edge.state = State.FRONTIER
            
def euclidean_graph_heuristic(node, goal):
    return ((node.x - goal.x) ** 2 + (node.y - goal.y) ** 2) ** 0.5