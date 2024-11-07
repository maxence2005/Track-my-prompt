from ultralytics import YOLOWorld
from utils import filepaths
import os
import re
import shutil
import uuid

def traitement(filePath : str) -> str:
    models_path = filepaths.get_base_data_dir() / 'models'
    model = YOLOWorld(os.path.join(models_path, 'yolov8s-world.pt'))
    results = model.predict(filePath, save=True)

    save_dir = results[0].save_dir
    file_name = os.path.basename(filePath)
    saved_image_path = os.path.join(save_dir, file_name)

    return saved_image_path

def traitementPrompt(filePath: str, classes: list, typ : str) -> str:
    models_path = filepaths.get_base_data_dir() / 'models'
    model = YOLOWorld(os.path.join(models_path, 'yolov8s-world.pt'))
    model.set_classes(classes)
    
    if typ == "image":
        collections_dir = filepaths.get_base_data_dir() / 'collections' / "image"
    else:
        collections_dir = filepaths.get_base_data_dir() / 'collections' / "video"

    os.makedirs(collections_dir, exist_ok=True)

    results = model.predict(filePath, save=True, save_dir=str(collections_dir), exist_ok=True)

    saved_image_path = results[0].save_dir 
    final_image_path = collections_dir / f"ia_{str(uuid.uuid4())}"

    shutil.move(saved_image_path, final_image_path)

    f = final_image_path / os.path.basename(filePath)
    return str(f)

def promptFiltre(phrase: str) -> list:

    available_classes = ["person", "backpack", "umbrella", "handbag", "suitcase", "tie", "bicycle", "car", 
        "motorcycle", "airplane", "train", "bus", "truck", "boat", "traffic light", 
        "fire hydrant", "stop sign", "parking meter", "bench", "sheep", "cow", "cat", 
        "horse", "dog", "bird", "elephant", "bear", "baseball glove", "kite", "giraffe", 
        "zebra", "tennis racket", "skateboard", "sports ball", "baseball bat", 
        "snowboard", "frisbee", "skis", "bottle", "wine glass", "fork", "cup", "knife", 
        "spoon", "bowl", "cake", "donut", "hot dog", "pizza", "carrot", "broccoli", 
        "sandwich", "orange", "apple", "banana", "couch", "chair", "potted plant", 
        "bed", "toilet", "dining table", "keyboard", "cell phone", "remote", "laptop", 
        "tv", "mouse", "microwave", "oven", "sink", "toaster", "refrigerator", 
        "teddy bear", "hair drier", "toothbrush", "scissors", "clock", "book", "vase"]

    phrase = phrase.lower()
    phrase = re.sub(r'[^\w\s]', '', phrase)
    

    words = phrase.split()
    

    filtered_classes = [word for word in words if word in available_classes]
    
    return filtered_classes
