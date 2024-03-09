# from ultralytics import SAM

# # Load the model
# model = SAM('models/mobile_sam.pt')

# # # Predict a segment based on a point prompt
# # model.predict(r"C:\Users\Aditya Sharma\Pictures\zidane.jpg", points=[900, 370], labels=[1])

# # Predict a segment based on a box prompt
# preds = model.predict("inputs/dragon.jpg")
# # print(preds)

# from ultralytics import SAM

# # Load a model
# model = SAM('sam_b.pt')

# # Display model information (optional)
# model.info()

# # Run inference
# model('inputs\dragon.jpg')

from ultralytics import SAM, YOLO

# Profile SAM-b
model = SAM('sam_b.pt')
model.info()
model('inputs/dragon.jpg')

# Profile MobileSAM
# model = SAM('mobile_sam.pt')
# model.info()
# model('inputs/dragon.jpg')

# Profile FastSAM-s
# model = FastSAM('FastSAM-s.pt')
# model.info()
# model('inputs/dragon.jpg')

# Profile YOLOv8n-seg
model = YOLO('yolov8n-seg.pt')
model.info()
model('inputs/dragon.jpg')