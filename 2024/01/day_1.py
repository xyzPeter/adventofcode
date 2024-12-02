def main():
    # data_file = r".\2024\01\data_example.txt"
    data_file = r".\2024\01\data.txt"

    with open(data_file, "r") as file:
        lines = file.readlines()
        # ans = part_1(lines)
        ans = part_2(lines)
        print(f"answer = {ans}")

def part_1(lines):
    result = 0
    list_1 = []
    list_2 = []

    for line in lines:
        values = line.split()
        list_1.append(int(values[0]))
        list_2.append(int(values[1]))

    list_1.sort()
    list_2.sort()

    diffs = [abs(a-b) for a, b in zip(list_1, list_2)]
    for diff in diffs:
        result += diff

    return result

def part_2(lines):
    result = 0
    list_1 = []
    list_2 = []

    for line in lines:
        values = line.split()
        list_1.append(int(values[0]))
        list_2.append(int(values[1]))

    for value in list_1:
        occurrences = list_2.count(value)
        result += occurrences * value

    return result

if __name__ == "__main__":
    main()
