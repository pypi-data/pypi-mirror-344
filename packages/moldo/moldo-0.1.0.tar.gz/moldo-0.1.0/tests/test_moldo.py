import unittest
from pathlib import Path
from moldo.compiler.parser import MoldoParser
from moldo.decorators import moldo_function

class TestMoldo(unittest.TestCase):
    def setUp(self):
        self.parser = MoldoParser()

    def test_basic_blocks(self):
        code = """
        <mblock variable>x = 10</mblock>
        <mblock print>x</mblock>
        """
        python_code = self.parser.parse(code)
        self.assertIn("x = 10", python_code)
        self.assertIn("print(x)", python_code)

    def test_function_decorator(self):
        @moldo_function(reference_name="test_func")
        def test_function(a, b):
            return a + b

        self.assertEqual(test_function.reference_name, "test_func")
        self.assertEqual(test_function(1, 2), 3)

    def test_import_and_execute(self):
        # Import the example module
        self.parser.import_python_module("examples/math_functions.py")
        
        # Verify functions are available
        functions = self.parser.get_available_functions()
        self.assertIn("add", functions)
        self.assertIn("subtract", functions)
        
        # Test function execution
        result = self.parser.execute_function("add", 5, 3)
        self.assertEqual(result, 8)

    def test_full_program(self):
        # Read and parse the example program
        with open("examples/calculator.moldo", "r") as f:
            code = f.read()
        
        # Import required modules
        self.parser.import_python_module("examples/math_functions.py")
        
        # Compile and verify the output
        python_code = self.parser.parse(code)
        self.assertIn("num1 = float(input())", python_code)
        self.assertIn("add(num1, num2)", python_code)

if __name__ == "__main__":
    unittest.main() 