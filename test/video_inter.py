import cv2

# Paths to your video files
# video_path1 = "C:/Users/Aditya Sharma/Videos/football/football_aspire_25022024.mp4"
# video_path2 = "C:/Users/Aditya Sharma/Videos/a silent voice.mp4"

import cv2
import pygame
import sys

# Initialize Pygame
pygame.init()

# Video paths
video_path1 = "C:/Users/Aditya Sharma/Videos/football/football_aspire_25022024.mp4"
video_path2 = "C:/Users/Aditya Sharma/Videos/a silent voice.mp4"

# Current video
current_video_path = video_path1

# Load the video using OpenCV
cap = cv2.VideoCapture(current_video_path)

# Get video size
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set up the Pygame window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Video Player')

# Function to switch videos
def switch_video(mouse_x):
    global current_video_path, cap
    if mouse_x < width // 2:
        if current_video_path != video_path1:
            current_video_path = video_path1
            cap = cv2.VideoCapture(video_path1)
    else:
        if current_video_path != video_path2:
            current_video_path = video_path2
            cap = cv2.VideoCapture(video_path2)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check for mouse position
    mouse_x, _ = pygame.mouse.get_pos()
    switch_video(mouse_x)

    ret, frame = cap.read()
    if not ret:
        # Restart the video if it ends
        cap = cv2.VideoCapture(current_video_path)
        continue

    # Convert the frame color from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert the frame to a Surface and display it
    frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    window.blit(frame_surface, (0, 0))

    pygame.display.update()

# Clean up
cap.release()
pygame.quit()
sys.exit()
