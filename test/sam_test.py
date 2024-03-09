from ultralytics import SAM

# Load the model
model = SAM('../models/mobile_sam.pt')

# # Predict a segment based on a point prompt
# model.predict(r"C:\Users\Aditya Sharma\Pictures\zidane.jpg", points=[900, 370], labels=[1])

# Predict a segment based on a box prompt
preds = model.predict(r"C:\Users\Aditya Sharma\Pictures\zidane.jpg", bboxes=[439, 437, 524, 709])
print(preds)