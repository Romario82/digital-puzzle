import pazl


def open_file(filename):
  #file = 'pazl.txt'
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
    path, total_puzzle = pazl.solve_puzzle(data)

    total_pieces = len(data.splitlines())
    print(f"Number of fragments used: {len(path)} из {total_pieces}")
    print("-" * 40)
    print("Sequence of fragments:")
    print(" -> ".join(path))
    print("-" * 40)
    print("Largest Number Puzzle (Answer):")
    print(total_puzzle)

if __name__ == "__main__":
  lines = open_file()
  data = prepare_data(lines)
  path, total_puzzle = pazl.solve_puzzle(data)

  total_pieces = len(data.splitlines())
  print(f"Number of fragments used: {len(path)} из {total_pieces}")
  print("-" * 40)
  print("Sequence of fragments:")
  print(" -> ".join(path))
  print("-" * 40)
  print("Largest Number Puzzle (Answer):")
  print(total_puzzle)