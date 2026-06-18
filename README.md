# Evaluación de Frameworks para APIs en Python

Este repositorio contiene un proyecto destinado a **comparar y evaluar la seguridad de dos frameworks de desarrollo de APIs en Python: FastAPI y Django**. 
El objetivo es implementar APIs básicas en ambos frameworks, aplicar medidas de seguridad y realizar pruebas para determinar cuál ofrece un entorno más seguro y confiable.

## Objetivos

* Implementar APIs utilizando **FastAPI** y **Django**.
* Aplicar buenas prácticas de seguridad en cada API.
* Realizar pruebas de vulnerabilidad y ataques controlados para evaluar la resistencia de cada framework.
* Comparar los resultados y determinar cuál framework proporciona mayor seguridad y confiabilidad.

## Estructura del proyecto

```text
/framework-fastapi
    └── Código y configuración de la API en FastAPI
/framework-django
    └── Código y configuración de la API en Django
/tests
    └── Scripts y herramientas para pruebas de seguridad
/docs
    └── Documentación adicional y hallazgos
README.md
```

## Tecnologías utilizadas

* Python 3.x
* **FastAPI**
* **Django**
* Herramientas de seguridad y pruebas (por de determinar)

## Pasos del experimento

1. Implementar y configurar cada API.
2. Aplicar medidas de seguridad: autenticación, autorización, gestión de sesiones, cifrado y validación de entradas.
3. Ejecutar pruebas de penetración y vulnerabilidad.
4. Analizar resultados y documentar conclusiones.

## Arrancar APIs
Servicio
Comando de ejecución
Frontend: http-server -S -p 5501 -C "C:\Users\santi\Documents\gema_principal\15.-Master_UNIR\TFM_GBT\certs\localhost.pem" -K "C:\Users\santi\Documents\gema_principal\15.-Master_UNIR\TFM_GBT\certs\localhost-key.pem"

FastAPI: python -m uvicorn api.main:app --reload --ssl-certfile="C:\Users\santi\Documents\gema_principal\15.-Master_UNIR\TFM_GBT\certs\localhost.pem" --ssl-keyfile="C:\Users\santi\Documents\gema_principal\15.-Master_UNIR\TFM_GBT\certs\localhost-key.pem"

Django: python manage.py runserver_plus 8001 --cert-file "C:\Users\santi\Documents\gema_principal\15.-Master_UNIR\TFM_GBT\certs\localhost.pem" --key-file "C:\Users\santi\Documents\gema_principal\15.-Master_UNIR\TFM_GBT\certs\localhost-key.pem"

