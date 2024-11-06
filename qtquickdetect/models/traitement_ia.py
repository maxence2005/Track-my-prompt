from ultralytics import YOLOWorld
from ..utils import filepaths
import os

class ia:
    def traitement(filePath : str) -> str:
        models_path = filepaths.get_base_data_dir() / 'models'
        model = YOLOWorld(os.path.join(models_path, 'yolov8s-world.pt'))
        results = model.predict(filePath, save=True)

        save_dir = results[0].save_dir
        file_name = os.path.basename(filePath)
        saved_image_path = os.path.join(save_dir, file_name)

        return saved_image_path
    
    def traitementPrompt(filePath : str, classes : list) -> str:
        models_path = filepaths.get_base_data_dir() / 'models'
        model = YOLOWorld(os.path.join(models_path, 'yolov8s-world.pt'))
        model.set_classes(classes)
        results = model.predict(filePath, save=True)

        save_dir = results[0].save_dir
        file_name = os.path.basename(filePath)
        saved_image_path = os.path.join(save_dir, file_name)

        return saved_image_path
