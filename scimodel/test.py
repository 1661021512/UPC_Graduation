from ultralytics import YOLO
model = YOLO("yolov8nCBAM.yaml")  # build a new model from scratch
# model = YOLO("best.pt")  # load a pretrained model (recommended for training)
# Use the model
# model.train(data="VOCData/Train.yaml", epochs=60)  # train the model
# metrics = model.val()  # evaluate model performance on the validation set