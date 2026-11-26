"""Regression checks using synthetic fixtures only; no original data required."""
import json
import unittest
from pathlib import Path

NOTEBOOK = Path(__file__).resolve().parents[1] / 'notebooks' / 'student-performance-kmeans-clustering.ipynb'
CELLS = json.loads(NOTEBOOK.read_text(encoding='utf-8'))['cells']

def source(index):
    return ''.join(CELLS[index]['source'])

def run(namespace, *indices):
    for i in indices:
        exec(compile(source(i), f'{NOTEBOOK.name}:cell-{i}', 'exec'), namespace)

class NotebookTests(unittest.TestCase):
    def test_python_cells_compile(self):
        for i, cell in enumerate(CELLS):
            if cell['cell_type'] != 'code':
                continue
            # Notebook magics are handled by IPython, not the Python parser.
            code = '\n'.join(line for line in source(i).splitlines() if not line.lstrip().startswith(('%', '!')))
            with self.subTest(cell=i):
                compile(code, f'{NOTEBOOK.name}:cell-{i}', 'exec')

    def test_pie_chart_definition_compiles(self):
        import ast
        tree = ast.parse(source(13))
        self.assertEqual(tree.body[0].name, 'plot_pie_chart')

if __name__ == '__main__':
    unittest.main()
