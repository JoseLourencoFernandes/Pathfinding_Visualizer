import pygame
from definitions.states import State
from definitions.colors import Color
from definitions.graph_constants import NODE_RADIUS

class GraphNode:
    """
    A class to represent a node in a graph.
    Each node has a position (x, y) and a state.
    Provides methods to draw the node, check if a point is inside the node, and change its state.
    
    :param x: The x-coordinate of the node.
    :type x: int
    :param y: The y-coordinate of the node.
    :type y: int
    :param state: The state of the node, default is State.ACTIVATED.
    :type state: State
    """
    x: int
    y: int
    state: State

    def __init__(self, x: int, y: int) -> None:
        """ Constructor for GraphNode. """
        self.x = x
        self.y = y
        self.state = State.ACTIVATED

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the node on the given screen based on its state.
        
        :param screen: The pygame screen where the node will be drawn.
        :type screen: pygame.Surface
        """
        color = self.state.get_color("graph")
        pygame.draw.circle(screen, color, (self.x, self.y), NODE_RADIUS)
        
    def is_point_inside(self, x: int, y: int) -> bool:
        """
        Checks if a point (x, y) is inside the node's area.
        
        :param x: The x-coordinate of the point to check.
        :type x: int
        :param y: The y-coordinate of the point to check.
        :type y: int
        
        :return: True if the point is inside the node's area, False otherwise.
        :rtype: bool
        """
        dx = self.x - x
        dy = self.y - y
        return (dx*dx + dy*dy) <= NODE_RADIUS*NODE_RADIUS

    def change_state(self, new_state: State) -> None:
        """
        Changes the state of the node to a new state.
        :param new_state: The new state to set for the node.
        :type new_state: State
        
        :raises ValueError: If new_state is not an instance of State.
        :raises TypeError: If new_state is not an instance of State.
        """
        if not isinstance(new_state, State):
            raise TypeError("new_state must be an instance of State")

        self.state = new_state
        
class Edge:
    """
    A class to represent an edge in a graph.
    Each edge connects two GraphNode instances and has a cost and state.
    
    :param node1: The first node connected by the edge.
    :type node1: GraphNode
    :param node2: The second node connected by the edge.
    :type node2: GraphNode
    :param cost: The cost associated with the edge (default is 1).
    :type cost: int
    :param state: The state of the edge, default is State.ACTIVATED.
    :type state: State
    :param cost_surface: A pygame.Surface to hold the cost text (default is None).
    :type cost_surface: pygame.Surface | None
    """
    node1: GraphNode
    node2: GraphNode
    cost: int
    state: State
    cost_surface: pygame.Surface

    def __init__(self, node1: GraphNode, node2: GraphNode, cost: int = 1) -> None:
        """ 
        Constructor for Edge. 
        Initializes the edge connecting two graph nodes with a cost and state.
        
        :param node1: The first node connected by the edge.
        :type node1: GraphNode
        :param node2: The second node connected by the edge.
        :type node2: GraphNode
        :param cost: The cost associated with the edge (default is 1).
        :type cost: int
        :param state: The state of the edge, default is State.ACTIVATED.
        :type state: State
        
        :raises ValueError: If node1 or node2 is not an instance of GraphNode.
        :raises TypeError: If node1 or node2 is not an instance of GraphNode
        """
        if not isinstance(node1, GraphNode) or not isinstance(node2, GraphNode):
            raise ValueError("node1 and node2 must be instances of GraphNode")
        
        self.node1 = node1
        self.node2 = node2
        self.cost = cost
        self.state = State.ACTIVATED
        self.cost_surface = None  # Surface to hold the cost text

    def get_cost_surface(self) -> pygame.Surface:
        """
        Returns the cost surface for the edge, rendering it if not already cached.

        :return: The surface containing the cost text.
        :rtype: pygame.Surface 
        """
        if self.cost_surface is None:
            font_size = 18
            font = pygame.font.Font(None, font_size)
            
            text_color = Color.BLACK
            outline_color = Color.WHITE
            
            # Create text surface with outline effect
            text_surface = font.render(str(self.cost), True, text_color)
            outline_surface = font.render(str(self.cost), True, outline_color)
            
            w, h = text_surface.get_size()
            self.cost_surface = pygame.Surface((w + 4, h + 4), pygame.SRCALPHA)
            
            # Draw outline by blitting the outline text at multiple positions
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:  # Skip the center position
                        self.cost_surface.blit(outline_surface, (dx + 2, dy + 2))
            
            # Draw the main text on top
            self.cost_surface.blit(text_surface, (2, 2))
            
        return self.cost_surface
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the edge on the given screen based on its state.
        
        :param screen: The pygame screen where the edge will be drawn.
        :type screen: pygame.Surface
        """
        color = self.state.get_color("graph")
        line_width = 3 if self.state.is_path() else 2
        pygame.draw.line(screen, color, (self.node1.x, self.node1.y), (self.node2.x, self.node2.y), line_width)

    def draw_cost(self, screen: pygame.Surface) -> None:
        """
        Draws the cost of the edge on the screen.
        This method retrieves the cost surface and blits it onto the screen at the edge's center.

        :param screen: The screen on which to draw the cost.
        """
        surface = self.get_cost_surface()
        
        # Calculate the midpoint of the edge
        mid_x = (self.node1.x + self.node2.x) // 2
        mid_y = (self.node1.y + self.node2.y) // 2
        
        # Calculate edge direction and perpendicular offset for better positioning
        dx = self.node2.x - self.node1.x
        dy = self.node2.y - self.node1.y
        edge_length = (dx*dx + dy*dy) ** 0.5
        
        if edge_length > 0:
            # Normalize the perpendicular vector (rotate 90 degrees)
            perp_x = -dy / edge_length
            perp_y = dx / edge_length
            
            # Offset the text slightly away from the edge line
            offset_distance = 12  # pixels away from the edge
            text_x = mid_x + perp_x * offset_distance
            text_y = mid_y + perp_y * offset_distance
        else:
            text_x = mid_x
            text_y = mid_y
        
        # Draw a small background rectangle for better readability
        text_rect = surface.get_rect(center=(int(text_x), int(text_y)))
        background_rect = text_rect.inflate(4, 2)  # Add some padding
        pygame.draw.rect(screen, Color.WHITE, background_rect)
        pygame.draw.rect(screen, Color.BLACK, background_rect, 1)  # Border
        
        # Draw the text
        screen.blit(surface, text_rect)
        
class Graph:
    """
    Represents a graph structure consisting of nodes and edges.
    Provides methods to add and remove nodes and edges, check placement of nodes,
    retrieve nodes and edges, and draw the graph.
    
    :param nodes: A list of GraphNode instances representing the nodes in the graph.
    :type nodes: list[GraphNode]
    :param edges: A list of Edge instances representing the edges in the graph.
    :type edges: list[Edge]
    :param customizable_cost: A boolean indicating if the graph allows customizable costs for edges.
    :type customizable_cost: bool
    """
    nodes: list[GraphNode]
    edges: list[Edge]
    customizable_cost: bool
    
    def __init__(self, customizable_cost: bool = False) -> None:
        """ Constructor for Graph. Initializes an empty graph. """
        self.nodes = []
        self.edges = []
        self.customizable_cost = customizable_cost

    def can_place_node(self, x: int, y: int) -> bool:
        """
        Checks if a node can be placed at the given coordinates (x, y).
        This method checks if the coordinates are far enough from existing nodes
        to avoid overlap.
        
        :param x: The x-coordinate where the node is to be placed.
        :type x: int
        :param y: The y-coordinate where the node is to be placed.
        :type y: int
        
        :return: True if the node can be placed, False otherwise.
        :rtype: bool
        """
        for node in self.nodes:
            dx = node.x - x
            dy = node.y - y
            if (dx*dx + dy*dy) < (2*NODE_RADIUS)**2:
                return False
        return True

    def add_node(self, x: int, y: int) -> GraphNode:
        """
        Adds a new node to the graph at the specified coordinates (x, y).
        
        :param x: The x-coordinate of the node.
        :type x: int
        :param y: The y-coordinate of the node.
        :type y: int
        
        :return: The newly created GraphNode instance.
        :rtype: GraphNode
        """
        node = GraphNode(x, y)
        self.nodes.append(node)
        
        return node
    
    def remove_node(self, node: GraphNode) -> None:
        """
        Removes a node from the graph and all edges connected to it.
        
        :param node: The GraphNode instance to be removed.
        :type node: GraphNode
        """
        if node in self.nodes:
            self.nodes.remove(node)
            # Remove edges connected to this node
            self.edges = [edge for edge in self.edges if edge.node1 != node and edge.node2 != node]

    def get_node(self, x: int, y: int) -> GraphNode | None:
        """
        Retrieves a node from the graph based on its position (x, y).
        This method checks if the point (x, y) is inside any of the existing nodes.
        
        :param x: The x-coordinate of the point to check.
        :type x: int
        :param y: The y-coordinate of the point to check.
        :type y: int
        
        :return: The GraphNode instance if found, None otherwise.
        :rtype: GraphNode | None
        """
        for node in self.nodes:
            if node.is_point_inside(x, y):
                return node
        return None

    def add_edge(self, node1: GraphNode, node2: GraphNode) -> None:
        """
        Adds an edge between two nodes in the graph.
        This method checks if both nodes exist in the graph, are not the same node,
        and if an edge between them does not already exist.
        
        :param node1: The first GraphNode instance to connect.
        :type node1: GraphNode
        :param node2: The second GraphNode instance to connect.
        :type node2: GraphNode
        """
        if node1 in self.nodes and node2 in self.nodes and node1 != node2 and not self.get_edge(node1, node2):
            edge = Edge(node1, node2)
            self.edges.append(edge)

    def remove_edge(self, node1: GraphNode, node2: GraphNode) -> None:
        """
        Removes an edge between two nodes in the graph.
        This method checks if the edge exists between the specified nodes and removes it.
        
        :param node1: The first GraphNode instance connected by the edge.
        :type node1: GraphNode
        :param node2: The second GraphNode instance connected by the edge.
        :type node2: GraphNode
        
        :raises ValueError: If the edge is not found between the specified nodes.
        """
        if edge := self.get_edge(node1, node2):
            self.edges.remove(edge)
        else:
            raise ValueError("Edge not found between the specified nodes")

    def get_edge(self, node1: GraphNode, node2: GraphNode) -> Edge | None:
        """
        Retrieves an edge between two nodes in the graph.
        This method checks if an edge exists between the specified nodes and returns it.
        
        :param node1: The first GraphNode instance connected by the edge.
        :type node1: GraphNode
        :param node2: The second GraphNode instance connected by the edge.
        :type node2: GraphNode
        
        :return: The Edge instance if found, None otherwise.
        :rtype: Edge | None
        """
        for edge in self.edges:
            if (edge.node1 == node1 and edge.node2 == node2) or (edge.node1 == node2 and edge.node2 == node1):
                return edge
        return None
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the graph on the given screen.

        :param screen: The pygame screen where the graph will be drawn.
        :type screen: pygame.Surface
        """
            
        for edge in self.edges:
            edge.draw(screen)
            
        for node in self.nodes:
            node.draw(screen)
            
        if self.customizable_cost:
            for edge in self.edges:
                edge.draw_cost(screen)
        

    def change_state(self, node: GraphNode, new_state: State) -> None:
        """
        Changes the state of a node in the graph.

        :param node: The GraphNode instance whose state will be changed.
        :type node: GraphNode
        :param new_state: The new state to assign to the node.
        :type new_state: State
        """
        if node in self.nodes:
            node.change_state(new_state)
        else:
            raise ValueError("Node not found in the graph")

    def get_start(self) -> GraphNode | None:
        """
        Retrieves the start node from the graph.

        :return: The start GraphNode instance if found, None otherwise.
        :rtype: GraphNode | None
        """
        for node in self.nodes:
            if node.state.is_start():
                return node
        return None

    def get_goal(self) -> GraphNode | None:
        """
        Retrieves the goal node from the graph.

        :return: The goal GraphNode instance if found, None otherwise.
        :rtype: GraphNode | None
        """
        for node in self.nodes:
            if node.state.is_goal():
                return node
        return None
    
    def get_neighbors(self, node: GraphNode) -> list[GraphNode]:
        """
        Retrieves the neighbors of a given node in the graph.
        
        :param node: The GraphNode instance whose neighbors will be retrieved.
        :type node: GraphNode
        
        :return: A list of GraphNode instances that are neighbors of the specified node.
        :rtype: list[GraphNode]
        """
        neighbors = []
        for edge in self.edges:
            if edge.node1 == node:
                neighbors.append(edge.node2)
            elif edge.node2 == node:
                neighbors.append(edge.node1)
        return neighbors
    
    def get_cost(self, node1: GraphNode, node2: GraphNode) -> float | None:
        """
        Retrieves the cost of the edge connecting two nodes in the graph.
        This method checks if an edge exists between the specified nodes and returns its cost.

        :param node1: The first GraphNode instance connected by the edge.
        :type node1: GraphNode
        :param node2: The second GraphNode instance connected by the edge.
        :type node2: GraphNode

        :return: The cost of the edge if found, None otherwise.
        :rtype: float | None
        """
        edge = self.get_edge(node1, node2)
        if edge:
            return edge.cost
        else:
            raise ValueError("Edge not found between the specified nodes")

    def mark_edge_visited(self, node1: GraphNode, node2: GraphNode) -> None:
        """ Marks the edge between two nodes as visited. """
        edge = self.get_edge(node1, node2)
        if edge:
            edge.state = State.VISITED

    def mark_edge_path(self, node1: GraphNode, node2: GraphNode) -> None:
        """ Marks the edge between two nodes as part of the path."""
        edge = self.get_edge(node1, node2)
        if edge:
            edge.state = State.PATH

    def mark_edge_frontier(self, node1: GraphNode, node2: GraphNode) -> None:
        """ Marks the edge between two nodes as part of the frontier. """
        edge = self.get_edge(node1, node2)
        if edge:
            edge.state = State.FRONTIER

def euclidean_graph_heuristic(node: GraphNode, goal: GraphNode) -> float:
    """ Calculates the Euclidean distance between a node and the goal node."""
    return ((node.x - goal.x) ** 2 + (node.y - goal.y) ** 2) ** 0.5