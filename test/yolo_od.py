from ultralytics import YOLO

# Build a YOLOv9c model from scratch
# model = YOLO('yolov9c.yaml')

# Build a YOLOv9c model from pretrained weight
model = YOLO('models/yolov9c.pt')

# Display model information (optional)
# model.info()

# Train the model on the COCO8 example dataset for 100 epochs
# results = model.train(data='coco8.yaml', epochs=100, imgsz=640)

# Run inference with the YOLOv9c model on the 'bus.jpg' image
results = model("inputs/dragon.jpg")
print(results)