import tensorflow as tf
print(tf.__version__)



from imageai.Detection import ObjectDetection
import os

execution_path = os.getcwd()

ObjectDetection().setModelTypeAsRetinaNet()
ObjectDetection().setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
ObjectDetection().loadModel()
detections = ObjectDetection().detectObjectsFromImage(input_image=os.path.join(execution_path , "image.jpg"), output_image_path=os.path.join(execution_path , "imagenew.jpg"))

for eachObject in detections:
    print(eachObject["name"] , " : " , eachObject["percentage_probability"] )