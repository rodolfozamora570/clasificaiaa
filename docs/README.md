# Hito 1. Propuesta

## Proyecto: Detector de SMS Spam

### 1. Problema y usuarios

Nuestro proyecto consiste en crear un programa que utilice inteligencia artificial para ayudar a identificar si un mensaje SMS es spam o un mensaje normal. Está pensado principalmente para estudiantes y personas que reciben muchos mensajes de estafas como "ganaste un premio" o "da click aquí".

Este programa será una herramienta de apoyo para aprender cómo la inteligencia artificial puede protegernos de los mensajes falsos y no reemplazará al filtro que ya tienen los celulares.

### 2. Datos

Para realizar el proyecto utilizaremos una base de datos llamada **SMS Spam Collection**, que contiene mensajes SMS reales que ya están clasificados como spam o normales.

- Fuente: https://archive.ics.uci.edu/dataset/228/sms+spam+collection
- Licencia: CC BY 4.0 - Uso libre para investigación.
- Cantidad de registros: 5,574 mensajes.
- Información: 4,827 mensajes son normales (ham) y 747 mensajes son spam.
- Variables de entrada: 1 variable de texto, que es el contenido del mensaje `message`.
- Resultado que buscamos: saber si el mensaje es `ham` (normal) o `spam` (basura / estafa).

Los datos no son de nuestra región, fueron recolectados en Reino Unido por la Universidad de Minho y están en inglés.

### 3. Algoritmo

Utilizaremos un método llamado **Naive Bayes Multinomial con TF-IDF**, que ayudará al programa a aprender de los datos y después identificar si un mensaje es spam o no. Lo elegimos porque es un algoritmo de clasificación, lo que significa que sirve para separar los mensajes en dos grupos.

Funciona calculando la probabilidad de cada palabra. Por ejemplo, aprende que palabras como `FREE, WIN, PRIZE, CALL NOW` aparecen casi siempre en mensajes spam, y palabras como `hola, tarea, llego` aparecen en mensajes normales. Además, no necesita una computadora muy potente para funcionar.

### 4. Resultados esperados

Queremos que nuestro programa tenga buenos resultados al identificar los mensajes spam.

Buscamos conseguir:

- F1-score de spam: mínimo 0.90.
- Precisión de spam: mínimo 0.95.
- Recall de spam: mínimo 0.85.

No usamos solo la exactitud porque hay muchos más mensajes normales que spam. Lo más importante será evitar que un mensaje importante sea marcado por error como spam, pero también que no se nos escape un spam real.

### 5. Recursos de cómputo

Para realizar el proyecto utilizaremos una laptop o GitHub Codespaces, donde trabajaremos con Python y las herramientas necesarias para crear el programa. También revisaremos cuánto tiempo tarda en funcionar y cuánta memoria utiliza.

- Tiempo de entrenamiento: de 0.8 a 2.5 segundos.
- Memoria utilizada: aproximadamente de 120 a 200 MB.
- No necesita GPU, funciona con 1 núcleo de CPU.
- Para servir el programa, cualquier laptop normal es suficiente, ya que predecir un mensaje tarda menos de 0.05 segundos.

### 6. Riesgos iniciales

1. Los datos están desbalanceados, hay muchos más mensajes normales que spam, por lo que el programa podría aprender a decir que todo es normal.
2. La información de la base de datos está en inglés y es del año 2012, por lo que puede no incluir los tipos de spam que existen hoy en México, como los de paquetes o bancos.
3. Como el programa clasifica mensajes, podría equivocarse y marcar un mensaje importante, como un código de verificación, como spam.

### 7. Reparto de actividades

- **Rodolfo (A):** se encargará de organizar la información y crear el programa que identificará los mensajes spam.
- **Alex (B):** desarrollará la conexión del programa con la página web.
- **Daniel (C):** realizará las pruebas, ayudará a preparar el proyecto para su funcionamiento y apoyará con su publicación.

Los tres integrantes participaremos en la revisión del proyecto, la documentación y la presentación final.