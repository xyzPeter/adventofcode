
def main():
    # data_file = r".\2024\09\data_example.txt"
    data_file = r".\2024\09\data.txt"

    print("\n")  # keep debug output on a new line

    with open(data_file, "r") as file:
        lines = file.readlines()
        # Remove newline characters from each line
        lines = [line.rstrip("\n") for line in lines]
        # ans = part_1(lines)
        ans = part_2(lines)
        print(f"\nanswer = {ans}")


def part_1(lines):
    result = 0  # filesystem checksum

    disk = []
    file_id = 0

    for i, c in enumerate(lines[0]):
        if i % 2 == 0:
            disk += [file_id] * int(c)
        else:
            # Odd index this is space - pos 0 is even and first file
            disk += ["."] * int(c)
            file_id += 1

    print("1:", disk)

    pos = 0
    last_file_idx = len(disk) - 1
    while pos < last_file_idx:
        if disk[pos] == ".":
            # Have a space, move a file here
            while disk[last_file_idx] == ".":
                last_file_idx -= 1
                disk.pop()
            if pos >= last_file_idx:
                break
            disk[pos] = disk[last_file_idx]
            disk.pop()
            last_file_idx -= 1

        pos += 1



    print("\n\n")
    print("2: ", disk)

    for i, val in enumerate(disk):
        result += i * val

    return result


def part_2(lines):
    # this function took several minutes to run - could be rewritten
    # to be more efficient!
    result = 0  # filesystem checksum

    disk = []
    file_id = 0

    # Load disk array - file ids or "." for free space
    for i, c in enumerate(lines[0]):
        if i % 2 == 0:
            disk += [file_id] * int(c)
        else:
            # Odd index this is space - pos 0 is even and first file
            disk += ["."] * int(c)
            file_id += 1

    print("1:", disk)

    # compact disk - move files to free space at start of disk
    # this time only move whole files
    last_file_idx = len(disk) - 1
    
    # work backward from end of disk, moving whole files only
    while last_file_idx > 0:
        if disk[last_file_idx] == ".":
            last_file_idx -= 1
            continue
        else:
            file_id = disk[last_file_idx]
            # find size of this file
            current_file_idx = last_file_idx - 1
            while current_file_idx > 0 and disk[current_file_idx] == disk[last_file_idx]:
                current_file_idx -= 1
            file_length = last_file_idx - current_file_idx

            # search for free space of at least file_length
            pos = 0
            while pos < current_file_idx:
                if disk[pos:pos+file_length] == ["."] * file_length:
                    disk[pos:pos+file_length] = [disk[last_file_idx]] * file_length
                    disk[current_file_idx+1:current_file_idx+1+file_length] = ["."] * file_length
                    pos += file_length
                    break
                # did not find a large enough space - keep looping
                pos += 1
            
            assert(file_length > 0)
            last_file_idx -= file_length

    for i, val in enumerate(disk):
        if val != ".":
            result += i * val

    return result


if __name__ == "__main__":
    main()
