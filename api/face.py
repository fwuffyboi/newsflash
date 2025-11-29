import os
import cv2
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CASCADE_PATH = os.path.join(SCRIPT_DIR, "haarcascade_frontalface_default.xml")
print(SCRIPT_DIR, CASCADE_PATH)

cascade = cv2.CascadeClassifier(CASCADE_PATH)

def detect_face(image_bytes, logger):

    # Convert to a NumPy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    max_dim = 640

    # Decode the image – Pillow is faster than cv2.imread for raw bytes
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Resize to keep CPU load low
    h, w = img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))

    # Convert to grayscale – required by Haar
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces (smallest window 20x20, adjust as needed)
    faces = cascade.detectMultiScale(gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(20, 20)
    )

    return {'faces': len(faces), 'error': ''}