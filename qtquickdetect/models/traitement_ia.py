from ultralytics import YOLOWorld
import os

class ia:
    def traitement(filePath : str) -> str:
        model = YOLOWorld("../resources/pre-trained_models/yolov8s-world.pt")
        results = model.predict(filePath, save=True)

        save_dir = results[0].save_dir
        file_name = os.path.basename(filePath)
        saved_image_path = os.path.join(save_dir, file_name)

        return saved_image_path
    
    def traitementPrompt(filePath : str, classes : list) -> str:
        model = YOLOWorld("../resources/pre-trained_models/yolov8s-world.pt")
        model.set_classes(classes)
        results = model.predict(filePath, save=True)

        save_dir = results[0].save_dir
        file_name = os.path.basename(filePath)
        saved_image_path = os.path.join(save_dir, file_name)

        return saved_image_path
