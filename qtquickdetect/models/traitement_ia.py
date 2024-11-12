import os
import uuid
import shutil
import re
import torch  # Importer torch pour la gestion du dispositif
from pathlib import Path
from ultralytics import YOLOWorld
from utils import filepaths

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def traitementPrompt(filePath: str, classes: list = None, typ: str = None) -> str:
    models_path = filepaths.get_base_data_dir() / 'models'
    model = YOLOWorld(os.path.join(models_path, 'yolov8s-world.pt'))

    model = model.to(device)
    
    if classes:
        model.set_classes(classes)
    
    collections_dir = filepaths.get_base_data_dir() / 'collections'
    if typ == "image":
        collections_dir = collections_dir / "image"
    else:
        collections_dir = collections_dir / "video"

    os.makedirs(collections_dir, exist_ok=True)

    # Effectuer la prédiction sur le GPU
    with torch.no_grad():  # Utiliser torch.no_grad pour réduire l'utilisation de la mémoire
        results = model.predict(filePath, save=True, save_dir=str(collections_dir), exist_ok=True)
    
    saved_image_path = results[0].save_dir
    filePath_without_extension = os.path.splitext(filePath)[0]
    saved_files = list(Path(saved_image_path).glob(os.path.basename(filePath_without_extension) + '*'))[0]

    final_image_path = collections_dir / f"ia_{str(uuid.uuid4())}"
    shutil.move(saved_image_path, final_image_path)

    f = final_image_path / os.path.basename(saved_files)
    return str(f)



