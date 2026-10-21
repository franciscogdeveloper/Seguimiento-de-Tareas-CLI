# Convierte listas y diccionarios de Python a texto JSON, y al revés
import json

# Funciones del sistema operativo, como reemplazar archivos
import os

# Manejo de rutas de archivos
from pathlib import Path

TASKS_FILE = Path("tasks.json")

# Guarda la lista de tareas en el archivo JSON
def save_tasks(tasks):
    # Se guarda en un archivo temporal
    temp_file = TASKS_FILE.with_suffix(".tmp")

    # Escribe las tareas en el archivo temporal con formato legible y acentos
    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2, ensure_ascii=False)

    # Reemplaza el archivo original por el temporal en un solo paso,
    # evitando que quede corrupto si el programa se interrumpe al escribir
    os.replace(temp_file, TASKS_FILE)

# Error al leer el archivo de tareas
class StorageError(Exception):
    pass


# Devuelve la lista de tareas; si el archivo no existe, lo crea vacío
def load_tasks():
    if not TASKS_FILE.exists():
        save_tasks([])
        return []

    # Lee el archivo; si el contenido no es JSON válido, lanza StorageError
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as file:
            tasks = json.load(file)
    except json.JSONDecodeError:
        raise StorageError(f"El archivo {TASKS_FILE} está dañado o no es un JSON válido.")

    # El archivo debe contener una lista de tareas
    if not isinstance(tasks, list):
        raise StorageError(f"El archivo {TASKS_FILE} no contiene una lista de tareas.")

    return tasks
