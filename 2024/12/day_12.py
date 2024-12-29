from collections import deque


def main():
    # data_file = r".\2024\12\data_example.txt"
    data_file = r".\2024\12\data.txt"

    print("\n\n")  # keep debug output on a new line

    with open(data_file, "r") as file:
        lines = file.readlines()
        # Remove newline characters from each line
        lines = [line.rstrip("\n") for line in lines]
        ans = part_1(lines)
        print(f"\npart 1 answer = {ans}")
        ans = part_2b(lines)
        print(f"\npart 2 answer = {ans}") # 953738


adj4 = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def part_1(lines):
    result = 0  # fence price

    num_rows = len(lines)
    num_cols = len(lines[0])

    # Scan all cells.
    # If new crop (letter), then start a new region.
    # A region keeps track of its locations, an total side length.

    regions = []  # list of region dict, name, perimeter
    visited = set()  # set of locations, e.g. ((0, 0), (0, 1))

    for r in range(num_rows):
        for c in range(num_cols):
            if (r, c) in visited:
                continue
            q = deque([(r, c)])  # double ended queue
            visited.add(
                (r, c)
            )  # add to visited when added to the queue, to avoid reprocessing
            region = {"crop": lines[r][c], "locs": {(r, c)}, "perim": 0}
            regions.append(region)
            while q:
                (cr, cc) = q.pop()
                # Look in all four directions, increment num_edges if grid edge or different crop.
                # Add the new cell to the queue if it is the same crop.
                # Continue until there are no more crops in the queue.
                for nr, nc in [(cr + adjr, cc + adjc) for adjr, adjc in adj4]:
                    if nr not in range(num_rows) or nc not in range(num_cols):
                        region[
                            "perim"
                        ] += 1  # cell (nr, nc) at edge of grid, so add 1 to perimeter
                        continue  # outside of grid
                    if lines[nr][nc] == lines[cr][cc]:
                        if (nr, nc) not in visited:
                            q.append((nr, nc))  # same crop, so add to the queue.
                            visited.add((nr, nc))
                            region["locs"].add((nr, nc))
                        # this is not an edge, so do not increase perim.
                    else:
                        region[
                            "perim"
                        ] += 1  # different crop in adjacent cell, so this is an edge

    for region in regions:
        result += len(region["locs"]) * region["perim"]

    return result


def is_edge(lines, row, col, dir, num_rows, num_cols):
    """
    Returns true if this cell is at the edge of the grid, or if
    the adjacent cell is a different crop.
    """
    assert row >= 0 and row < num_rows, "row outside grid"
    assert col >= 0 and col < num_cols, "col outside grid"

    # check for edge of grid first
    if (dir == "T" and row <= 0) or (dir == "L" and col <= 0):
        return True
    if (dir == "B" and row >= num_rows - 1) or (dir == "R" and col >= num_cols - 1):
        return True

    crop = lines[row][col]
    # check for different crop
    if (dir == "T" and lines[row - 1][col] != crop) or (
        dir == "B" and lines[row + 1][col] != crop
    ):
        return True
    if (dir == "L" and lines[row][col - 1] != crop) or (
        dir == "R" and lines[row][col + 1] != crop
    ):
        return True

    return False  # adjacent cells have same crop, so return False


def edge_from_adj4(adjr, adjc):
    """
    Positive adjr -> B, Negative adjr -> T.
    Positive adjc -> R, Negative adjc -> L.
    """
    if adjr == 1:
        return "B"
    if adjr == -1:
        return "T"
    if adjc == 1:
        return "R"
    if adjc == -1:
        return "L"
    assert False, "Unexpected values for adjr and adjc in def edge_from_adj4()"


def find_sides(locs_edges):
    """
    Return the total length of sides, by only counting edges once
    if they are adjacent.
    locs_edges is a set containing tuples of (row, column, edge).
    For example, (3, 2, "T") means row 3, column 2, Top edge.
    """
    total_sides = 0

    while locs_edges:
        r, c, edge = locs_edges.pop()
        total_sides += 1
        if edge == "T" or edge == "B":
            # Look left and right for adjacent T/B edges and remove
            # Look left first.
            n_c = c - 1
            while (r, n_c, edge) in locs_edges:
                locs_edges.remove((r, n_c, edge))
                n_c -= 1

            n_c = c + 1
            while (r, n_c, edge) in locs_edges:
                locs_edges.remove((r, n_c, edge))
                n_c += 1

        if edge == "L" or edge == "R":
            # Look up and down for adjacent L/R edges and remove
            # Look up first.
            n_r = r - 1
            while (n_r, c, edge) in locs_edges:
                locs_edges.remove((n_r, c, edge))
                n_r -= 1

            n_r = r + 1
            while (n_r, c, edge) in locs_edges:
                locs_edges.remove((n_r, c, edge))
                n_r += 1

    return total_sides


def part_2b(lines):
    """
    Approach 2b:
    Find all edges and record these in each region - cell coord and
    edge (T, R, B, L).
    Within the region, identify sides from edges.
    """

    result = 0  # fence price

    num_rows = len(lines)
    num_cols = len(lines[0])

    # Scan all cells.
    # If new crop (letter), then start a new region.
    # A region keeps track of its locations, an total side length.

    regions = []  # list of region dict, crop, locations, loc_edges
    visited = set()  # set of locations, e.g. ((0, 0), (0, 1))

    for r in range(num_rows):
        for c in range(num_cols):
            if (r, c) in visited:
                continue
            q = deque([(r, c)])  # double ended queue
            visited.add(
                (r, c)
            )  # add to visited when added to the queue, to avoid reprocessing
            region = {"crop": lines[r][c], "locs": {(r, c)}, "perim": 0, "locs_edges": []}
            regions.append(region)
            while q:
                (cr, cc) = q.pop()
                # Look in all four directions, increment num_edges if grid edge or different crop.
                # Add the new cell to the queue if it is the same crop.
                # Continue until there are no more crops in the queue.
                for nr, nc, adjr, adjc in [(cr + adjr, cc + adjc, adjr, adjc) for adjr, adjc in adj4]:
                    if nr not in range(num_rows) or nc not in range(num_cols):
                        edge = edge_from_adj4(adjr, adjc)
                        region["locs_edges"].append((cr, cc, edge))
                        region[
                            "perim"
                        ] += 1  # cell (cr, cc) at edge of grid, so add 1 to perimeter
                        continue  # outside of grid
                    if lines[nr][nc] == lines[cr][cc]:
                        if (nr, nc) not in visited:
                            q.append((nr, nc))  # same crop, so add to the queue.
                            visited.add((nr, nc))
                            region["locs"].add((nr, nc))
                        # this is not an edge, so do not increase perim.
                    else:
                        edge = edge_from_adj4(adjr, adjc)
                        region["locs_edges"].append((cr, cc, edge))
                        region[
                            "perim"
                        ] += 1  # different crop in adjacent cell, so this is an edge

    for region in regions:
        total_sides = find_sides(region["locs_edges"])
        result += len(region["locs"]) * total_sides

    return result



def same_crop(lines, crop, r, c, num_rows, num_cols):
    """
    Return True if within grid and same crop in cell (r, c) as specified in parameter
    crop, else False.
    """
    if r >= 0 and c >= 0 and r < num_rows and c < num_cols:
        return crop == lines[r][c]
    return False


def add_no_duplicates(deq, item):
    if item not in deq:
        deq.append(item)


def part_2a(lines):
    """
    First attempt - did not work.
    """
    result = 0  # fence price

    num_rows = len(lines)
    num_cols = len(lines[0])

    # Scan all cells.
    # If new crop (letter), then start a new region.
    # A region keeps track of its locations, an total side length.

    regions = []  # list of region dict, name, sides
    visited = set()  # set of locations, e.g. ((0, 0), (0, 1))

    for r in range(num_rows):
        for c in range(num_cols):
            if (r, c) in visited:
                continue
            q = deque([(r, c)])  # double ended queue
            visited.add(
                (r, c)
            )  # add to visited when added to the queue, to avoid reprocessing
            region = {"crop": lines[r][c], "locs": {(r, c)}, "edges": {}, "sides": 0}
            regions.append(region)
            while q:
                print(f"crop: {lines[r][c]}; queue, before pop(): {q}")
                (cr, cc) = q.popleft()

                # Check for edge on each side.
                # If we find an edge, then check if this is a new side, by examining adjacent
                # perpendicular cells for the same edge, and only if that cell was already
                # in the current region's set of locations.
                region["locs"].add((cr, cc))
                crop = lines[cr][cc]
                visited.add((cr, cc))

                top_side = is_edge(lines, cr, cc, "T", num_rows, num_cols)
                right_side = is_edge(lines, cr, cc, "R", num_rows, num_cols)
                bottom_side = is_edge(lines, cr, cc, "B", num_rows, num_cols)
                left_side = is_edge(lines, cr, cc, "L", num_rows, num_cols)
                # xxxx_side variables need testing against adjacent cells, will be set to False
                # if there is an adjacent edge in the same region.

                # look up
                if (cr - 1, cc) in region["locs"]:
                    if left_side:
                        if is_edge(lines, cr - 1, cc, "L", num_rows, num_cols):
                            left_side = False
                    if right_side:
                        if is_edge(lines, cr - 1, cc, "R", num_rows, num_cols):
                            right_side = False
                elif same_crop(lines, crop, cr - 1, cc, num_rows, num_cols):
                    add_no_duplicates(q, (cr - 1, cc))

                # look down
                if (cr + 1, cc) in region["locs"]:
                    if left_side:
                        if is_edge(lines, cr + 1, cc, "L", num_rows, num_cols):
                            left_side = False
                    if right_side:
                        if is_edge(lines, cr + 1, cc, "R", num_rows, num_cols):
                            right_side = False
                elif same_crop(lines, crop, cr + 1, cc, num_rows, num_cols):
                    add_no_duplicates(q, (cr + 1, cc))

                # look left
                if (cr, cc - 1) in region["locs"]:
                    if top_side:
                        if is_edge(lines, cr, cc - 1, "T", num_rows, num_cols):
                            top_side = False
                    if bottom_side:
                        if is_edge(lines, cr, cc - 1, "B", num_rows, num_cols):
                            bottom_side = False
                elif same_crop(lines, crop, cr, cc - 1, num_rows, num_cols):
                    add_no_duplicates(q, (cr, cc - 1))

                # look right
                if (cr, cc + 1) in region["locs"]:
                    if top_side:
                        if is_edge(lines, cr, cc + 1, "T", num_rows, num_cols):
                            top_side = False
                    if bottom_side:
                        if is_edge(lines, cr, cc + 1, "B", num_rows, num_cols):
                            bottom_side = False
                elif same_crop(lines, crop, cr, cc + 1, num_rows, num_cols):
                    add_no_duplicates(q, (cr, cc + 1))

                if top_side:
                    region["sides"] += 1
                if right_side:
                    region["sides"] += 1
                if bottom_side:
                    region["sides"] += 1
                if left_side:
                    region["sides"] += 1

    for region in regions:
        print(
            f"Region: {region["crop"]}, Area: {len(region["locs"])}, Sides: {region["sides"]}, Price: {len(region["locs"]) * region["sides"]}"
        )
        result += len(region["locs"]) * region["sides"]

    return result


if __name__ == "__main__":
    main()
