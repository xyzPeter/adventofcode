from itertools import product

def main():
    # data_file = r".\2024\07\data_example.txt"
    data_file = r".\2024\07\data.txt"

    print("\n")  # keep debug output on a new line

    with open(data_file, "r") as file:
        lines = file.readlines()
        # Remove newline characters from each line
        lines = [line.rstrip("\n") for line in lines]
        # ans = part_1(lines)
        ans = part_2(lines)
        print(f"\nanswer = {ans}")


def is_valid_equation(equation_in):
    nums = equation_in[1]
    if len(nums) < 2:
        raise ValueError("At least two numbers are required.")

    operators = ['+', '*']
    
    # Generate all combinations of operators for the (n-1) gaps between numbers
    # print(f"ops: {product(operators, repeat=len(nums))} ||| {nums}")
    for ops in product(operators, repeat=len(nums) - 1):
        result = nums[0]
        for i, op in enumerate(ops):
            result = eval(str(result) + op + str(nums[i+1]))

        if result == equation_in[0]:
            return True
   
    return False

def is_valid_equation_2(equation_in):
    nums = equation_in[1]
    if len(nums) < 2:
        raise ValueError("At least two numbers are required.")

    operators = ['+', '*', "||"]
    
    # Generate all combinations of operators for the (n-1) gaps between numbers
    # print(f"ops: {product(operators, repeat=len(nums))} ||| {nums}")
    for ops in product(operators, repeat=len(nums) - 1):
        result = nums[0]
        for i, op in enumerate(ops):
            if op == "||":
                result = eval(str(result) + str(nums[i+1]))
            else:
                result = eval(str(result) + op + str(nums[i+1]))

        if result == equation_in[0]:
            return True
   
    return False



def part_1(lines):
    result = 0  # sum of correct equation results

    equations = list()

    for line in lines:
        vals = line.split(":")
        operands = [int(x) for x in vals[1].strip().split(" ")]
        equations.append([int(vals[0]), operands])
    # print(equations)

    for equation in equations:
        if is_valid_equation(equation):
            result += equation[0]


    return result


def part_2(lines):
    result = 0  # sum of correct equation results

    equations = list()

    for line in lines:
        vals = line.split(":")
        operands = [int(x) for x in vals[1].strip().split(" ")]
        equations.append([int(vals[0]), operands])
    # print(equations)

    for equation in equations:
        if is_valid_equation_2(equation):
            result += equation[0]


    return result

if __name__ == "__main__":
    main()
