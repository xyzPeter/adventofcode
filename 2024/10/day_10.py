
def main():
    # data_file = r".\2024\10\data_example.txt"
    data_file = r".\2024\10\data.txt"

    print("\n\n")  # keep debug output on a new line

    with open(data_file, "r") as file:
        lines = file.readlines()
        # Remove newline characters from each line
        lines = [line.rstrip("\n") for line in lines]
        # ans = part_1(lines)
        ans = part_2(lines)
        print(f"\nanswer = {ans}")


# use a global variable for number of viable trails
# accumulate this variable in the recursive find_trail function
# we need to find the number of reachable peaks for each trailhead, not
# the number of paths to these peaks.
reachable_peaks = set()  # number of trails
total_trails = 0

def find_trail(lines, last_height, r, c):
    global reachable_peaks
    global total_trails

    height = int(lines[r][c])
    if height != last_height + 1:
        return # not a valid trail
    
    # print(f"find_trail(), next step identified, num_trails: {len(reachable_peaks)}, height: {height}, r: {r}, c: {c}")

    if height == 9:
        reachable_peaks.add((r, c))
        total_trails += 1
        return
    
    # test each direction for height + 1
    if c > 0:
        find_trail(lines, height, r, c-1)
    if r > 0:
        find_trail(lines, height, r-1, c)
    if c < len(lines[r]) - 1:
        find_trail(lines, height, r, c+1)
    if r < len(lines) - 1:
        find_trail(lines, height, r+1, c)

    return

def part_1(lines):
    result = 0 # number of viable trails
    global reachable_peaks
    num_trailheads = 0

    for r, line in enumerate(lines):
        for c, val in enumerate(line):
            if val == "0":
                num_trailheads += 1
                # trailhead - start looking for all trails:
                # print(f"trailhead #: {num_trailheads}")
                find_trail(lines, -1, r, c) # pass in last_height of -1, as we are not actually testing the next step yet
                # print(f"trailhead at: ({r}, {c})")
                # print(f"after find_trail, num trails: {len(reachable_peaks)}")
                # print(reachable_peaks)
                result += len(reachable_peaks)
                reachable_peaks.clear()

    return result


def part_2(lines):
    result = 0 # number of viable trails
    global reachable_peaks
    global total_trails

    num_trailheads = 0

    for r, line in enumerate(lines):
        for c, val in enumerate(line):
            if val == "0":
                num_trailheads += 1
                # trailhead - start looking for all trails:
                # print(f"trailhead #: {num_trailheads}")
                find_trail(lines, -1, r, c) # pass in last_height of -1, as we are not actually testing the next step yet
                # print(f"trailhead at: ({r}, {c})")
                # print(f"after find_trail, num trails: {len(reachable_peaks)}")
                # print(reachable_peaks)
                result += len(reachable_peaks)
                reachable_peaks.clear()

    return total_trails


if __name__ == "__main__":
    main()
