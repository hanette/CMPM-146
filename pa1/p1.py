from p1_support import load_level, show_level, save_level_costs
from math import sqrt
# from math import inf, sqrt
from heapq import heappop, heappush

def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.
    """

    #Initialize Lists/Dicts
    queue = [(0,initial_position)]
    dist = {}
    prev = {}
    path = []
    prev[initial_position] = None
    dist[initial_position] = 0

    #while priority queue still valid
    while queue:
        running_cost, current_cell = heappop(queue)
        #If at destination backtrack appending shortest path
        if current_cell == destination:
            backtrack = current_cell
            while prev[backtrack] != None:
                path.insert(0,backtrack)
                backtrack = prev[backtrack]
            path.insert(0,backtrack)
            print ('total cost =  ', running_cost,'\n')
            return path
        #If not goal, add to queue w cost or ignore
        else:
            for cell, cost in navigation_edges(graph, current_cell):
                pathcost = cost + dist[current_cell]
                if cell not in prev.keys() or pathcost < dist[cell]:
                    dist[cell] = pathcost
                    prev[cell] = current_cell
                    heappush(queue, (pathcost,cell))

    return None

def dijkstras_shortest_cost(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return the cost.
        Otherwise, return None.
    """

    queue = [(0,initial_position)]
    dist = {}
    prev = {}

    prev[initial_position] = None
    dist[initial_position] = 0

    while queue:
        running_cost, current_cell = heappop(queue)
        if current_cell == destination:
            return running_cost
        else:
            for cell, cost in navigation_edges(graph, current_cell):
                pathcost = cost + dist[current_cell]
                if cell not in prev.keys():
                    dist[cell] = pathcost
                    prev[cell] = current_cell
                    heappush(queue, (pathcost,cell))
                elif pathcost < dist[cell]:
                    dist[cell] = pathcost
                    prev[cell] = current_cell
                    heappush(queue, (pathcost,cell))
    return None


def dijkstras_shortest_path_to_all(initial_position, graph, adj):

    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """

    xs, ys = zip(*(list(graph['spaces'].keys()) + list(graph['walls'])))
    x_lo, x_hi = min(xs), max(xs)
    y_lo, y_hi = min(ys), max(ys)
    finaldict = {}

    #Iterate through each cell and find the cost to get there
    for j in range(y_lo, y_hi + 1):
        for i in range(x_lo, x_hi + 1):
            cell = (i, j) #cell we are calculating for
            totalcost = dijkstras_shortest_cost(initial_position, cell, graph, adj)

            if totalcost != None:
                finaldict[cell] = totalcost
            else:
                finaldict[cell] = "inf"
    return finaldict


def navigation_edges(level, cell):

    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    final = [] #contain adj coordinates

    # left
    templist = list(cell) # change to list to edit
    templist[0] -= 1 # change left coord (col)
    tempcell = tuple(templist) # revert back to tuple
    init_cost = cell_cost(level, cell) # cost of current cell
    tempcost = calculate_cost(level, tempcell, 0, init_cost) #cost to get there

    if tempcost != None:
        temptuple = (tempcell, tempcost)
        final.append(temptuple) # add to final list

    # top-left
    templist = list(cell) # change to list to edit
    templist[0] -= 1 # change left coord (col)
    templist[1] -= 1 # change right coord (row)
    tempcell = tuple(templist) # revert back to tuple
    init_cost = cell_cost(level, cell) # cost of current cell
    tempcost = calculate_cost(level, tempcell, 1, init_cost) #cost to get there
    if tempcost != None:
        temptuple = (tempcell, tempcost)
        final.append(temptuple) # add to final list

    # top
    templist = list(cell) # change to list to edit
    templist[1] -= 1 # change right coord (row)
    tempcell = tuple(templist) # revert back to tuple
    init_cost = cell_cost(level, cell) # cost of current cell
    tempcost = calculate_cost(level, tempcell, 0, init_cost) #cost to get there
    if tempcost != None:
        temptuple = (tempcell, tempcost)
        final.append(temptuple) # add to final list

    # top-right
    templist = list(cell) # change to list to edit
    templist[0] += 1 # change left coord (col)
    templist[1] -= 1 # change right coord (row)
    tempcell = tuple(templist) # revert back to tuple
    init_cost = cell_cost(level, cell) # cost of current cell
    tempcost = calculate_cost(level, tempcell, 1, init_cost) #cost to get there
    if tempcost != None:
        temptuple = (tempcell, tempcost)
        final.append(temptuple) # add to final list

    # right
    templist = list(cell) # change to list to edit
    templist[0] += 1 # change left coord (col)
    tempcell = tuple(templist) # revert back to tuple
    init_cost = cell_cost(level, cell) # cost of current cell
    tempcost = calculate_cost(level, tempcell, 0, init_cost) #cost to get there
    if tempcost != None:
        temptuple = (tempcell, tempcost)
        final.append(temptuple) # add to final list

    # bottom-right
    templist = list(cell) # change to list to edit
    templist[0] += 1 # change left coord (col)
    templist[1] += 1 # change right coord (row)
    tempcell = tuple(templist) # revert back to tuple
    init_cost = cell_cost(level, cell) # cost of current cell
    tempcost = calculate_cost(level, tempcell, 1, init_cost) #cost to get there
    if tempcost != None:
        temptuple = (tempcell, tempcost)
        final.append(temptuple) # add to final list

    # bottom
    templist = list(cell) # change to list to edit
    templist[1] += 1 # change right coord (row)
    tempcell = tuple(templist) # revert back to tuple
    init_cost = cell_cost(level, cell) # cost of current cell
    tempcost = calculate_cost(level, tempcell, 0, init_cost) #cost to get there
    if tempcost != None:
        temptuple = (tempcell, tempcost)
        final.append(temptuple) # add to final list

    # bottom-left
    templist = list(cell) # change to list to edit
    templist[0] -= 1 # change left coord (col)
    templist[1] += 1 # change right coord (row)
    tempcell = tuple(templist) # revert back to tuple
    init_cost = cell_cost(level, cell) # cost of current cell
    tempcost = calculate_cost(level, tempcell, 1, init_cost) #cost to get there
    if tempcost != None:
        temptuple = (tempcell, tempcost)
        final.append(temptuple) # add to final list

    finals = tuple(final)
    return finals

def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")

def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.
    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]

    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)

def cell_cost(level, cell):
    """ Checks the level for the cost of the cell passed in.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        The cost of the tile passed in.
        returns None if wall.
    """

    space = level.get("spaces")
    waypoint = level.get("waypoints")

    if cell in space.keys():
        cost = space.get(cell)
    elif cell in waypoint.keys():
        cost = 1
    else:
        return None

    return cost

def calculate_cost(level, cell, is_diagonal, init_cost):

    #Function will determine the type of node and use that to calculate the cost to move
    # Tuple of all space, wall, waypoint

    space = level.get("spaces")
    waypoint = level.get("waypoints")

    tempcost = -1 #start as none

    if cell in space.keys():
        tempcost = space.get(cell)
    elif cell in waypoint.keys():
        tempcost = 1
    elif cell in waypoint.keys():
        pass

    if tempcost != -1:
        if is_diagonal == 0: #adj is not diagonal:
            cost = (init_cost*0.5)+(tempcost*0.5)
            return cost
        if is_diagonal == 1: #adj is  diagonal:
            cost = (init_cost*sqrt(2)*0.5)+(tempcost*0.5*sqrt(2))
            return cost



if __name__ == '__main__':

    filename, src_waypoint, dst_waypoint = 'test_maze.txt', 'a','d'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    # cost_to_all_cells(filename, src_waypoint, 'my_maze.csv')
