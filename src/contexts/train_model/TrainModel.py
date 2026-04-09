import numpy as np
import joblib
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder


class TrainModel:

    def entrenarModelo():

        load_dotenv("/app/.env")
        USER = os.getenv("SUPABASE_USER")
        PASSWORD = os.getenv("SUPABASE_PASSWORD")
        HOST = os.getenv("SUPABASE_HOST")
        PORT = os.getenv("SUPABASE_PORT")
        DBNAME = os.getenv("SUPABASE_DBNAME")

        if PORT is None:
            print("no se lee el env")
            return
        else:
            print("si se lee el env")

        try:
            with psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                dbname=DBNAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT email, country, city, genre FROM "Dataset";')
                    rows = cursor.fetchall()
                    print(f"Filas recuperadas: {len(rows)}")

        except Exception as e:
            print(f"Error al conectar o recuperar datos: {e}")
            return

        if not rows:
            print("No se recuperaron filas. Abortando entrenamiento.")
            return

        # Convertir a DataFrame
        df = pd.DataFrame(rows, columns=["email", "country", "city", "genre"])

        # Separar X y Y
        X = df[["email", "country", "city"]].values
        y = df["genre"].values

        # Encoders
        encoder = OrdinalEncoder()
        X_encoded = encoder.fit_transform(X)

        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)

        # Dividir en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y_encoded, test_size=0.2, random_state=42
        )

        # Entrenar modelo clasificador
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Guardar los 3 archivos
        joblib.dump(model, os.getenv("MODELO_ENTRENADO"))
        joblib.dump(encoder, os.getenv("ENCODER_ENTRENADO"))
        joblib.dump(label_encoder, os.getenv("LABEL_ENCODER_ENTRENADO"))

        print("✅ Modelo, encoder y label_encoder guardados correctamente")
