import requests

from typing import Callable, Optional


def get_content_type(url: str) -> Optional[str]:
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        return response.headers.get('Content-Type', '').split(';')[0].strip()
    except requests.RequestException:
        return None

def is_image(url: str) -> bool:
    """
    Convenience function to check if a URL is an image
    :param url: URL to check
    :return: True if the URL points to what is supposed to be an image, False otherwise
    """

    content_type = get_content_type(url)
    if not content_type:
        return False
    image_types = ["image/jpeg", "image/png", "image/gif", "image/bmp", "image/tiff"]
    return content_type in image_types


def is_video(url: str) -> bool:
    """ 
    Convenience function to check if a URL is a video
    :param url: URL to check
    :return: True if the URL points to what is supposed to be a video, False otherwise
    """

    content_type = get_content_type(url)
    if not content_type:
        return False
    video_types = ["video/mp4", "video/avi", "video/mkv", "video/mpeg", "video/quicktime", "video/x-msvideo",
                   "video/webm"]
    return content_type in video_types


def is_live_video(url: str) -> bool:
    """
    Convenience function to check if a URL is a live video
    :param url: URL to check
    :return: True if the URL points to what is supposed to be a live video, False otherwise
    """

    content_type = get_content_type(url)
    live_content_types = ["application/vnd.apple.mpegurl", "application/dash+xml"]
    live_url_patterns = ["m3u8", ".ts", "live", "streaming"]
    if content_type and content_type in live_content_types:
        return True
    if any(pattern in url for pattern in live_url_patterns):
        return True
    return False


def is_url(url: str) -> bool:
    """
    Convenience function to check if a string is a valid URL
    :param url: String to check
    :return: True if the string is a valid URL, False otherwise
    """

    if not url.startswith('http'):
        return False

    try:
        requests.head(url, allow_redirects=True, timeout=10)
        return True
    except requests.RequestException:
        return False


def download_file(url: str, dst: str, cb: Optional[Callable[[int, int], None]] = None) -> None:
    try:
        resp = requests.get(url, stream=True)
        resp.raise_for_status()  # Vérifie si la requête a réussi
        
        total = int(resp.headers.get('content-length', 0))
        current = 0

        with open(dst, 'wb') as file:
            for chunk in resp.iter_content(chunk_size=1024):
                current += len(chunk)
                file.write(chunk)

                if cb:
                    cb(current, total)
    except requests.RequestException as e:
        print(f"Erreur lors du téléchargement du fichier : {e}")
    except IOError as e:
        print(f"Erreur lors de l'enregistrement du fichier : {e}")
