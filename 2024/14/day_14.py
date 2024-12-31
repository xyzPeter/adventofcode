import re

room_width = 101
room_height = 103
# room_width = 11
# room_height = 7

def main():
    # data_file = r".\2024\14\data_example.txt"
    data_file = r".\2024\14\data.txt"

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
    Find the position and speed of each robot.
    Find the position after 100 seconds, and identify the
    quadrant at the end of the 100 seconds and keep track
    of the quantity per quadrant.
    Result is the product of these four quantities.
    """
    q_1 = q_2 = q_3 = q_4 = 0
    for line in lines:
        # Regex to match the pattern
        pattern = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"

        # Perform regex search
        match = re.search(pattern, line)
        if match:
            x, y = (int(match.group(1)), int(match.group(2)))
            v_x, v_y = (int(match.group(3)), int(match.group(4)))
            n_x = (x + 100 * v_x) % room_width
            n_y = (y + 100 * v_y) % room_height
            print(f"new x, y: {(n_x, n_y)}")
            if n_x < room_width//2 and n_y < room_height//2:
                q_1 += 1
            elif n_x > room_width//2 and n_y < room_height//2:
                q_2 += 1
            elif n_x < room_width//2 and n_y > room_height//2:
                q_3 += 1
            elif n_x > room_width//2 and n_y > room_height//2:
                q_4 += 1
        else:
            print("No match found.")

    return q_1 * q_2 * q_3 * q_4
    # 218965032


def part_2(lines):
    """
    Looking for a christmas tree image.
    Find the position and speed of each robot.
    Find the position after each second multiple adjacent robots - at least 10.
    Return the second count when this occurs.
    """
    result = -1
    robots = []

    for line in lines:
        # Regex to match the pattern
        pattern = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"

        # Perform regex search
        match = re.search(pattern, line)
        if match:
            x, y = (int(match.group(1)), int(match.group(2)))
            v_x, v_y = (int(match.group(3)), int(match.group(4)))
            robots.append((x, y, v_x, v_y))

    print(f"Num robots: {len(robots)}")

    for steps in range(1, room_width * room_height):
        robot_positions = []
        for robot in robots:
            x = (robot[0] + steps * robot[2]) % room_width
            y = (robot[1] + steps * robot[3]) % room_height
            robot_positions.append((x, y))
        if find_tree(robot_positions):
            result = steps
            print_tree(robot_positions)
            break

    return result


def print_tree(robot_positions):

    visual = ""
    for y in range(room_height):
        visual += "\n|"
        for x in range(room_width):
            if (x, y) in robot_positions:
                visual += "X"
            else:
                visual += " "
        visual += "|"
    with open(r".\2024\14\tree.txt", "w") as file:
        file.write(visual)


def find_tree(robot_positions):
    """
    Scan for 10 vertically adjacent robots.
    Return True if 10 adjacent robots found.
    """

    for y in range(room_height-10):
        for x in range(room_width):
            for i in range(10):
                if (x, y+i) not in robot_positions:
                    # not a tree - break to next cell
                    break
                if i == 9:
                    return True

    return False

if __name__ == "__main__":
    main()
