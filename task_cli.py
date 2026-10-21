import sys

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


def cmd_add(args):
    print(f"[add] argumentos: {args}")


def cmd_update(args):
    print(f"[update] argumentos: {args}")


def cmd_delete(args):
    print(f"[delete] argumentos: {args}")


def cmd_mark_in_progress(args):
    print(f"[mark-in-progress] argumentos: {args}")


def cmd_mark_done(args):
    print(f"[mark-done] argumentos: {args}")


def cmd_list(args):
    print(f"[list] argumentos: {args}")


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

    handler(args)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
