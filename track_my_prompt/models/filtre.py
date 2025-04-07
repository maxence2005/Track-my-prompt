import os
from nltk.stem import WordNetLemmatizer
import re
from utils.filepaths import get_base_data_dir
import requests
import ast
from deep_translator import GoogleTranslator
from pathlib import Path

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

nltk_file = Path(get_base_data_dir()) / 'nltk'
os.environ['NLTK_DATA'] = str(nltk_file)
lemmatizer = WordNetLemmatizer()
word_pattern = re.compile(r'\b\w+\b')
lemmatizer.lemmatize("dog") # Initialize the lemmatizer

def promptFiltre(phrase: str, method: str, api_key: str = "") -> list:
    """
    Filter the prompt using the specified method.

    Args:
        phrase (str): The input prompt.
        method (str): The method to use for filtering ('dumb', 'dumb_ts', or 'mistral').
        api_key (str, optional): API key for the 'mistral' method. Defaults to "".

    Returns:
        list: List of filtered classes.
    """
    match method:
        case "dumb_ts":
            return traitement_dumb_ts(phrase)
        case "dumb":
            return traitement_dumb(phrase)
        case "mistral":
            return traitement_mistral(phrase, api_key)
        case _:
            raise ValueError(f"Invalid method : must be 'dumb' or 'mistral' but got {method}")

def traitement_dumb_ts(phrase: str) -> list:
    """
    Translate the phrase and filter it using the 'dumb' method.

    Args:
        phrase (str): The input phrase.

    Returns:
        list: List of filtered classes.
    """
    translated = GoogleTranslator().translate(phrase)
    return traitement_dumb(translated)

def traitement_dumb(phrase: str) -> list:
    """
    Filter the phrase using the 'dumb' method.

    Args:
        phrase (str): The input phrase.

    Returns:
        list: List of filtered classes.
    """
    words = word_pattern.findall(phrase.lower())
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    filtered_classes = [word for word in lemmatized_words if word in available_classes]
    return filtered_classes


def traitement_mistral(phrase: str, API_KEY: str) -> list:
    """
    Filter the phrase using the 'mistral' method.

    Args:
        phrase (str): The input phrase.
        API_KEY (str): API key for the Mistral API.

    Returns:
        list: List of filtered classes.
    """
    MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

    def get_list_filter(prompt):
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "mistral-large-latest",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            
            "max_tokens": 100,
            "temperature": 0.5,
            "top_p": 0.9
        }

        response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)
        
        if response.status_code == 200:
            try:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            except ValueError:
                print("Erreur lors de la conversion de la réponse en JSON")
                return None
        else:
            print(f"Erreur API: {response.status_code}")
            print(response.text)
            return None

    prompt = f"""You are an AI that aims to be integrated into an application called Track-My-Prompt, which is an application that aims to find certain content in an image. This application has a prompt field, where you will be used. In this field we want to detect what the user is looking for. We have the ability to detect objects only from this list, which we will call the list of detectables: {available_classes}.
    Via the user prompt that will follow, which can be in any language, you must be able to send me back as output a list of this form: ["requested object 1", "requested object 2" ...], and I don't want markdown syntax. The elements of this list must be in the same order as the elements of the list above, if an element is not present in the user prompt, do not include it in the output. for example, user inputs "dog" and "vacuum cleaner". the vacuum cleaner is not in the list therefore you should not include it. If an element is present several times, for example "dog", "dog", in the user prompt, do not repeat it. Please verify all elements in output list are in the detectable list.
    I want only this list as output, no superfluous text, it is intended to be used by a computer that understands nothing other than precise instructions, this list is a precise instruction.
    Here is the user prompt, don't forget to translate it in english before : """
    prompt += phrase
    filtered = get_list_filter(prompt)
    filtered = ast.literal_eval(filtered)
    return traitement_dumb(" ".join(filtered))