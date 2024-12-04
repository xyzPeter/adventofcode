import re


def main():
    # data_file = r".\2024\03\data_example.txt"
    data_file = r".\2024\03\data.txt"

    print("\n")  # keep debug output on a new line

    with open(data_file, "r") as file:
        lines = file.readlines()
        # ans = part_1(lines)
        ans = part_2(lines)
        print(f"\nanswer = {ans}")


def find_mul_instances(text):
    # Define the regex pattern
    pattern = r"(mul\((\d{1,3}),(\d{1,3})\))"

    # Find all matches in the text
    matches = re.findall(pattern, text)

    # Return the list of matches
    return matches


def find_mul_instances_2(text):
    # Define the regex pattern
    pattern = r"(mul\((\d{1,3}),(\d{1,3})\))|(do\(\))|(don't\(\))"

    # Find all matches in the text
    matches = re.findall(pattern, text)

    # Return the list of matches
    return matches


def part_1(lines):
    result = 0  # total of multiplications

    for line in lines:
        print(line)
        mul_values = find_mul_instances(line)

        print(mul_values)
        for mul_value in mul_values:
            result += int(mul_value[1]) * int(mul_value[2])

    return result


def part_2(lines):
    log_file = r".\2024\03\logfile.txt"
    result = 0  # total of multiplications
    # Open the file in write mode (this will create the file if it doesn't exist)
    with open(log_file, "w") as file:
        file.write("mul_value,Do,Mul_1, Mul_2,Result")

    allow_multiply = True
    for line in lines:
        mul_values = find_mul_instances_2(line)

        print("    +++++++++++++++++++ do() +++++++++++++++++++")
        for mul_value in mul_values:
            print(f"mul_value = {mul_value}")
            if allow_multiply:
                if mul_value[0][:3] == "mul":
                    mul = int(mul_value[1]) * int(mul_value[2])
                    result += mul
                    with open(log_file, "a") as file:
                        file.write(
                            f"\n{mul_value},{allow_multiply},{mul_value[1]},{mul_value[2]},{result}"
                        )

                    print(
                        f"multiplied value = {mul};   result after multiplying = {result}"
                    )

                elif mul_value[4] == "don't()":
                    allow_multiply = False
                    print("    XXXXXXXXXXXXXXXXX don't() XXXXXXXXXXXXXXXXX")
                    with open(log_file, "a") as file:
                        file.write(
                            f"\n{mul_value},{allow_multiply},{mul_value[1]},{mul_value[2]},{result}"
                        )
            else:
                if mul_value[3] == "do()":
                    allow_multiply = True
                    print("    +++++++++++++++++++ do() +++++++++++++++++++")
                with open(log_file, "a") as file:
                    file.write(
                        f"\n{mul_value},{allow_multiply},{mul_value[1]},{mul_value[2]},{result}"
                    )
    return result


if __name__ == "__main__":
    main()
