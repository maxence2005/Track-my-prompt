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

def traitementPrompt(filePath: str, classes: list = None, typ: str = "video", encyclopedia_model: EncyclopediaModel = None) -> str:
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
        with torch.no_grad():  
            results = model.predict(filePath, save=True, save_dir=str(collections_dir), exist_ok=True)
        
        saved_image_path = results[0].save_dir
        filePath_without_extension = os.path.splitext(filePath)[0]
        saved_files = list(Path(saved_image_path).glob(os.path.basename(filePath_without_extension) + '*'))[0]

        final_image_path = collections_dir / f"ia_{str(uuid.uuid4())}"
        shutil.move(saved_image_path, final_image_path)

        f = final_image_path / os.path.basename(saved_files)
        return str(f)
    
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
                        
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        
                        if r.boxes.conf is not None and i < len(r.boxes.conf):
                            confidence = r.boxes.conf[i].item() * 100  # Confiance en pourcentage
                            class_index = int(r.boxes.cls[i].item())  # Indice de la classe
                            class_name = model.names[class_index] if class_index in model.names else "Unknown"
                            label = f"{class_name} {confidence:.1f}%"

                            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

                    if r.masks is not None:
                        r.masks.draw(frame)


                out.write(frame)  # Écrire la frame avec les cadres

        cap.release()
        out.release()

        return str(output_video_path)
