def solve_puzzle(data_str):
  # Clean data from spaces and empty lines, keep only digit lines
  pieces = [line.strip() for line in data_str.strip().split('\n') if line.strip()]

  # Adjacency list: graph[prefix] = [(fragment_index, suffix, full_fragment), ...]
  graph = {}
  for i, piece in enumerate(pieces):
    prefix = piece[:2]
    suffix = piece[-2:]
    if prefix not in graph:
      graph[prefix] = []
    graph[prefix].append((i, suffix, piece))

  best_path = []
  max_length = 0
  visited = [False] * len(pieces)

  def dfs(current_node, current_path, current_len):
    nonlocal max_length, best_path

    if current_len > max_length:
      max_length = current_len
      best_path = list(current_path)

    if current_node in graph:
      for idx, next_node, piece in graph[current_node]:
        if not visited[idx]:
          visited[idx] = True
          current_path.append(piece)

          dfs(next_node, current_path, current_len + 1)

          current_path.pop()
          visited[idx] = False

  for i, piece in enumerate(pieces):
    visited[i] = True
    dfs(piece[-2:], [piece], 1)
    visited[i] = False

  if not best_path:
    return [], ""

  result_str = best_path[0]
  for p in best_path[1:]:
    result_str += p[2:]

  return best_path, result_str
