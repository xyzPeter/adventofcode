from functools import cache

def main():
    print("Hello from adventofcode!")
    rocks = "125 17"
    i_rocks = [int(x) for x in rocks.split()]
    
    result = 0
    for rock in i_rocks:
        result += solve(rock, 25)

    print(f"Num rocks: {result}")


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
