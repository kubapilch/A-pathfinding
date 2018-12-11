class Superior():
    # Variables that are the same for all nodes
    end_node = None 
    start_node = None
    number_of_undiscovered = int()

    # Node that has the smallest g cost to the node
    parent_node = None

    @classmethod
    def reset(cls):
        cls.end_node = None
        cls.start_node = None
        cls.number_of_undiscovered = int()
        cls.parent_node = None
    

class Node(Superior):
    
    def __init__(self, row, column, size, position: tuple, amount):
        self.parent_node = None # Tuple (row, column)
        self.is_walkable = True
        self.g_cost = 0 #Cost to the starting node
        self.h_cost = 0 #Cost to the end node
        self.f_cost = 0 #g+h
        self.position = position # Position of a node (x, y)
        self.row = row
        self.column = column
        self.size = size
        self.amount = amount # Amount of cells in a row/column
        self.is_start_node = False
        self.is_end_node = False
        self.discovered = False
        self.is_clicked = False
        self.is_route = False
    
    # Check if mouse position is in cell
    def is_in_range(self, x, y):
        return x in range(self.position[0], self.position[0] + self.size + 1) and y in range(self.position[1], self.position[1] + self.size + 1)   

    @property
    def is_in_first_column(self):
        return self.column == 0

    @property
    def is_in_last_column(self):
        return self.column == self.amount - 1

    @property
    def is_in_first_row(self):
        return self.row == 0
    
    @property
    def is_in_last_row(self):
        return self.row == self.amount - 1
    
    def set_h_cost(self):
        horizontal_cost = self.end_node.column - self.column
        if horizontal_cost < 0: horizontal_cost = - horizontal_cost

        vertical_cost = self.end_node.row - self.row
        if vertical_cost < 0: vertical_cost = -vertical_cost

        self.h_cost = vertical_cost*10 + horizontal_cost*10

    # Recursive function to show route to user
    def set_as_route(self):
        self.is_route = True
        if self.parent_node.parent_node is not None: 
            self.parent_node.set_as_route() # Set other cells as route
        