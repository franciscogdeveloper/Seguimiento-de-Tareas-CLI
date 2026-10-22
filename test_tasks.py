import os
import tempfile
import unittest
import io
from contextlib import redirect_stderr, redirect_stdout

import storage
import tasks
from task_cli import main


# Base para los tests: cada test corre en una carpeta temporal vacía
class TempDirTestCase(unittest.TestCase):
    # Se ejecuta antes de cada test
    def setUp(self):
        self.original_dir = os.getcwd()
        self.temp_dir = tempfile.TemporaryDirectory()
        os.chdir(self.temp_dir.name)

    # Se ejecuta después de cada test: vuelve a la carpeta original y borra la temporal
    def tearDown(self):
        os.chdir(self.original_dir)
        self.temp_dir.cleanup()


# Tests de la lógica en tasks.py
class TestTasks(TempDirTestCase):
    # Crea tasks.json vacío si no existe
    def test_load_tasks_creates_file_if_missing(self):
        self.assertEqual(storage.load_tasks(), [])
        self.assertTrue(storage.TASKS_FILE.exists())

    # Guarda la tarea con id, descripción, estado "todo" y fechas iguales
    def test_add_task_creates_task_with_all_properties(self):
        task = tasks.add_task("Comprar pan")

        self.assertEqual(task["id"], 1)
        self.assertEqual(task["description"], "Comprar pan")
        self.assertEqual(task["status"], "todo")
        self.assertEqual(task["createdAt"], task["updatedAt"])
        self.assertEqual(storage.load_tasks(), [task])

    # No acepta descripciones vacías o con solo espacios
    def test_add_task_rejects_empty_description(self):
        with self.assertRaises(tasks.TaskError):
            tasks.add_task("   ")

    # Devuelve todas las tareas o solo las del estado pedido
    def test_list_tasks_filters_by_status(self):
        tasks.add_task("A")
        tasks.add_task("B")
        tasks.set_status(2, "done")

        self.assertEqual(len(tasks.list_tasks()), 2)
        self.assertEqual([task["id"] for task in tasks.list_tasks("done")], [2])
        self.assertEqual(tasks.list_tasks("in-progress"), [])

    # No acepta estados que no existen
    def test_list_tasks_rejects_invalid_status(self):
        with self.assertRaises(tasks.TaskError):
            tasks.list_tasks("otro")

    # Cambia la descripción sin modificar la fecha de creación
    def test_update_task_changes_description_and_keeps_created_at(self):
        created = tasks.add_task("Comprar pan")
        updated = tasks.update_task(1, "Comprar pan y leche")

        self.assertEqual(updated["description"], "Comprar pan y leche")
        self.assertEqual(updated["createdAt"], created["createdAt"])

    # Elimina solo la tarea indicada
    def test_delete_task_removes_it(self):
        tasks.add_task("A")
        tasks.add_task("B")
        tasks.delete_task(1)

        self.assertEqual([task["id"] for task in tasks.list_tasks()], [2])

    # Cambia el estado de la tarea
    def test_set_status_changes_status(self):
        tasks.add_task("A")
        tasks.set_status(1, "in-progress")

        self.assertEqual(tasks.list_tasks()[0]["status"], "in-progress")

    # Update, delete y set_status fallan si el id no existe
    def test_missing_id_raises_error(self):
        with self.assertRaises(tasks.TaskError):
            tasks.update_task(99, "Hola")
        with self.assertRaises(tasks.TaskError):
            tasks.delete_task(99)
        with self.assertRaises(tasks.TaskError):
            tasks.set_status(99, "done")

    # Falla con un error claro si el JSON está dañado
    def test_corrupted_file_raises_storage_error(self):
        storage.TASKS_FILE.write_text("basura", encoding="utf-8")

        with self.assertRaises(storage.StorageError):
            storage.load_tasks()


# Tests de la CLI en task_cli.py
class TestCli(TempDirTestCase):
    # Ejecuta la CLI y devuelve el código de salida y lo que imprimió
    def run_cli(self, *argv):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = main(list(argv))
        return code, stdout.getvalue(), stderr.getvalue()

    # Muestra el id de la tarea creada y termina con código 0
    def test_add_prints_new_id(self):
        code, out, _ = self.run_cli("add", "Comprar pan")

        self.assertEqual(code, 0)
        self.assertIn("ID: 1", out)

    # Muestra las tareas guardadas
    def test_list_shows_tasks(self):
        self.run_cli("add", "Comprar pan")
        code, out, _ = self.run_cli("list")

        self.assertEqual(code, 0)
        self.assertIn("Comprar pan", out)

    # Las entradas inválidas terminan con código 1 y un mensaje en stderr
    def test_invalid_input_returns_error_code(self):
        cases = [
            [],
            ["volar"],
            ["add"],
            ["update", "abc", "Hola"],
            ["delete", "99"],
            ["list", "otro"],
        ]
        for argv in cases:
            # Indica cuál caso falló, si alguno falla
            with self.subTest(argv=argv):
                code, _, err = self.run_cli(*argv)
                self.assertEqual(code, 1)
                self.assertTrue(err)

    # Un JSON dañado se informa como error, sin traceback
    def test_corrupted_file_returns_error_code(self):
        storage.TASKS_FILE.write_text("basura", encoding="utf-8")
        code, _, err = self.run_cli("list")

        self.assertEqual(code, 1)
        self.assertIn("dañado", err)
