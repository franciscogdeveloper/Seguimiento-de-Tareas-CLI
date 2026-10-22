import sys
import tasks
import storage

USAGE = """\
Uso: task-cli <comando> [argumentos]

Comandos:
  add "<descripción>"             Agrega una tarea nueva
  update <id> "<descripción>"     Cambia la descripción de una tarea
  delete <id>                     Elimina una tarea
  mark-in-progress <id>           Marca una tarea como en progreso
  mark-done <id>                  Marca una tarea como completada
  list [todo|in-progress|done]    Lista las tareas (filtro opcional)
  help                            Muestra esta ayuda
"""


# Agrega una tarea: task-cli add "<descripción>"
def cmd_add(args):
    if len(args) != 1:
        raise tasks.TaskError('Uso: task-cli add "<descripción>"')

    task = tasks.add_task(args[0])
    print(f"Tarea agregada correctamente (ID: {task['id']})")


def cmd_update(args):
    print(f"[update] argumentos: {args}")


def cmd_delete(args):
    print(f"[delete] argumentos: {args}")


def cmd_mark_in_progress(args):
    print(f"[mark-in-progress] argumentos: {args}")


def cmd_mark_done(args):
    print(f"[mark-done] argumentos: {args}")


# Lista las tareas
def cmd_list(args):
    if len(args) > 1:
        raise tasks.TaskError("Uso: task-cli list [todo|in-progress|done]")

    # Sin argumento muestra todas; con argumento filtra por estado
    status = args[0] if args else None
    task_list = tasks.list_tasks(status)

    if not task_list:
        print("No hay tareas para mostrar.")
        return

    # Una tarea por línea, con el estado alineado en 11 caracteres
    for task in task_list:
        print(f"[{task['id']}] {task['status']:<11}  {task['description']}")


def cmd_help(args):
    print(USAGE)


COMMANDS = {
    "add": cmd_add,
    "update": cmd_update,
    "delete": cmd_delete,
    "mark-in-progress": cmd_mark_in_progress,
    "mark-done": cmd_mark_done,
    "list": cmd_list,
    "help": cmd_help,
}


def main(argv):
    if not argv:
        print(USAGE, file=sys.stderr)
        return 1
    
    command, *args = argv
    handler = COMMANDS.get(command)
    if handler is None:
        print(f"Error: comando desconocido '{command}'.", file=sys.stderr)
        print("Escribe 'task-cli help' para ver los comandos disponibles.", file=sys.stderr)
        return 1

    # Muestra los errores esperados como un mensaje limpio, sin traceback
    try:
        handler(args)
    except (tasks.TaskError, storage.StorageError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
