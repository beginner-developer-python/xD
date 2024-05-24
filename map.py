import cv2
import time
import numpy as np
import networkx as nx
import pyautogui
import math
import json
import os


def load_overlay(overlay_path):
    """Load the overlay image and convert it to a binary image."""
    overlay = cv2.imread(overlay_path)
    # Convert the overlay to grayscale
    overlay_gray = cv2.cvtColor(overlay, cv2.COLOR_BGR2GRAY)
    # Threshold the grayscale image to create a binary image
    _, overlay_bin = cv2.threshold(overlay_gray, 1, 255, cv2.THRESH_BINARY)

    return overlay_bin


def find_path(start, end, overlay):
    """Find the path between the start and end points using A* algorithm."""
    # Create a graph from the overlay image
    graph = nx.grid_2d_graph(*overlay.shape[::-1])
    # Remove nodes corresponding to black pixels (obstacles) in the overlay
    for y, row in enumerate(overlay):
        for x, value in enumerate(row):
            if value == 0:
                graph.remove_node((x, y))
    # Find the shortest path between the start and end nodes using A* algorithm
    path_nodes = nx.astar_path(graph, start, end)
    # Convert the path nodes to pixel coordinates
    path_coords = [(node[0], node[1]) for node in path_nodes]
    return path_coords


def calculate_distances(path_coords):
    """Calculate the distances traveled in each direction along the path."""
    distances = []
    xcs = []
    prev_coord = path_coords[0]
    total_distance = 0
    prev_direction = None  # keep track of previous direction
    i = 0
    for coord in path_coords[1:]:
        dx = coord[0] - prev_coord[0]
        dy = coord[1] - prev_coord[1]
        distance = math.sqrt(dx**2 + dy**2) / 15
        total_distance += distance
        if dx > 0:
            if dy > 0:
                direction = "downright"
            elif dy == 0:
                direction = "right"
            else:
                direction = "upright"
        elif dx < 0:
            if dy > 0:
                direction = "downleft"
            elif dy == 0:
                direction = "left"
            else:
                direction = "upleft"
        else:
            if dy > 0:
                direction = "down"
            else:
                direction = "up"
        prev_coord = coord
        if i == 0:
            prev_direction = direction
            i += 1
        if prev_direction != direction:  # append only when direction changes
            if (int(total_distance) + 0.5) < total_distance:
                distances.append((prev_direction, (int(total_distance)+1)))
                prev_direction = direction  # update previous direction
                total_distance = 0
            else:
                distances.append((prev_direction, int(total_distance)))
                prev_direction = direction  # update previous direction
                total_distance = 0
    distances.append((prev_direction, int(total_distance + 1))
                     )  # append final distance
    print(distances)
    return distances


def draw_path(map_img, path_coords):
    """Draw the path on a copy of the map image."""
    # Draw a line connecting each pair of adjacent points in the path
    map_img = cv2.imread(map_img)
    for i in range(len(path_coords) - 1):
        cv2.line(map_img,
                 tuple(path_coords[i]), tuple(path_coords[i + 1]), (0, 35, 40), thickness=2)
    return map_img



def movetoend(path_grid):
    sleep = path_grid
    for i in range(len(sleep)):
        for n in range(int(sleep[i][1]+0.5)):
            if sleep[i][0] == "right":
                pyautogui.keyDown("D")
                time.sleep(0.05)
                pyautogui.keyUp("D")
            elif sleep[i][0] == "left":
                pyautogui.keyDown("A")
                time.sleep(0.05)
                pyautogui.keyUp("A")
            elif sleep[i][0] == "down":
                pyautogui.keyDown("S")
                time.sleep(0.05)
                pyautogui.keyUp("S")
            elif sleep[i][0] == "up":
                pyautogui.keyDown("W")
                time.sleep(0.05)
                pyautogui.keyUp("W")
            # time.sleep(0.15)


def path_main():
    start = (1064, 760)
    goal = (1192, 761)
    # Load the overlay image
    overlay = load_overlay('overlay.png')
    path_coords = None
    if os.path.isfile('path_coords.json'):
        with open('path_coords.json', 'r') as f:
            path_coords = json.load(f)

    else:
        path_coords = find_path(start, goal, overlay)
        with open('path_coords.json', 'w') as f:
            json.dump(path_coords, f)

    distance = calculate_distances(path_coords=path_coords)
    movetoend(distance)
with open("path_coords.json", "r") as f:
    path_coords1 = json.load(f)

print(path_coords1)

map_image = "map.png"
result_img = draw_path(map_img=map_image, path_coords=path_coords1)
real = cv2.resize(result_img, [1000, 1000])
cv2.imshow("Path Image", real)
cv2.waitKey(0)
cv2.destroyAllWindows()