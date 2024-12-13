from functools import cache

def main():
    print("Hello from adventofcode!")


@cache
def solve(rock, steps):

    steps -= 1
    if steps <= 0:
        return rock

    if rock == 0:
        return solve(1, steps - 1)

    s_rock = str(rock)
    if len(s_rock) % 2 == 0:
        return solve(int(s_rock[:len(s_rock)//2], steps - 1) + solve(int(s_rock[len(s_rock)//2:], steps - 1)

    return solve(rock*2024, steps-1)


if __name__ == "__main__":
    main()
