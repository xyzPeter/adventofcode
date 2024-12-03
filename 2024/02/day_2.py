def main():
    # data_file = r".\2024\02\data_example.txt"
    data_file = r".\2024\02\data.txt"

    print("\n") # keep debug output on a new line

    with open(data_file, "r") as file:
        lines = file.readlines()
        # ans = part_1(lines)
        ans = part_2(lines)
        print(f"\nanswer = {ans}")

def part_1(lines):
    result = 0 # number of safe reports

    for line in lines:
        print(line)
        s_values = line.split()
        values = [int(x) for x in s_values]

        is_safe = (values[0] != values[1] and abs(values[1] - values[0]) < 4)
        if not is_safe:
            continue # not safe - continue to next line

        is_increasing = values[1] > values[0]
        prev_value = values[1]

        for value in values[2:]:
            is_safe = (value != prev_value and abs(value - prev_value) < 4)
            print(f"is_safe 1: {is_safe}")
            if not is_safe:
                break # not safe - break out of value, to next line
            is_safe = (is_increasing and value > prev_value) or (not is_increasing and value < prev_value)
            print(f"is_safe 2: {is_safe}")
            if not is_safe:
                break # not safe - break out of value, to next line
            prev_value = value
        
        print(f"is_safe 3: {is_safe}")
        if is_safe:
            result += 1

    return result

def part_2(lines):
    ''' 
        Check if the entire line is safe. If not, iteratively remove one value from the list
        and recheck. If any sub-list is safe, add to the safe report count
    '''

    result = 0 # number of safe reports

    for line in lines:
        is_safe = False # just for debugging
        s_values = line.split()
        values = [int(x) for x in s_values]

        print (line)

        if check_safe(values):
            result += 1
            print(f"safe on first check, result = {result}")
            is_safe = True
            continue

        # Not safe with whole list - try each partial list
        for i in range(len(values)):
            partial_values = values.copy()
            del partial_values[i]
            if check_safe(partial_values):
                is_safe = True
                result += 1
                print(f"safe with this partial list: {partial_values}")
                print(f"result: {result}")
                break
        
        if not is_safe:
            print(f"Report is unsafe. Partial line: {partial_values}")
            print(f"result: {result}")

    return result

def check_safe(values):
    is_safe = (values[0] != values[1] and abs(values[1] - values[0]) < 4)
    if not is_safe:
        return False

    is_increasing = values[1] > values[0]
    prev_value = values[1]

    for value in values[2:]:
        is_safe = (value != prev_value and abs(value - prev_value) < 4)
        # print(f"is_safe 1: {is_safe}")
        if not is_safe:
            break # not safe - break out of value, to next line
        is_safe = (is_increasing and value > prev_value) or (not is_increasing and value < prev_value)
        # print(f"is_safe 2: {is_safe}")
        if not is_safe:
            break # not safe - break out of value, to next line
        prev_value = value
    
    # print(f"is_safe 3: {is_safe}")

    return is_safe


if __name__ == "__main__":
    main()
