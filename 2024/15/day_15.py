from collections import deque


def main():
    # data_file = r".\2024\15\data_example.txt"
    data_file = r".\2024\15\data.txt"

    print("\n\n")  # keep debug output on a new line

    with open(data_file, "r") as file:
        # Remove newline characters from each line
        lines = [line.rstrip("\n") for line in file.readlines()]
        ans = part_1(lines)
        print(f"\npart_1 answer = {ans}")
        ans = part_2(lines)
        print(f"\npart_2 answer = {ans}")


def part_1(lines):
    """
    Track position of all boxes as the robot moves.
    GPS value for each box is 100.C + R.
    Sum the GPS values and return.
    """
    grid = []
    movements = []
    robot_pos = ()
    is_grid = True
    for line in lines:
        if not line:
            # blank line - switch to movements
            is_grid = False
            continue
        if is_grid:
            grid_line = []
            for cell in line:
                grid_line += cell
            grid.append(grid_line)
        else:
            for move in line:
                movements += move

    [print("".join(row)) for row in grid]
    # print(movements)
    print()

    found = False
    for y, row in enumerate(grid):
        if found:
            break
        for x, cell in enumerate(row):
            if cell == "@":
                robot_pos = (x, y)
                found = True
                break

    for move in movements:
        robot_pos = move_robot(robot_pos, move, grid)

    [print("".join(row)) for row in grid]

    total_gps = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if grid[x][y] == "O":
                total_gps += 100 * x + y

    return total_gps

def print_grid(grid):
    [print("".join(row)) for row in grid]


def part_2(lines):
    """
    Expand the walls, boxes and empty spaces to double width.
    Track position of all boxes as the robot moves.
    GPS value for each box is 100.C + R.
    Sum the GPS values and return.
    """
    grid = []
    movements = []
    robot_pos = ()
    is_grid = True
    for line in lines:
        if not line:
            # blank line - switch to movements
            is_grid = False
            continue
        if is_grid:
            grid_line = []
            for cell in line:
                if cell == "#":
                    grid_line += "#"
                    grid_line += "#"
                elif cell == "O":
                    grid_line += "["
                    grid_line += "]"
                elif cell == ".":
                    grid_line += "."
                    grid_line += "."
                elif cell == "@":
                    grid_line += "@"
                    grid_line += "."
            grid.append(grid_line)
        else:
            for move in line:
                movements += move

    print_grid(grid)
    # print(movements)
    print()

    found = False
    for r, row in enumerate(grid):
        if found:
            break
        for c, cell in enumerate(row):
            if cell == "@":
                robot_pos = (r, c)
                found = True
                break

    for move in movements:
        robot_pos = move_robot_2(robot_pos, move, grid)
        # print(f"\nMove direction: {move}")
        # print_grid(grid)

    total_gps = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if grid[r][c] == "[":
                total_gps += 100 * r + c

    return total_gps


def move_vector(move):
    """
    Note that vectors are row, column (r, c), not x, y.
    """
    vector = {
        ">": (0, 1),
        "v": (1, 0),
        "<": (0, -1),
        "^": (-1, 0),
    }
    return vector.get(move, (0, 0))


def new_pos(current_pos, vector):
    return (current_pos[0] + vector[0], current_pos[1] + vector[1])


def move_robot(robot_pos, move, grid):
    """
    Look in direction of move. If there is an empty cell (.), switch
    the robot and empty cell. If there is a wall, do nothing. If there
    is a box (O), keep looking in the direction of move to find either
    an empty cell or wall.
    """
    vector = move_vector(move)
    test_pos = new_pos(robot_pos, vector)
    if grid[test_pos[0]][test_pos[1]] == ".":
        # move robot to the empty space
        grid[test_pos[0]][test_pos[1]] = "@"  # robot
        grid[robot_pos[0]][robot_pos[1]] = "."  # empty square
        return test_pos
    while grid[test_pos[0]][test_pos[1]] == "O":
        test_pos = new_pos(test_pos, vector)  # keep moving while boxes present.
    if grid[test_pos[0]][test_pos[1]] == ".":
        # fill this discovered empty space with a box, move robot one square,
        # replace robot original pos with empty space.
        grid[test_pos[0]][test_pos[1]] = "O"  # box
        grid[robot_pos[0]][robot_pos[1]] = "."  # empty square
        test_pos = new_pos(robot_pos, vector)
        grid[test_pos[0]][test_pos[1]] = "@"  # robot
        return test_pos
    return robot_pos  # did not move - no empty spaces


def move_robot_horiz(robot_pos, vector, grid):
    test_pos = new_pos(robot_pos, vector)
    if grid[test_pos[0]][test_pos[1]] == ".":
        # move robot to the empty space
        grid[test_pos[0]][test_pos[1]] = "@"  # robot
        grid[robot_pos[0]][robot_pos[1]] = "."  # empty square
        return test_pos
    while grid[test_pos[0]][test_pos[1]] in ("[", "]"):
        test_pos = new_pos(test_pos, vector)  # keep moving while boxes present.
    if grid[test_pos[0]][test_pos[1]] == ".":
        new_robot_pos = new_pos(robot_pos, vector)
        opp_vector = tuple(-value for value in vector)
        r = robot_pos[0] # row index
        # Loop from first empty square, back to the cell adjacent to the robot
        # shuffling the cell contents towards the empty square.
        for c in range(test_pos[1], robot_pos[1] + vector[1], opp_vector[1]):
            grid[r][c] = grid[r][c + opp_vector[1]]
        grid[new_robot_pos[0]][new_robot_pos[1]] = "@"
        grid[robot_pos[0]][robot_pos[1]] = "."
        return new_robot_pos
    
    return robot_pos  # no movement possible


def move_robot_vert(robot_pos, vector, grid):
    """
    Note that grid is (row, col), so up is vector (-1, 0) and down
    is (1, 0).
    This function is called only by part_2, where the robot pushes
    boxes that span 2 squares: [].
    First, we look for an empty square . and if there is an empty
    square, the robot moves to that square and the routine returns.
    If a box is found, then we begin to keep track of the expanding 
    set of boxes, some examples:
    Moves down:  Moves up:  Does not move down:
        @        ......        @
        []       [][][]        []
        [][]      [][]        [].
        .[].       []          []
         ..         @       #########
    """
    
    # move robot to the empty space - no boxes involved
    test_pos = new_pos(robot_pos, vector)
    new_robot_pos = test_pos
    if grid[test_pos[0]][test_pos[1]] == ".":
        grid[test_pos[0]][test_pos[1]] = "@"  # robot
        grid[robot_pos[0]][robot_pos[1]] = "."  # empty square
        return test_pos
    
    # working on boxes - add all moving cells to list moving_cells.
    moving_cells = list()
    moving_cells.append(robot_pos)
    if grid[test_pos[0]][test_pos[1]] == "#":
        # we've hit the edge and cannot move.
        return robot_pos
    
    if grid[test_pos[0]][test_pos[1]] in ("[", "]"):
        moving_cells.append(test_pos)
        # expand moving_cells to pick up other half of any boxes
        if grid[moving_cells[-1][0]][moving_cells[-1][1]] == "]":
            moving_cells.append((moving_cells[-1][0], moving_cells[-1][1] - 1))
        elif grid[moving_cells[-1][0]][moving_cells[-1][1]] == "[":
            moving_cells.append((moving_cells[-1][0], moving_cells[-1][1] + 1))
    
    # So far, we've only tested moving the first (robot) cell.
    # Keep track of which moving_cells have been tested to move - save
    # the index of the next moving_cell to test.
    next_moving_cell = 1

    while next_moving_cell < len(moving_cells):
        # return when we hit a wall, or all empty squares.
        test_pos = new_pos(moving_cells[next_moving_cell], vector)
        if grid[test_pos[0]][test_pos[1]] == "#":
            # at edge - cannot move any cells
            return robot_pos
        if grid[test_pos[0]][test_pos[1]] == ".":
            next_moving_cell += 1
        elif test_pos in moving_cells:
            next_moving_cell += 1 # no need to add a cell twice
        elif grid[test_pos[0]][test_pos[1]] in ("[", "]"):
            moving_cells.append(test_pos)
            # expand moving_cells to pick up other half of any boxes
            if grid[test_pos[0]][test_pos[1]] == "]":
                moving_cells.append((test_pos[0], test_pos[1] - 1))
            if grid[test_pos[0]][test_pos[1]] == "[":
                moving_cells.append((test_pos[0], test_pos[1] + 1))
            next_moving_cell += 1
    
    # we have the list of cells to move - now we need to move them.
    # We need to keep track of the replaced cells, to ensure that we
    # don't later replace them with an empty space - use list replaced.
    replaced = []
    while moving_cells:
        cell = moving_cells.pop()
        move_to = new_pos(cell, vector)
        grid[move_to[0]][move_to[1]] = grid[cell[0]][cell[1]]
        if cell not in replaced:
            grid[cell[0]][cell[1]] = "."
        replaced.append(move_to)

    return new_robot_pos


def move_robot_2(robot_pos, move, grid):
    """
    Look in direction of move. If there is an empty cell (.), switch
    the robot and empty cell. If there is a wall, do nothing. If there
    is a box (O), keep looking in the direction of move to find either
    an empty cell or wall.
    """
    vector = move_vector(move)
    if vector[1] == 0:
        return move_robot_vert(robot_pos, vector, grid)
    else:
        return move_robot_horiz(robot_pos, vector, grid)


if __name__ == "__main__":
    main()
