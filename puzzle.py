import os


def find_longest_puzzle(numbers):
    adj = {}
    for num in numbers:
        prefix = num[:2]
        if prefix not in adj:
            adj[prefix] = []
        adj[prefix].append(num)

    best_path = []

    def dfs(current_num, current_path, used_numbers):
        nonlocal best_path


        if len(current_path) > len(best_path):
            best_path = current_path[:]

        suffix = current_num[-2:]
        if suffix in adj:
            for next_num in adj[suffix]:
                if next_num not in used_numbers:
                    used_numbers.add(next_num)
                    current_path.append(next_num)

                    dfs(next_num, current_path, used_numbers)

                    # Backtracking
                    current_path.pop()
                    used_numbers.remove(next_num)


    for start_num in numbers:
        dfs(start_num, [start_num], {start_num})

    return best_path


def reconstruct_sequence(path):
    if not path:
        return ""
    result = path[0]
    for num in path[1:]:
        result += num[2:]
    return result


def solve_puzzle(data_str):
    pieces = [line.strip() for line in data_str.strip().split('\n') if line.strip()]
    longest_path = find_longest_puzzle(pieces)
    final_sequence = reconstruct_sequence(longest_path)
    return longest_path, final_sequence


# --- FILE OPERATIONS ---
if __name__ == "__main__":
    file_name = "pazl.txt"

    if not os.path.exists(file_name):
        print(f"Error: File '{file_name}' not found!")
        print("Please create this file in the same folder as the script and paste the numbers there.")
    else:
        with open(file_name, "r", encoding="utf-8") as file:
            data = file.read().split()

        # Cleaning up potential non-digit characters
        data = [num.strip() for num in data if num.strip().isdigit()]

        print(f"Fragments read from file: {len(data)}")

        # Calculations
        longest_path = find_longest_puzzle(data)
        final_sequence = reconstruct_sequence(longest_path)

        # Output results
        print(f"Number of fragments used: {len(longest_path)}")
        print(f"Maximum sequence length in characters: {len(final_sequence)}")
        print("\nMaximum sequence:")
        print(final_sequence)
        print("\nFragment order:")
        print(" -> ".join(longest_path))