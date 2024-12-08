from collections import defaultdict
from itertools import combinations


def main():
    # data_file = r".\2024\08\data_example.txt"
    data_file = r".\2024\08\data.txt"

    print("\n")  # keep debug output on a new line

    with open(data_file, "r") as file:
        lines = file.readlines()
        # Remove newline characters from each line
        lines = [line.rstrip("\n") for line in lines]
        # ans = part_1(lines)
        ans = part_2(lines)
        print(f"\nanswer = {ans}")


def in_grid(new_pos, num_rows, num_cols):
    return (
        new_pos[0] >= 0
        and new_pos[0] < num_rows
        and new_pos[1] >= 0
        and new_pos[1] < num_cols
    )


def part_1(lines):
    result = 0  # number of antinodes

    num_rows = len(lines)
    num_cols = len(lines[0])

    anti_nodes = [["." for r in range(num_rows)] for c in range(num_cols)]
    print(anti_nodes)

    # create dictionary, with values being a list of
    # tuples, being the coordinates of the antennas.
    # {"a": [(1, 2), (3, 5)], "b": [(3, 7), (8, 12)]}

    antennas = defaultdict(list)

    for r, line in enumerate(lines):
        for c, val in enumerate(line):
            if val != ".":
                antennas[val].append((r, c))

    print(antennas)

    for antenna in antennas.values():
        print(f"antenna: {antenna}")
        antenna_combis = combinations(antenna, 2)
        for antenna_combi in antenna_combis:
            dx, dy = (
                antenna_combi[0][0] - antenna_combi[1][0],
                antenna_combi[0][1] - antenna_combi[1][1],
            )
            new_pos = (antenna_combi[0][0] + dx, antenna_combi[0][1] + dy)
            if in_grid(new_pos, num_rows, num_cols):
                anti_nodes[new_pos[0]][new_pos[1]] = "#"
            new_pos = (antenna_combi[1][0] - dx, antenna_combi[1][1] - dy)
            if in_grid(new_pos, num_rows, num_cols):
                anti_nodes[new_pos[0]][new_pos[1]] = "#"

    for r in range(num_rows):
        s = ""
        for c in range(num_cols):
            s += anti_nodes[r][c]
            if anti_nodes[r][c] == "#":
                result += 1
        print(s)

    print("\n\n")

    return result


def part_2(lines):
    result = 0  # number of antinodes

    num_rows = len(lines)
    num_cols = len(lines[0])

    anti_nodes = [["." for r in range(num_rows)] for c in range(num_cols)]
    print(anti_nodes)

    # create dictionary, with values being a list of
    # tuples, being the coordinates of the antennas.
    # {"a": [(1, 2), (3, 5)], "b": [(3, 7), (8, 12)]}
    antennas = defaultdict(list)
    for r, line in enumerate(lines):
        for c, val in enumerate(line):
            if val != ".":
                antennas[val].append((r, c))

    for antenna in antennas.values():
        print(f"antenna: {antenna}")
        antenna_combis = combinations(antenna, 2)
        for antenna_combi in antenna_combis:
            dx, dy = (
                antenna_combi[0][0] - antenna_combi[1][0],
                antenna_combi[0][1] - antenna_combi[1][1],
            )
            # Need to test multiples of dx, dy until the new_pos is off the grid
            multiple = 0
            while True:
                new_pos = (antenna_combi[0][0] + multiple*dx, antenna_combi[0][1] + multiple*dy)
                if not in_grid(new_pos, num_rows, num_cols):
                    break
                anti_nodes[new_pos[0]][new_pos[1]] = "#"
                multiple += 1

            multiple = 0
            while True:
                new_pos = (antenna_combi[1][0] - multiple*dx, antenna_combi[1][1] - multiple*dy)
                if not in_grid(new_pos, num_rows, num_cols):
                    break
                anti_nodes[new_pos[0]][new_pos[1]] = "#"
                multiple += 1

    for r in range(num_rows):
        s = ""
        for c in range(num_cols):
            s += anti_nodes[r][c]
            if anti_nodes[r][c] == "#":
                result += 1
        print(s)

    print("\n\n")

    # 1119 - too low (of 2500 cells)
    # 1233 - include position of antennas, by setting initial multiplier to 0
    return result


if __name__ == "__main__":
    main()
