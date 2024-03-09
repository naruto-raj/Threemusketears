import cv2

import cv2
import pygame
import sys
from ultralytics import SAM

# # Load the model

# # # Predict a segment based on a point prompt

# Initialize Pygame

class VideoPipeline:
    def __init__(self) -> None:
        pygame.init()
        self.model = SAM('models/sam_l.pt')
        # self.model = SAM('models/mobile_sam.pt')

    
    def video_interaction(self,frame, segmentation_point):
        self.preds = self.model.predict(frame, points=segmentation_point)
        print(self.preds)

    def dislpay_video(self, path):
        cap = cv2.VideoCapture(path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Set up the Pygame window
        window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Video Player')
        running = True
        while running:
            segmentation_point = ()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    segmentation_point = pygame.mouse.get_pos()
            ret, frame = cap.read()
            if not ret:
                cap = cv2.VideoCapture(path)
                continue
            # Convert the frame color from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if segmentation_point:
                self.video_interaction(frame, segmentation_point)

            # Convert the frame to a Surface and display it
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            window.blit(frame_surface, (0, 0))

            pygame.display.update()

        # Clean up
        cap.release()
        pygame.quit()
        sys.exit()

    
obj = VideoPipeline()
obj.dislpay_video(path="C:/Users/Aditya Sharma/Videos/football/G1 - Made with Clipchamp.mp4")
# Video paths
# video_path1 = "C:/Users/Aditya Sharma/Videos/football/football_aspire_25022024.mp4"
# video_path2 = "C:/Users/Aditya Sharma/Videos/a silent voice.mp4"

# Current video
# current_video_path = video_path1

# Load the video using OpenCV
# cap = cv2.VideoCapture(current_video_path)

# # Get video size
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Set up the Pygame window
# window = pygame.display.set_mode((width, height))
# pygame.display.set_caption('Video Player')

# Function to switch videos


# Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Check for mouse position
#     mouse_x, _ = pygame.mouse.get_pos()
#     switch_video(mouse_x)

#     ret, frame = cap.read()
#     if not ret:
#         # Restart the video if it ends
#         cap = cv2.VideoCapture(current_video_path)
#         continue

#     # Convert the frame color from BGR to RGB
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Convert the frame to a Surface and display it
#     frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
#     window.blit(frame_surface, (0, 0))

#     pygame.display.update()

# # Clean up
# cap.release()
# pygame.quit()
# sys.exit()
