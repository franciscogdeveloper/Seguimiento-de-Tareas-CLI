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

    # El id es el mayor existente + 1 (o 1 si no hay tareas)
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


# Devuelve las tareas; si se indica un estado, solo las de ese estado
def list_tasks(status=None):
    if status is not None and status not in VALID_STATUSES:
        raise TaskError(f"Estado inválido '{status}'. Usa: {', '.join(VALID_STATUSES)}.")

    tasks = storage.load_tasks()
    if status is None:
        return tasks

    # Filtra las tareas que tienen el estado pedido
    return [task for task in tasks if task["status"] == status]


# Busca una tarea por id; si no existe, lanza TaskError
def find_task(tasks, task_id):
    # Devuelve la primera coincidencia, o None si no hay ninguna
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        raise TaskError(f"No existe una tarea con ID {task_id}.")
    return task


# Cambia la descripción de una tarea y actualiza su fecha de modificación
def update_task(task_id, description):
    description = description.strip()
    if not description:
        raise TaskError("La descripción no puede estar vacía.")

    tasks = storage.load_tasks()
    task = find_task(tasks, task_id)

    # Apunta al diccionario dentro de la lista, así que el cambio queda en tasks
    task["description"] = description
    task["updatedAt"] = now()

    storage.save_tasks(tasks)
    return task


# Elimina una tarea por id y devuelve la tarea eliminada
def delete_task(task_id):
    tasks = storage.load_tasks()
    task = find_task(tasks, task_id)

    tasks.remove(task)
    storage.save_tasks(tasks)
    return task


# Cambia el estado de una tarea
def set_status(task_id, status):
    if status not in VALID_STATUSES:
        raise TaskError(f"Estado inválido '{status}'. Usa: {', '.join(VALID_STATUSES)}.")

    tasks = storage.load_tasks()
    task = find_task(tasks, task_id)

    task["status"] = status
    task["updatedAt"] = now()

    storage.save_tasks(tasks)
    return task
