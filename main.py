import pygame
from node import Node, Superior
from random import randrange
import atexit

class Game():

    # FPS variables
    FPS = 30
    clock = pygame.time.Clock()

    def __init__(self, size, amount, g_and_h_cost=False, f_cost=False, AI=True, speed=10):
        pygame.init()
        self.AI = AI
        self.AI_speed = speed
        self.font = pygame.font.SysFont("monospace", int(size/4)+1)
        boundary = size*amount + amount - 1
        self.amount = amount
        self.size = size
        self.display = pygame.display.set_mode((boundary, boundary))
        self.show_g_and_h_cost = g_and_h_cost
        self.show_f_cost = f_cost
        atexit.register(self.cleanup)
    
    def create_grid(self, amount, size):
        grid = list()
        for row in range(0, amount):
            placeholder = list()
            for column in range(0, amount):
                cell = Node(row, column, size, (column * size + column, row * size + row), amount)
                placeholder.append(cell)
            grid.append(placeholder)
        Superior.number_of_undiscovered = amount**2 - 2
        return grid

    def show_grid(self, grid):
        # Colors
        red = (255, 0, 0)
        green = (0, 255, 0)
        yellow = (255, 255, 0)
        blue = (0, 0, 255)
        black = (0, 0, 0)
        grey = (215, 215, 193)

        for row in grid:
            for cell in row:
                # Labels for costs vizualization
                glabel = self.font.render(str(cell.g_cost), 1, black)
                hlabel = self.font.render(str(cell.h_cost), 1, black)
                flabel = self.font.render(str(cell.f_cost), 1, black)

                if cell.is_start_node:
                    # Starting node
                    pygame.draw.rect(self.display, green, [cell.position[0], cell.position[1], cell.size, cell.size])
                elif cell.is_route:
                    # Route
                    pygame.draw.rect(self.display, green, [cell.position[0], cell.position[1], cell.size, cell.size])
                elif cell.is_end_node:
                    # End node
                    pygame.draw.rect(self.display, yellow, [cell.position[0], cell.position[1], cell.size, cell.size])
                elif not cell.is_walkable:
                    # Wall
                    pygame.draw.rect(self.display, black, [cell.position[0], cell.position[1], cell.size, cell.size])
                elif cell.parent_node is not None:
                    # Any other node that has been discovered
                    if cell.is_clicked:
                        # Clicked node
                        pygame.draw.rect(self.display, red, [cell.position[0], cell.position[1], cell.size, cell.size])
                    else:
                        # Not clicked node
                        pygame.draw.rect(self.display, blue, [cell.position[0], cell.position[1], cell.size, cell.size])
                    
                    # Check if user wants to show labels
                    if self.show_g_and_h_cost:
                        self.display.blit(glabel, cell.position)
                        self.display.blit(hlabel, (cell.position[0]  + (cell.size/2), cell.position[1]))
                    
                    if self.show_f_cost:
                        self.display.blit(flabel, (cell.position[0] + (cell.size/3), cell.position[1] + (cell.size/2)))
                else:
                    # Not discovered nodes
                    pygame.draw.rect(self.display, grey, [cell.position[0], cell.position[1], cell.size, cell.size])
                
        pygame.display.update()

    def checkNeighbors(self, grid, cell: Node):
        found = bool()
        
        # Top node
        if not cell.is_in_first_row:
            neighbor = grid[cell.row - 1][cell.column]
            if neighbor.is_walkable and not neighbor.is_start_node and not neighbor.is_end_node:
                neighbor.discovered = True
                if neighbor.parent_node is None or cell.g_cost + 10  + neighbor.h_cost < neighbor.f_cost:
                    neighbor.g_cost = cell.g_cost + 10
                    neighbor.set_h_cost()
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                    neighbor.parent_node = cell

            # Look for end node
            if neighbor.is_end_node:
                neighbor.parent_node = cell
                neighbor.set_as_route()
                found = True
                
        # Bottom node
        if not cell.is_in_last_row:
            neighbor = grid[cell.row + 1][cell.column]
            if neighbor.is_walkable and not neighbor.is_start_node and not neighbor.is_end_node:
                neighbor.discovered = True
                if neighbor.parent_node is None or cell.g_cost + 10  + neighbor.h_cost < neighbor.f_cost:
                    neighbor.g_cost = cell.g_cost + 10
                    neighbor.set_h_cost()
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                    neighbor.parent_node = cell
            
            # Look for end node
            if neighbor.is_end_node:
                neighbor.parent_node = cell
                neighbor.set_as_route()
                found = True

        # Left node
        if not cell.is_in_first_column:
            neighbor = grid[cell.row][cell.column - 1]
            if neighbor.is_walkable and not neighbor.is_start_node and not neighbor.is_end_node:
                neighbor.discovered = True
                if neighbor.parent_node is None or cell.g_cost + 10  + neighbor.h_cost < neighbor.f_cost:
                    neighbor.g_cost = cell.g_cost + 10
                    neighbor.set_h_cost()
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                    neighbor.parent_node = cell
            
            # Look for end node
            if neighbor.is_end_node:
                neighbor.parent_node = cell
                neighbor.set_as_route()
                found = True

        # Right node
        if not cell.is_in_last_column:
            neighbor = grid[cell.row][cell.column + 1]
            if neighbor.is_walkable and not neighbor.is_start_node and not neighbor.is_end_node:
                neighbor.discovered = True
                if neighbor.parent_node is None or cell.g_cost + 10  + neighbor.h_cost < neighbor.f_cost:
                    neighbor.g_cost = cell.g_cost + 10
                    neighbor.set_h_cost()
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                    neighbor.parent_node = cell
            
            # Look for end node
            if neighbor.is_end_node:
                neighbor.parent_node = cell
                neighbor.set_as_route()
                found = True
        
        # Top left node
        if not cell.is_in_first_row and not cell.is_in_first_column:
            neighbor = grid[cell.row - 1][cell.column - 1]
            if neighbor.is_walkable and not neighbor.is_start_node and not neighbor.is_end_node:
                neighbor.discovered = True
                if neighbor.parent_node is None or cell.g_cost + 14  + neighbor.h_cost < neighbor.f_cost:
                    neighbor.g_cost = cell.g_cost + 14
                    neighbor.set_h_cost()
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                    neighbor.parent_node = cell
            
            # Look for end node
            if neighbor.is_end_node:
                neighbor.parent_node = cell
                neighbor.set_as_route()
                found = True
        
        # Top right node
        if not cell.is_in_first_row and not cell.is_in_last_column:
            neighbor = grid[cell.row - 1][cell.column + 1]
            if neighbor.is_walkable and not neighbor.is_start_node and not neighbor.is_end_node:
                neighbor.discovered = True
                if neighbor.parent_node is None or cell.g_cost + 14  + neighbor.h_cost < neighbor.f_cost:
                    neighbor.g_cost = cell.g_cost + 14
                    neighbor.set_h_cost()
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                    neighbor.parent_node = cell
            
            # Look for end node
            if neighbor.is_end_node:
                neighbor.parent_node = cell
                neighbor.set_as_route()
                found = True
        
        # Bottom left node
        if not cell.is_in_last_row and not cell.is_in_first_column:
            neighbor = grid[cell.row + 1][cell.column - 1]
            if neighbor.is_walkable and not neighbor.is_start_node and not neighbor.is_end_node:
                neighbor.discovered = True
                if neighbor.parent_node is None or cell.g_cost + 14  + neighbor.h_cost < neighbor.f_cost:
                    neighbor.g_cost = cell.g_cost + 14
                    neighbor.set_h_cost()
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                    neighbor.parent_node = cell
            
            # Look for end node 
            if neighbor.is_end_node:
                neighbor.parent_node = cell
                neighbor.set_as_route()
                found = True
        
        # Bottom right node
        if not cell.is_in_last_row and not cell.is_in_last_column:
            neighbor = grid[cell.row + 1][cell.column + 1]
            if neighbor.is_walkable and not neighbor.is_start_node and not neighbor.is_end_node:
                neighbor.discovered = True
                if neighbor.parent_node is None or cell.g_cost + 14  + neighbor.h_cost < neighbor.f_cost:
                    neighbor.g_cost = cell.g_cost + 14
                    neighbor.set_h_cost()
                    neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                    neighbor.parent_node = cell
            
            # Look for end node
            if neighbor.is_end_node:
                neighbor.parent_node = cell
                neighbor.set_as_route()
                found = True

        return found
    
    def pick_node(self, grid):
        lowest_f = int()
        cells_with_lowest_f = list()
        counter = 0

        for row in grid:
            for cell in row:
                
                #Check if cell is end cell (when start node and end node are next to each other)
                if cell.is_end_node:
                    row_diffrence = cell.end_node.row - Superior.start_node.row
                    column_difference = cell.end_node.column - Superior.start_node.column

                    if row_diffrence < 0: 
                        row_diffrence = -row_diffrence
                    if column_difference < 0: 
                        column_difference = -column_difference
                    
                    if row_diffrence == 1 and column_difference == 1:
                        return cell
                
                # Check nodes
                if not cell.discovered or cell.is_start_node or cell.is_clicked: continue

                # Set first value
                if counter == 0:
                    lowest_f = cell.f_cost
                    counter += 1

                # Find lowest f cost and nodes with lowest f cost
                if cell.f_cost < lowest_f:
                    lowest_f = cell.f_cost
                    cells_with_lowest_f = []
                    cells_with_lowest_f.append(cell)
                elif cell.f_cost == lowest_f:
                    cells_with_lowest_f.append(cell)
        
        random = randrange(0, len(cells_with_lowest_f))
        return cells_with_lowest_f[random]
        
    def main_loop(self):
        grid = self.create_grid(self.amount, self.size)
        self.show_grid(grid)
        
        exit_game = False

        # Stage indicators
        stages = ("Start node placement", "End node placement", "Walls placement", "Game")
        stage = 0

        # Drawing variables
        mouse_pressed = False
        highlighted_cells = []

        print(f"Stage: {stages[stage]}")

        while not exit_game:
            for event in pygame.event.get():
                # Check if user wants to quit the game
                if event.type == pygame.QUIT:
                    exit_game = True
                    self.cleanup()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    
                    # Place start node
                    if stage == 0:
                        for row in grid:
                            for cell in row:
                                if cell.is_in_range(x=mouse_position[0], y=mouse_position[1]):
                                    
                                    # Find old start node index and set it to False
                                    if cell.start_node is not None:
                                        old_start_node_row = [x for x in grid if cell.start_node in x][0]
                                        old_parent_node_column_index = old_start_node_row.index(cell.start_node)
                                        old_start_node_row_index = grid.index([x for x in grid if cell.start_node in x][0])
                                        grid[old_start_node_row_index][old_parent_node_column_index].is_start_node = False
                                        cell.discovered = False
                                        cell.is_clicked = False

                                    # Set new start node
                                    Superior.start_node = cell
                                    cell.is_start_node = True
                                    cell.discovered = True
                                    cell.is_clicked = True

                    # Place end node
                    if stage == 1:
                        for row in grid:
                            for cell in row:
                                if cell.is_in_range(x=mouse_position[0], y=mouse_position[1]) and not cell.is_start_node:

                                    # Find old start node index and set it to False
                                    if cell.end_node is not None:
                                        old_end_node_row = [x for x in grid if cell.end_node in x][0]
                                        old_parent_node_column_index = old_end_node_row.index(cell.end_node)
                                        old_end_node_row_index = grid.index([x for x in grid if cell.end_node in x][0])
                                        grid[old_end_node_row_index][old_parent_node_column_index].is_end_node = False
                                        cell.is_clicked = False
                                    
                                    # Set new end node
                                    Superior.end_node = cell
                                    cell.is_end_node = True
                                    cell.is_clicked = True
                    
                    # Start drawing
                    if stage == 2:
                        mouse_pressed = True

                    # Step on cell
                    if stage == 3:
                        for row in grid:
                            for cell in row:
                                if cell.is_in_range(mouse_position[0], mouse_position[1]) and not cell.is_end_node and not cell.is_start_node and cell.parent_node is not None and not self.AI:
                                    found = self.checkNeighbors(grid, cell)
                                    cell.is_clicked = True
                                    if found:
                                        stage += 1
                                        print("Route found!")
                
                # Stop drawing
                if event.type == pygame.MOUSEBUTTONUP and stage == 2:
                    mouse_pressed = False
                    highlighted_cells = []

                # Move to next stage
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and stage < 3:
                        stage += 1
                        print(f"Stage: {stages[stage]}")

                        # Discover nodes around the starting point
                        if stage == 3:
                            for row in grid:
                                for cell in row:
                                    if cell.is_start_node:
                                        self.checkNeighbors(grid, cell)
                            
                            # If AI mode is on change FPS
                            if self.AI:
                                self.FPS = self.AI_speed
                    elif event.key == pygame.K_SPACE and stage == 4:
                        exit_game = True
                        Superior().reset()
                        
            # Place walls
            if mouse_pressed:
                mouse_position = pygame.mouse.get_pos()
                for row in grid:
                    for cell in row:
                        if cell.is_in_range(x=mouse_position[0], y=mouse_position[1]) and not cell.is_start_node and not cell.is_end_node and cell not in highlighted_cells:
                            cell.is_walkable = not cell.is_walkable
                            if cell.is_walkable:
                                Superior.number_of_undiscovered += 1
                            else:
                                Superior.number_of_undiscovered -= 1
                            
                            self.show_grid(grid)
                            highlighted_cells.append(cell)

            # Check if mode is set to AI
            if self.AI and stage == 3:
                # Check if there is any undiscovered node
                if Superior.number_of_undiscovered == 0:
                    stage += 1
                    print("There is no route!")
                    continue

                # Pick node
                node = self.pick_node(grid)
                
                # Checl if node is end node
                if cell.is_end_node:
                    stage += 1
                    self.FPS = 30
                    print("Route found!")
                
                # Move one step
                node.is_clicked = True
                found = self.checkNeighbors(grid, node)
                
                Superior.number_of_undiscovered -= 1

                # Check if end node is found
                if found:
                    stage += 1
                    self.FPS = 30
                    print("Route found!")

            self.show_grid(grid)
            self.clock.tick(self.FPS)

    def play(self):
        while True:
            self.main_loop()

    @staticmethod
    def cleanup():
        pygame.quit()
        quit()

if __name__ == "__main__":
    game = Game(20, 30, speed=30)
    game.play()
    