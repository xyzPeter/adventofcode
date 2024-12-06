import re


def main():
    # data_file = r".\2024\04\data_example.txt"
    data_file = r".\2024\04\data.txt"

    print("\n")  # keep debug output on a new line

    with open(data_file, "r") as file:
        lines = file.readlines()
        # ans = part_1(lines)
        ans = part_2(lines)
        print(f"\nanswer = {ans}")


def part_1(lines):
    result = 0  # number of "XMAS"

    num_rows = len(lines)
    num_cols = len(lines[0].strip())

    # Search left to right AND right to left
    for line in lines:
        for col_idx, c in enumerate(line):
            if col_idx > num_cols - 4:
                break

            if (
                line[col_idx : col_idx + 4] == "XMAS"
                or line[col_idx : col_idx + 4] == "SAMX"
            ):
                result += 1

    print(f"Left/Right: {result}")

    # Search top to bottom AND bottom to top
    for row_idx, line in enumerate(lines):
        if row_idx > num_rows - 4:
            break  # no vertical XMAS can fit in less that 4 rows

        for col_idx, c in enumerate(line):
            if (
                c == "X"
                and lines[row_idx + 1][col_idx] == "M"
                and lines[row_idx + 2][col_idx] == "A"
                and lines[row_idx + 3][col_idx] == "S"
            ) or (
                c == "S"
                and lines[row_idx + 1][col_idx] == "A"
                and lines[row_idx + 2][col_idx] == "M"
                and lines[row_idx + 3][col_idx] == "X"
            ):
                result += 1

    print(f"Up/Down: {result}")

    # diagonal up to right
    for row_idx in range(3, num_rows):  # start from fourth row
        for col_idx in range(0, num_cols - 3):  # finish at fourth to last column
            if (
                lines[row_idx][col_idx] == "X"
                and lines[row_idx - 2][col_idx + 2] == "A"
                and lines[row_idx - 3][col_idx + 3] == "S"
                and lines[row_idx - 1][col_idx + 1] == "M"
            ) or (
                lines[row_idx][col_idx] == "S"
                and lines[row_idx - 1][col_idx + 1] == "A"
                and lines[row_idx - 2][col_idx + 2] == "M"
                and lines[row_idx - 3][col_idx + 3] == "X"
            ):
                print(f"Up/right, row: {row_idx}, col: {col_idx}")
                result += 1

    print(f"Up to right: {result}")

    # diagonal down to right
    for row_idx in range(0, num_rows - 3):  # start from fourth row
        for col_idx in range(0, num_cols - 3):  # finish at fourth to last column
            if (
                lines[row_idx][col_idx] == "X"
                and lines[row_idx + 1][col_idx + 1] == "M"
                and lines[row_idx + 2][col_idx + 2] == "A"
                and lines[row_idx + 3][col_idx + 3] == "S"
            ) or (
                lines[row_idx][col_idx] == "S"
                and lines[row_idx + 1][col_idx + 1] == "A"
                and lines[row_idx + 2][col_idx + 2] == "M"
                and lines[row_idx + 3][col_idx + 3] == "X"
            ):
                print(f"Down/Right, row: {row_idx}, col: {col_idx}")
                result += 1

    return result


def part_2(lines):
    result = 0  # number of X-MAS

    num_rows = len(lines)
    num_cols = len(lines[0].strip())

    # Start from second row and second column, check through to
    # seond to last row and column. Look for an A, with M/S up 
    # left and down right, and M/S up right and down left.
    for row_idx in range(1, num_rows-1):
        for col_idx in range(1, num_cols - 1):
            if lines[row_idx][col_idx] == "A":
                # found potential center of X-MAS
                if ((lines[row_idx-1][col_idx-1] == "M" and lines[row_idx+1][col_idx+1] == "S") 
                    or
                    (lines[row_idx-1][col_idx-1] == "S" and lines[row_idx+1][col_idx+1] == "M")):
                    # found one diagonal - now check second diagonal
                    #  
                    if ((lines[row_idx+1][col_idx-1] == "M" and lines[row_idx-1][col_idx+1] == "S") 
                        or
                        (lines[row_idx+1][col_idx-1] == "S" and lines[row_idx-1][col_idx+1] == "M")):
                        # found both diagonals - hence an X-MAS
                        result += 1
        
    return result

if __name__ == "__main__":
    main()
