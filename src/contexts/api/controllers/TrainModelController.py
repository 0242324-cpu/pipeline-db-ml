import os
import joblib
import numpy as np
from src.contexts.api.models import PredictorRequest


class TrainModelController:
    def execute(self, request: PredictorRequest):
        print(request)
        email = request.email
        country = request.country
        city = request.city

        # Cargar los modelos
        modelo = joblib.load(os.getenv("MODELO_ENTRENADO"))
        encoder = joblib.load(os.getenv("ENCODER_ENTRENADO"))
        label_encoder = joblib.load(os.getenv("LABEL_ENCODER_ENTRENADO"))

        # Codificar el dato de entrada
        nuevo_dato = encoder.transform(np.array([[email, country, city]]))

        # Predecir
        resultado = modelo.predict(nuevo_dato)
        genero = label_encoder.inverse_transform(resultado)

        print(f"Predicción: {genero[0]}")
        return {"status": "OK", "genre": genero[0]}
