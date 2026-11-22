
"""
ClasificaIA: API para detectar mensajes SMS spam.
Utiliza Multinomial Naive Bayes.
"""

import hmac
import os
from pathlib import Path

import joblib
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


# Modelo
CARPETA = Path(__file__).parent

ARTEFACTO = joblib.load(
    os.getenv("MODELO_PATH", CARPETA / "modelo.joblib")
)

MODELO = ARTEFACTO["modelo"]


# Seguridad
MOSTRAR_DOCS = os.getenv("MOSTRAR_DOCS", "1") == "1"
API_KEY = os.getenv("API_KEY", "")

app = FastAPI(
    title="ClasificaIA - Detector de SMS Spam",
    version=ARTEFACTO["version"],
    docs_url="/docs" if MOSTRAR_DOCS else None,
    redoc_url=None,
    openapi_url="/openapi.json" if MOSTRAR_DOCS else None
)

# Archivos estáticos: CSS, imágenes y JavaScript.
app.mount(
    "/static",
    StaticFiles(directory=CARPETA / "static"),
    name="static"
)


def requiere_llave(x_api_key: str = Header(default="")):
    if not API_KEY:
        return

    if not x_api_key:
        raise HTTPException(401, "Falta la cabecera x-api-key")

    if not hmac.compare_digest(x_api_key, API_KEY):
        raise HTTPException(403, "Llave inválida")


# Entrada
class MensajeSMS(BaseModel):
    """Texto del mensaje SMS que se desea clasificar."""

    mensaje: str = Field(min_length=1, max_length=500)


# Endpoints
@app.get("/health")
def salud():
    return {
        "status": "ok",
        "version": ARTEFACTO["version"],
        "algoritmo": ARTEFACTO["algoritmo"],
        "exactitud": ARTEFACTO["exactitud"],
        "variables": ARTEFACTO["variables"],
        "unidades": ARTEFACTO["unidades"]
    }


@app.post("/predict", dependencies=[Depends(requiere_llave)])
def predecir(datos: MensajeSMS):
    mensaje = datos.mensaje.strip()

    if not mensaje:
        raise HTTPException(422, "El mensaje no puede estar vacío")

    prediccion = MODELO.predict([mensaje])[0]
    probabilidades = MODELO.predict_proba([mensaje])[0]

    indice = list(MODELO.classes_).index(prediccion)
    confianza = float(probabilidades[indice])

    return {
        "clase": str(prediccion),
        "resultado": (
            "Mensaje no deseado (SPAM)"
            if prediccion == "spam"
            else "Mensaje legítimo (HAM)"
        ),
        "confianza": round(confianza, 3),
        "algoritmo": ARTEFACTO["algoritmo"],
        "exactitud_modelo": ARTEFACTO["exactitud"]
    }


@app.get("/", response_class=HTMLResponse)
def inicio():
    return (CARPETA / "index.html").read_text(encoding="utf-8")