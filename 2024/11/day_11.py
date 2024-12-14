import functools


def main():
    # data_file = r".\2024\11\data_example.txt"
    data_file = r".\2024\11\data.txt"

    print("\n\n")  # keep output on a new line

    with open(data_file, "r") as file:
        lines = file.readlines()
        # Remove newline characters from each line
        lines = [line.rstrip("\n") for line in lines]
        ans = part_1(lines)
        print(f"\npart 1 answer = {ans}")
        ans = part_2(lines)
        print(f"\npart 2 answer = {ans}")


def blink(rocks):
    i = 0
    while i < len(rocks):
        s_rock = str(rocks[i])
        if rocks[i] == 0:
            rocks[i] = 1
        elif len(s_rock) % 2 == 0:
            # even number of rocks
            r1 = s_rock[: len(s_rock) // 2]
            rocks.insert(i, int(r1))
            r2 = s_rock[len(s_rock) // 2 :]
            i += 1
            rocks[i] = int(r2)
        else:
            rocks[i] = rocks[i] * 2024
        i += 1


def part_1(lines):
    result = 0  # number of rocks

    rocks = [int(x) for x in lines[0].split()]

    for i in range(25):
        blink(rocks)
        # print(rocks)

    result = len(rocks)

    return result


@functools.cache
def blink_2(rock, steps):

    if steps <= 0:
        return 1  # just one rock

    steps -= 1

    if rock == 0:
        return blink_2(1, steps)

    s_rock = str(rock)
    if len(s_rock) % 2 == 0:
        return blink_2(int(s_rock[: len(s_rock) // 2]), steps) + blink_2(
            int(s_rock[len(s_rock) // 2 :]), steps
        )

    return blink_2(rock * 2024, steps)


def part_2(lines):
    result = 0  # number of viable trails
    i_rocks = [int(x) for x in lines[0].split()]

    result = 0
    for rock in i_rocks:
        result += blink_2(rock, 75)

    return result


if __name__ == "__main__":
    main()
