import tensorflow as tf
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

def calc(a, b):
    return a + b

def clasificar_imagen(img_path):

    # Cargar el modelo y las etiquetas
    model = load_model("./converted_keras/keras_model.h5", compile=False)
    with open("./converted_keras/labels.txt", "r") as f:
        class_names = f.read().splitlines()

    # Preprocesar la imagen
    size = (224, 224)
    image = Image.open(img_path).convert("RGB")
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # Predicción
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return class_name.strip(), float(confidence_score)