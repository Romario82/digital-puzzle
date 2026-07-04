import puzzle


def open_file(filename):
  file = filename
  with open(file, encoding='utf-8') as file_object:
    lines = file_object.readlines()
  return lines


def prepare_data(lines):
  text = ''.join(lines)
  pieces = [piece.strip() for piece in text.replace(',', '\n').split('\n') if piece.strip()]
  return '\n'.join(pieces)

def startconsol(filename):
    lines = open_file(filename)
    data = prepare_data(lines)
    path, total_puzzle = puzzle.solve_puzzle(data)

    print(f"Number of fragments used: {len(path)}")
    print(f"Maximum sequence length in characters: {len(total_puzzle)}")
    print("\nMaximum sequence:")
    print(total_puzzle)
    print("\nFragment order:")
    print(" -> ".join(path))

if __name__ == "__main__":
  import sys
  filename = sys.argv[1] if len(sys.argv) > 1 else 'pazl.txt'
  lines = open_file(filename)
  data = prepare_data(lines)
  path, total_puzzle = puzzle.solve_puzzle(data)

  print(f"Number of fragments used: {len(path)}")
  print(f"Maximum sequence length in characters: {len(total_puzzle)}")
  print("\nMaximum sequence:")
  print(total_puzzle)
  print("\nFragment order:")
  print(" -> ".join(path))