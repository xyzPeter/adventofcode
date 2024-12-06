import functools

def main():
    # data_file = r".\2024\05\data_example.txt"
    data_file = r".\2024\05\data.txt"

    print("\n")  # keep debug output on a new line

    with open(data_file, "r") as file:
        lines = file.readlines()
        # Remove newline characters from each line
        lines = [line.rstrip('\n') for line in lines] 
        # ans = part_1(lines)
        ans = part_2(lines)
        print(f"\nanswer = {ans}")


def part_1(lines):
    result = 0  # sum of middle numbers

    rules = []
    pages = []

    ordering_rules = True
    for line in lines:
        if ordering_rules:
            if line == "":
                ordering_rules = False
            else:
                rules.append(list(map(int, line.split("|"))))
        else:
            pages.append(list(map(int, line.split(","))))

    for page in pages:
        # print(page)
        page_valid = True # for now...
        for rule in rules:
            try:
                pos1 = page.index(rule[0])
                pos2 = page.index(rule[1])
                if pos2 < pos1:
                    page_valid = False
                    break
            except ValueError:
                pass
            
        if page_valid:
            # All of the page ordering rules passed
            # Find the middle value in the page and add to result
            result += page[len(page)//2]

    return result

global rules


def comp_func(val1, val2):
    global rules

    for rule in rules:
        if val1 in rule and val2 in rule:
            if rule.index(val1) == 1:
                return -1
            else:
                return 1
            
    return 0
                

def part_2(lines):
    result = 0  # sum of middle numbers

    global rules
    rules = []
    pages = []
    invalid_pages = []

    ordering_rules = True
    for line in lines:
        if ordering_rules:
            if line == "":
                ordering_rules = False
            else:
                rules.append(list(map(int, line.split("|"))))
        else:
            pages.append(list(map(int, line.split(","))))

    for page in pages:
        # print(page)
        page_valid = True # for now...
        for rule in rules:
            try:
                pos1 = page.index(rule[0])
                pos2 = page.index(rule[1])
                if pos2 < pos1:
                    page_valid = False
                    break
            except ValueError:
                pass
            
        if page_valid:
            # All of the page ordering rules passed
            # Find the middle value in the page and add to result
            result += page[len(page)//2]
        else:
            invalid_pages.append(page)

    result = 0 # reset result
    for page in invalid_pages:
        page = sorted(page, key=functools.cmp_to_key(comp_func))
        result += page[len(page) // 2]

    return result

if __name__ == "__main__":
    main()
