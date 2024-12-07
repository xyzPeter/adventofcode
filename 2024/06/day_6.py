import functools


def main():
    # data_file = r".\2024\06\data_example.txt"
    data_file = r".\2024\06\data.txt"

    print("\n")  # keep debug output on a new line

    with open(data_file, "r") as file:
        lines = file.readlines()
        # Remove newline characters from each line
        lines = [line.rstrip("\n") for line in lines]
        # ans = part_1(lines)
        ans = part_2(lines)
        print(f"\nanswer = {ans}")


def starting_pos(lines):
    # Find starting location
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if lines[r][c] == "^":
                return (r, c)

def new_pos(r, c, dr, dc):
    return (r+dr, c+dc)

def rotate_right(dr, dc):
    if dr == -1 and dc == 0:
        return (0, 1)
    elif dr == 0 and dc == 1:
        return (1, 0)
    elif dr == 1 and dc == 0:
        return (0, -1)
    elif dr == 0 and dc == -1:
        return (-1, 0)
    assert(f"Unexpected dr/dc pair: {dr}/{dc}")

def part_1(lines):
    result = 0  # num squares that guard visits

    num_rows = len(lines)
    num_cols = len(lines[0])

    r, c = starting_pos(lines)
    print(r, c)
    dr = -1
    dc = 0
    visited = set()
    visited.add((r, c))
    print(visited)

    while True:
        new_r, new_c = new_pos(r, c, dr, dc)
        if new_r >= num_rows or new_r < 0 or new_c >= num_cols or new_c < 0:
            break # Guard has exited the grid
        while lines[new_r][new_c] == "#":
            dr, dc = rotate_right(dr, dc)
            new_r, new_c = new_pos(r, c, dr, dc)

        r, c = new_r, new_c
        visited.add((r, c))

    print(visited)

    # 231 too low
    # 5516 was correct
    result = len(visited)

    return result


def part_2(lines):
    result = 0  # num squares that guard visits

    num_rows = len(lines)
    num_cols = len(lines[0])

    sr, sc = starting_pos(lines)

    grid = []
    # convert lines to list of lists, to allow changing individual cells
    for line in lines:
        line = list(line)
        grid.append(line)
    
    print(sr, sc)

    for cr in range(num_rows):
        for cc in range(num_cols):
            orig_cell_value = grid[cr][cc]
            if orig_cell_value == ".":
                # not the starting point or an existing obstacle
                grid[cr][cc] = "#"

                # reset r and c back to sr and sc (start r and start c)
                r = sr
                c = sc
                dr = -1
                dc = 0
                # reset visited set back to empty
                visited = set()
                visited.add((sr, sc, dr, dc)) # include direction
                # Run guard trace routine:
                while True:
                    new_r, new_c = new_pos(r, c, dr, dc)
                    if new_r >= num_rows or new_r < 0 or new_c >= num_cols or new_c < 0:
                        break # Guard has exited the grid
                    while grid[new_r][new_c] == "#":
                        dr, dc = rotate_right(dr, dc)
                        new_r, new_c = new_pos(r, c, dr, dc)

                    r, c = new_r, new_c
                    if (r, c, dr, dc) in visited:
                        # created a loop
                        result += 1
                        grid[cr][cc] = orig_cell_value
                        break

                    visited.add((r, c, dr, dc)) # include direction

                grid[cr][cc] = orig_cell_value


    print(visited)

    # 16077 too high
    # 2008 correct
    return result

if __name__ == "__main__":
    main()
