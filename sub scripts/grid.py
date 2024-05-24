import cv2

# Load image
img = cv2.imread('overlay.png')

# Define grid parameters
grid_size = 16
height, width, _ = img.shape

for x in range(0, width, grid_size):
    cv2.line(img, (x, 0), (x, height), (255,255, 0), 1)
    for y in range(0, height, grid_size):
        cv2.line(img, (0, y), (width, y), (255, 255, 0), 1)
        cv2.circle(img, (x+grid_size//2, y+grid_size//2), 2, (0, 0, 0), -1)


# Display image
cv2.imwrite('GridImage.png', img)
