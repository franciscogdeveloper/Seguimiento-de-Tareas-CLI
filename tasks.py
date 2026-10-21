# Fecha y hora actual
from datetime import datetime

# Lectura y escritura del archivo de tareas
import storage

# Estados válidos de una tarea
VALID_STATUSES = ("todo", "in-progress", "done")


# Error de la lógica de tareas
class TaskError(Exception):
    pass


# Devuelve la fecha y hora actual en formato ISO 8601, sin microsegundos
def now():
    return datetime.now().isoformat(timespec="seconds")


# Crea una tarea nueva con estado "todo", la guarda y la devuelve
def add_task(description):
    # Quita espacios al inicio y al final; rechaza descripciones vacías
    description = description.strip()
    if not description:
        raise TaskError("La descripción no puede estar vacía.")

    tasks = storage.load_tasks()

    # El id es el mayor existente + 1, así no se repite aunque se borren tareas
    new_id = max((task["id"] for task in tasks), default=0) + 1

    # Misma fecha para creación y última actualización
    timestamp = now()
    task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": timestamp,
        "updatedAt": timestamp,
    }

    tasks.append(task)
    storage.save_tasks(tasks)
    return task
