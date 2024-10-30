# BACK-END-CRM

Este repositorio contiene el **Backend** de un sistema CRM diseñado para gestionar y dar soporte a clientes.

## Descripción del Proyecto

El backend de este CRM se encarga de procesar y gestionar los datos de clientes, proyectos y tareas, dispositivos, proporcionando una API para que el frontend pueda interactuar con la base de datos de manera segura y eficiente.

## Tecnologías Utilizadas

Este proyecto utiliza las siguientes tecnologías y herramientas:

- **Python**: Lenguaje de programación principal.
- **Django REST Framework**: Framework utilizado para construir APIs de manera rápida y eficiente.
- **PostgreSQL**: Sistema de gestión de bases de datos relacional.
- **JWT (JSON Web Tokens)**: Autenticación y autorización de usuarios.
  
## Instalación

Sigue estos pasos para configurar el proyecto en tu entorno local.

1. **Clona este repositorio**:
2. **Crea y activa un entorno virtual**:
    python -m venv env
    source env/bin/activate  # En Windows usa: env\Scripts\activate
3. **Instala las dependencias**:
    pip install -r requirements.txt
4. **Realiza las migraciones**:
    python manage.py migrate
5. **Inicia el servidor de desarrollo**:
    python manage.py runserver


