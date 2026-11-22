import os

# Desactivar la llave para las pruebas normales
os.environ["API_KEY"] = ""

import app.main as main_module
from fastapi.testclient import TestClient

cliente = TestClient(main_module.app)


def test_health():
    r = cliente.get("/health")

    assert r.status_code == 200
    datos = r.json()

    assert datos["status"] == "ok"
    assert datos["algoritmo"] == "Multinomial Naive Bayes"
    assert datos["exactitud"] > 0.99


def test_predict_spam():
    mensaje = {
        "mensaje": "Congratulations! You have won a free prize. Call now!"
    }

    r = cliente.post("/predict", json=mensaje)

    assert r.status_code == 200
    datos = r.json()

    assert datos["clase"] == "spam"
    assert datos["resultado"] == "Mensaje no deseado (SPAM)"
    assert 0 <= datos["confianza"] <= 1


def test_predict_ham():
    mensaje = {
        "mensaje": "Hey, are we still meeting for lunch today?"
    }

    r = cliente.post("/predict", json=mensaje)

    assert r.status_code == 200
    datos = r.json()

    assert datos["clase"] == "ham"
    assert datos["resultado"] == "Mensaje legítimo (HAM)"


def test_mensaje_vacio():
    r = cliente.post("/predict", json={"mensaje": ""})

    assert r.status_code == 422


def test_llave_requerida(monkeypatch):
    monkeypatch.setattr(main_module, "API_KEY", "secreto-de-prueba")

    mensaje = {
        "mensaje": "Congratulations! You won a free prize!"
    }

    r = cliente.post("/predict", json=mensaje)
    assert r.status_code == 401

    r = cliente.post(
        "/predict",
        json=mensaje,
        headers={"x-api-key": "secreto-de-prueba"}
    )

    assert r.status_code == 200