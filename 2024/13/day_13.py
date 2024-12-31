import numpy as np
import re

"""
Input example:
    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=8400, Y=5400

Solve simultaneous equations:
    94.A + 22.B = 8400
    34.A + 67.B = 5400
"""


def main():
    # data_file = r".\2024\13\data_example.txt"
    data_file = r".\2024\13\data.txt"

    print("\n\n")  # keep debug output on a new line

    with open(data_file, "r") as file:
        lines = file.readlines()
        # Remove newline characters from each line
        lines = [
            line.rstrip("\n") for line in lines if line.strip()
        ]  # strip blank lines
        ans = part_1(lines)
        print(f"\npart_1 answer = {ans}")
        ans = part_2(lines)
        print(f"\npart_2 answer = {ans}")


def round_and_check(value, tolerance=1e-3):
    """
    Rounds the given value to the nearest integer and checks if the
    original value is close to the rounded value within a tolerance.

    Parameters:
    - value (float): The value to round and check.
    - tolerance (float): The tolerance within which the values are considered close.

    Returns:
    - tuple: (rounded_value, is_close)
        - rounded_value (int): The rounded integer value.
        - is_close (bool): Whether the original and rounded values are close.
    """
    rounded_value = round(value)
    is_close = abs(value - rounded_value) <= tolerance
    return rounded_value, is_close


def solve_equations_int(coefficients, constants):
    """
    Solve a system of linear equations Ax = B.

    Parameters:
    - coefficients (list of list of float): Coefficient matrix A.
    - constants (list of float): Constant vector B.

    Returns:
    - solution (list of float): Solution vector x.
    """
    # Convert the inputs to numpy arrays
    A = np.array(coefficients)
    B = np.array(constants)

    # Solve the linear equations
    solution = np.linalg.solve(A, B)
    result = solution.tolist()

    print(f"values: {result}")
    for i, value in enumerate(result):
        rounded, close = round_and_check(value)
        if close:
            result[i] = rounded
        else:
            raise ValueError(f"Not a valid integer solution: {value} / {rounded}")

    return result


def parse_claw_machine_data(lines):
    """
    Reads data from a list of lines and extracts numeric values for each claw 
    machine configuration.

    Parameters:
    - lines from the input file

    Returns:
    - list of dict: A list of dictionaries, each containing the numeric values
                    for 'button_a', 'button_b', and 'prize' of each claw machine.
    """
    machines = []

    for i in range(0, len(lines), 3):  # Process blocks of 3 lines
        button_a_line = lines[i]
        button_b_line = lines[i + 1]
        prize_line = lines[i + 2]

        # Extract numbers for Button A
        a_match = re.search(r"X\+(\d+), Y\+(\d+)", button_a_line)
        a_x, a_y = map(int, a_match.groups())

        # Extract numbers for Button B
        b_match = re.search(r"X\+(\d+), Y\+(\d+)", button_b_line)
        b_x, b_y = map(int, b_match.groups())

        # Extract numbers for Prize
        prize_match = re.search(r"X=(\d+), Y=(\d+)", prize_line)
        prize_x, prize_y = map(int, prize_match.groups())

        # Store the parsed values in a dictionary
        machine = {
            "button_a": (a_x, a_y),
            "button_b": (b_x, b_y),
            "prize": (prize_x, prize_y),
        }
        machines.append(machine)

    # print(f"Machine coefficients: \n{machines}")
    return machines


def part_1(lines):
    # Parse the data file contents:
    machines = parse_claw_machine_data(lines)

    num_coins = 0

    for machine in machines:
        a_x, a_y = machine["button_a"]
        b_x, b_y = machine["button_b"]
        prize_x, prize_y = machine["prize"]
        coefficients = [[a_x, b_x], [a_y, b_y]]
        constants = [prize_x, prize_y]
        try:
            solution = solve_equations_int(coefficients, constants)
            num_coins += 3 * solution[0] + solution[1]
            # print(solution)

        except Exception as e:
            # Probably no solution
            print(f"Error: {e}")
    return num_coins


def part_2(lines):
    # Parse the data file contents:
    machines = parse_claw_machine_data(lines)

    num_coins = 0

    for machine in machines:
        a_x, a_y = machine["button_a"]
        b_x, b_y = machine["button_b"]
        prize_x, prize_y = machine["prize"]
        coefficients = [[a_x, b_x], [a_y, b_y]]
        constants = [10000000000000 + prize_x, 10000000000000 + prize_y]
        try:
            solution = solve_equations_int(coefficients, constants)
            num_coins += 3 * solution[0] + solution[1]
            print(solution)

        except Exception as e:
            # Probably no solution
            print(f"Error: {e}")

    return num_coins


if __name__ == "__main__":
    main()
