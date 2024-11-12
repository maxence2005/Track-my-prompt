import os
from nltk.stem import WordNetLemmatizer
import re
from utils.filepaths import get_base_data_dir


def promptFiltre(phrase: str) -> list:

    available_classes = {
        "person", "backpack", "umbrella", "handbag", "suitcase", "tie", "bicycle", "car", 
        "motorcycle", "airplane", "train", "bus", "truck", "boat", "traffic light", 
        "fire hydrant", "stop sign", "parking meter", "bench", "sheep", "cow", "cat", 
        "horse", "dog", "bird", "elephant", "bear", "baseball glove", "kite", "giraffe", 
        "zebra", "tennis racket", "skateboard", "sports ball", "baseball bat", 
        "snowboard", "frisbee", "skis", "bottle", "wine glass", "fork", "cup", "knife", 
        "spoon", "bowl", "cake", "donut", "hot dog", "pizza", "carrot", "broccoli", 
        "sandwich", "orange", "apple", "banana", "couch", "chair", "potted plant", 
        "bed", "toilet", "dining table", "keyboard", "cell phone", "remote", "laptop", 
        "tv", "mouse", "microwave", "oven", "sink", "toaster", "refrigerator", 
        "teddy bear", "hair drier", "toothbrush", "scissors", "clock", "book", "vase"
    }

    nltk_file = get_base_data_dir() / 'nltk'
    
    os.environ['NLTK_DATA'] = str(nltk_file)

    lemmatizer = WordNetLemmatizer()

    words = re.findall(r'\b\w+\b', phrase.lower())

    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

    filtered_classes = [word for word in lemmatized_words if word in available_classes]
    
    return filtered_classes