
"""
Entrena el modelo de ClasificaIA para detectar SMS spam.
"""

import csv
import sys
from datetime import datetime, timezone

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

SALIDA = sys.argv[1] if len(sys.argv) > 1 else "app/modelo.joblib"
SEMILLA = 42

# 1. Cargar los mensajes
mensajes = []
etiquetas = []

with open("datos/SMSSpamCollection", "r", encoding="utf-8") as archivo:
    lector = csv.reader(archivo, delimiter="\t")

    for fila in lector:
        if len(fila) >= 2 and fila[0] in ("ham", "spam"):
            etiquetas.append(fila[0])
            mensajes.append("\t".join(fila[1:]))

print(f"Mensajes cargados: {len(mensajes)}")

# 2. Separar entrenamiento y prueba
X_tr, X_te, y_tr, y_te = train_test_split(
    mensajes,
    etiquetas,
    test_size=0.30,
    random_state=SEMILLA,
    stratify=etiquetas
)

# 3. Crear modelo: TF-IDF + Multinomial Naive Bayes
modelo = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )),
    ("naive_bayes", MultinomialNB())
])

modelo.fit(X_tr, y_tr)

# 4. Evaluar el modelo
predicciones = modelo.predict(X_te)
exactitud = accuracy_score(y_te, predicciones)

print("\nReporte de clasificación:")
print(classification_report(y_te, predicciones))

# 5. Guardar modelo y metadatos
joblib.dump(
    {
        "modelo": modelo,
        "clases": list(modelo.classes_),
        "variables": ["mensaje"],
        "unidades": "texto",
        "exactitud": round(float(exactitud), 4),
        "version": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M"),
        "algoritmo": "Multinomial Naive Bayes",
    },
    SALIDA
)

print(f"Exactitud={exactitud:.3f} guardado en {SALIDA}")