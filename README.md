# Seguimiento de Tareas CLI

Aplicación de línea de comandos para registrar y gestionar tu lista de tareas.
Las tareas se guardan en un archivo `tasks.json` en el directorio actual, que se crea automáticamente si no existe.

Hecha solo con la librería estándar de Python (sin dependencias externas), como parte del
[proyecto Task Tracker de roadmap.sh](https://roadmap.sh/projects/task-tracker).

## Requisitos

- Python 3 (probado con Python 3.15)

## Uso

Ejecuta los comandos desde la carpeta del proyecto:

```bash
# Agregar una tarea
python task_cli.py add "Comprar pan"

# Actualizar la descripción de una tarea
python task_cli.py update 1 "Comprar pan y leche"

# Eliminar una tarea
python task_cli.py delete 1

# Marcar una tarea como en progreso o completada
python task_cli.py mark-in-progress 1
python task_cli.py mark-done 1

# Listar todas las tareas
python task_cli.py list

# Listar tareas por estado
python task_cli.py list todo
python task_cli.py list in-progress
python task_cli.py list done

# Mostrar la ayuda
python task_cli.py help
```

Si la entrada no es válida (comando desconocido, argumentos faltantes, ID no numérico o inexistente,
descripción vacía o archivo JSON dañado), el programa muestra un mensaje de error claro y termina con código `1`.

## Propiedades de una tarea

Cada tarea se guarda en `tasks.json` con estas propiedades:

```json
{
  "id": 1,
  "description": "Comprar pan",
  "status": "todo",
  "createdAt": "2026-10-21T20:56:38",
  "updatedAt": "2026-10-21T20:56:38"
}
```

| Propiedad     | Descripción                                        |
|---------------|----------------------------------------------------|
| `id`          | Identificador único de la tarea                    |
| `description` | Descripción breve                                  |
| `status`      | Estado: `todo`, `in-progress` o `done`             |
| `createdAt`   | Fecha y hora de creación (ISO 8601)                |
| `updatedAt`   | Fecha y hora de la última modificación (ISO 8601)  |

## Tests

```bash
python -m unittest -v
```

Los tests corren en una carpeta temporal, así que no modifican tu `tasks.json`.

## Estructura del proyecto

```
task_cli.py     # Interfaz de línea de comandos: lee los argumentos y muestra los resultados
tasks.py        # Lógica de las tareas: agregar, listar, actualizar, eliminar y cambiar estado
storage.py      # Lectura y escritura del archivo tasks.json
test_tasks.py   # Tests de la lógica y de la CLI
```
