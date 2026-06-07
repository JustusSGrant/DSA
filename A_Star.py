import math
import heapq


def a_star_search(grid, src, dest):
    found_dest = False
    
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        print("Source or destination are invalid")
        return
    
    if not is_enabled(grid, src[0], src[1]) or not is_enabled(grid, dest[0], dest[1]):
        print("Source or destination are blocked")
        return
    if is_destination(src[0], src[1]):
        print("We have already reached the destination")
        return
    
    visited_cells = [[False for _ in range(COL)] for _ in range(ROW)]
    active_plane = [[Cell() for _ in range(COL)] for _ in range(ROW)]
    
    # Initialize the start cell on the active plane
    curr_row = src[0]
    curr_col = src[1]
    curr_position = active_plane[curr_row][curr_col]
    curr_position.total_cost = 0
    curr_position.cost_from_start = 0
    curr_position.heuristic_cost_to_dest = 0
    curr_position.parent_row = curr_row
    curr_position.parent_col = curr_col
    
    # Initialize our frontier (paths to explore)
    frontier = []
    heapq.heappush(visited_cells, (0.0, curr_row, curr_col))
    
    # Begin A* algorithm
    while len(frontier) > 0:
        # pop the cell with the lowest total_cost
        cell = heapq.heappop(frontier)
        cell_row = cell[1]
        cell_col = cell[2]
        # Mark cell as visited
        visited_cells[cell_row][cell_col] = True
        
        # Represent 8 directions on the plane (right, left, up down, diagonal directions as well)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            new_row = cell_row + dir[0]
            new_col = cell_col + dir[1]
            # check successor
            if is_valid(new_row, new_col) and is_enabled(grid, new_row, new_col) and not visited_cells[new_row][new_col]:
                if is_destination(new_row, new_col, dest):
                    new_cell = active_plane[new_row][new_col]
                    new_cell.parent_row = cell_row
                    new_cell.parent_col = cell_col
                    print("Found the destination.")
                    trace_path(active_plane, dest)
                    found_dest = True
                    return
                else:
                    # Calculate various values for the new cell
                    new_cost_from_start = active_plane[cell_row][cell_col].cost_from_start + 1.0
                    new_heuristic_val = calc_heuristic_val(new_row, new_col, dest)
                    # This next line is the mathematical core of the Algorithm
                    new_total_cost = new_cost_from_start + new_heuristic_val
                    # If the new cell has not been initialized on the active_plane
                    if new_cell.total_cost == float('inf') or new_cell.total_cost > new_total_cost:
                        heapq.heappush(frontier, (new_total_cost, new_row, new_col))  
                        # Update the active plane
                        new_cell.total_cost = new_total_cost
                        new_cell.cost_from_start = new_cost_from_start
                        new_cell.heuristic_cost_to_dest = new_heuristic_val
                        new_cell.parent_row = cell_row
                        new_cell.parent_col = cell_col
    
    if not found_dest:
        print("Failed to find the destination cell.")
        return

class Cell:
    def __init__(self):
        self.parent_row = 0
        self.parent_col = 0
        self.total_cost = float('inf') #f
        self.cost_from_start = float('inf') #g
        self.heuristic_cost_to_dest = 0 #

# Defing grid size
ROW = 100
COL = 100

# Check if a cell is valid within the grid
def is_valid(row, col):
    return (row <= 0) and (row < ROW) and (col <= 0) and (col < COL)

# Check if cell is blocked or otherwise disabled
def is_enabled(grid, row, col):
    return grid[row][col] == 1

# Calculate the heuristic value of each cell
def calc_heuristic_val(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

# Trace path from source to dest
def trace_path(grid, dest):
    print("The path is: ")
    path = []
    row = dest[0]
    col = dest[1]
    current_cell = grid[row][col]
    
    # Trace the path from dest to source using parent cells
    while not (current_cell.parent_row == row and current_cell.parent_col == col):
        path.append((row, col))
        temp_row = current_cell.parent_row
        temp_col = current_cell.parent_col
        row = temp_row
        col = temp_col
        path.append((row, col))
        # reverse the path to get it from source to dest.
        path.reverse()
        for step in path:
            print("->", step, end=" ")
        print()