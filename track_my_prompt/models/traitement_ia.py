import os
import uuid
import shutil
import torch
import random
from pathlib import Path
from ultralytics import YOLOWorld
from utils import filepaths
import cv2
from models.encylo import EncyclopediaModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def traitementPrompt(filePath: str, classes: list = None, typ: str = "video", encyclopedia_model: EncyclopediaModel = None, color = (0, 255, 0)) -> str:
    """
    Process the prompt and return the path to the processed file.

    Args:
        filePath (str): Path to the input file.
        classes (list, optional): List of classes to detect. Defaults to None.
        typ (str, optional): Type of the input file ('image' or 'video'). Defaults to "video".
        encyclopedia_model (EncyclopediaModel, optional): Encyclopedia model for updating class counts. Defaults to None.

    Returns:
        str: Path to the processed file.
    """
    models_path = filepaths.get_base_data_dir() / 'models'
    model = YOLOWorld(os.path.join(models_path, 'yolov8s-world.pt'))

    model = model.to(device)

    if classes:
        model.set_classes(classes)
        if encyclopedia_model != None:
            encyclopedia_model.incrementTimeFound(classes)
    collections_dir = filepaths.get_base_data_dir() / 'collections' / typ
    os.makedirs(collections_dir, exist_ok=True)

    if typ == "image":
        image = cv2.imread(filePath)
        if image is None:
            print(f"Erreur : Impossible de lire l'image {filePath}")
            return ""

        with torch.no_grad():
            results = model.predict(image, stream=True)

        for r in results:
            for i, box in enumerate(r.boxes.xyxy):
                x1, y1, x2, y2 = map(int, box)

                if color == "rainbow":
                    color_to_use = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                else:
                    color_to_use = color

                cv2.rectangle(image, (x1, y1), (x2, y2), color_to_use, 4)

                if r.boxes.conf is not None and i < len(r.boxes.conf):
                    confidence = r.boxes.conf[i].item() * 100
                    class_index = int(r.boxes.cls[i].item())
                    class_name = model.names[class_index] if class_index in model.names else "Unknown"
                    label = f"{class_name} {confidence:.1f}%"
                    cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color_to_use, 2)

            if r.masks is not None:
                r.masks.draw(image)

        final_image_path = collections_dir / f"ia_{str(uuid.uuid4())}.png"
        cv2.imwrite(str(final_image_path), image)

        return str(final_image_path)
    
    else:
        cap = cv2.VideoCapture(filePath)
        if not cap.isOpened():
            print(f"Erreur : Impossible de lire le fichier vidéo {filePath}")
            return ""
        
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        output_video_path = collections_dir / f"output_{str(uuid.uuid4())}.mp4"
        out = cv2.VideoWriter(str(output_video_path), cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

        with torch.no_grad():
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                results = model.predict(frame, stream=True)
                
                for r in results:
                    for i, box in enumerate(r.boxes.xyxy):
                        x1, y1, x2, y2 = map(int, box)
                        if color == "rainbow":
                            color_to_use = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                        else:
                            color_to_use = color
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color_to_use, 4)
                        
                        if r.boxes.conf is not None and i < len(r.boxes.conf):
                            confidence = r.boxes.conf[i].item() * 100 
                            class_index = int(r.boxes.cls[i].item())
                            class_name = model.names[class_index] if class_index in model.names else "Unknown"
                            label = f"{class_name} {confidence:.1f}%"

                            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color_to_use, 2)

                    if r.masks is not None:
                        r.masks.draw(frame)


                out.write(frame)

        cap.release()
        out.release()

        return str(output_video_path)
