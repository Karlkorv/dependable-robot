import random
from time import sleep


board = [[1, 2, 3, 4, 5, 6],
         [7, 8, 9, 10, 11, 12],
         [13, 14, 15, 16, 17, 18], 
         [19, 20, 21, 22, 23, 24],
         [25, 26, 27, 28, 29, 30],
         [31, 32, 33, 34, 35, 36],
         [37, 38, 39, 40, 41, 42]]

known_obstacles = [[False, False, False, False, False, False],
                   [False, True, True, False, False, False],
                   [False, False, False, False, False, False],
                   [False, False, False, False, False, False],
                   [False, False, False, False, True, False],
                   [False, False, False, False, True, False],
                   [False, False, False, False, False, False]]

# robot_position = (0, 0)
# target_position = (6, 3)

# def print_board(board, known_obstacles, robot_position, target_position):
#     for r in range(len(board)):
#         row_display = ""
#         for c in range(len(board[0])):
#             if (r, c) == robot_position:
#                 row_display += " R "
#             elif (r, c) == target_position:
#                 row_display += " T "
#             elif known_obstacles[r][c]:
#                 row_display += " X "
#             else:
#                 row_display += f" . "
#         print(row_display)
#     print("\n")


# def step_through_path(path, known_obstacles=known_obstacles):
#     if not path:
#         return robot_position
    
#     robot_position = path[0]
    
#     for position in path[1:]:
#         # check for robots in the way
#         print(f"Bug2: Stepping to position {position}")
#         print_board(board, known_obstacles, position, target_position)
#         sleep(1) 
#         robot_position = position
        
#     return robot_position


def dijkstra_find_path(board, known_obstacles, start_pos, end_pos):
    rows = len(board)
    cols = len(board[0])

    distances = [[float('inf')] * cols for _ in range(rows)]
    distances[start_pos[0]][start_pos[1]] = 0

    previous_nodes = [[None] * cols for _ in range(rows)]   
    unvisited = set((r, c) for r in range(rows) for c in range(cols) if not known_obstacles[r][c])

    while unvisited:
        current = min(unvisited, key=lambda pos: distances[pos[0]][pos[1]])
        unvisited.remove(current)

        if current == end_pos:
            break

        neighbors = [(current[0] + dr, current[1] + dc) for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        for neighbor in neighbors:
            r, c = neighbor
            if 0 <= r < rows and 0 <= c < cols and not known_obstacles[r][c] and neighbor in unvisited:
                alt_distance = distances[current[0]][current[1]] + 1
                if alt_distance < distances[r][c]:
                    distances[r][c] = alt_distance
                    previous_nodes[r][c] = current

    # Reconstruct the shortest path
    path = []
    while end_pos is not None:
        path.append(end_pos)
        end_pos = previous_nodes[end_pos[0]][end_pos[1]]
    path.reverse()

    if path[0] != robot_position:
        print("No path found!")
        return []

    return path


# path = dijkstra_find_path(board, known_obstacles, robot_position, target_position)
# for i in path:
#     print("Dijkstra's shortest path step: ", i)
#     print_board(board, known_obstacles, i, target_position)
#     sleep(1)

# while (new_position := step_through_path(path, known_obstacles)) != target_position:
#     robot_position = new_position
#     path = dijkstra_find_path(board, known_obstacles, robot_position, target_position)
#     if not path:
#         print("No available path to the target!")
#         break

# if new_position == target_position:
#     robot_position = new_position
    
# if robot_position == target_position:
#     print("Robot has reached the target!")
# print("Robot terminating at: ", robot_position, " Target was at: ", target_position)
