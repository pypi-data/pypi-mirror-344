import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

class PredictionPipeline:
    def __init__(self,filename):
        self.filename =filename

    def predict(self):
        model = load_model(os.path.join("artifacts", "training", "model.keras"))
        test_image = image.load_img(self.filename, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = test_image / 255.0
        test_image = np.expand_dims(test_image, axis=0)

        # Get probabilities
        probabilities = model.predict(test_image)[0]
        print("Probabilities:", probabilities)

        result = np.argmax(probabilities)
        confidence = float(np.max(probabilities)) * 100
        prediction = 'Dog' if result == 1 else 'Cat'
        return [{
            "prediction": prediction,
            "confidence": round(confidence, 2)
        }]