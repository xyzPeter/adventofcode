import numpy as np
from functools import cache

def main():
    print("Hello from adventofcode!")

    # Example usage
    coefficients = [
        [1, 1],
        [1, 1]
    ]
    constants = [8400, 5400]

    solution = solve_equations_int(coefficients, constants)
    print("Solution:", solution)


    rocks = "125 17"
    i_rocks = [int(x) for x in rocks.split()]
    
    result = 0
    for rock in i_rocks:
        result += solve(rock, 25)

    print(f"Num rocks: {result}")


def round_and_check(value, tolerance=1e-9):
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
    print(f"type(value) = {type(value)}")
    rounded_value = round(value)
    print(f"type(rounded_value) = {type(rounded_value)}")
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
    try:
        # Convert the inputs to numpy arrays
        A = np.array(coefficients)
        B = np.array(constants)
        
        # Solve the linear equations
        solution = np.linalg.solve(A, B)
        result = solution.tolist()

        for i, value in enumerate(result):
            rounded, close = round_and_check(value)
            if close:
                result[i] = rounded
            else:
                raise ValueError(f"Not a valid integer solution: {value} / {rounded}")
        
        return result
    except np.linalg.LinAlgError as e:
        return f"Error: {e}"


@cache
def solve(rock, steps):
    
    if steps <= 0:
        return 1 # just one rock

    steps -= 1
    
    if rock == 0:
        return solve(1, steps)

    s_rock = str(rock)
    if len(s_rock) % 2 == 0:
        return solve(int(s_rock[:len(s_rock)//2]), steps) + solve(int(s_rock[len(s_rock)//2:]), steps)

    return solve(rock*2024, steps)


if __name__ == "__main__":
    main()
