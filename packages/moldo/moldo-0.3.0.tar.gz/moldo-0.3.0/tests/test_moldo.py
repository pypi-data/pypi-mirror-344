import unittest
from pathlib import Path
from moldo.compiler.parser import MoldoParser
from moldo.decorators import moldo_function, BlockType, VisualBlock

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

    def test_visual_block_decorator(self):
        @moldo_function(
            reference_name="add_numbers",
            block_type=BlockType.MATH,
            description="Adds two numbers together",
            parameters={"a": int, "b": int},
            return_type=int,
            icon="add",
            color="blue",
            category="Math"
        )
        def add(a: int, b: int) -> int:
            return a + b

        self.assertEqual(add.reference_name, "add_numbers")
        self.assertEqual(add(1, 2), 3)
        self.assertIsInstance(add.visual_block, VisualBlock)
        self.assertEqual(add.visual_block.block_type, BlockType.MATH)
        self.assertEqual(add.visual_block.description, "Adds two numbers together")

    def test_educational_blocks(self):
        code = """
        <mblock math>2 + 2</mblock>
        <mblock text>Hello, World!</mblock>
        <mblock list>[1, 2, 3]</mblock>
        <mblock condition>x > 5</mblock>
        <mblock loop>i in range(5)</mblock>
        """
        python_code = self.parser.parse(code)
        self.assertIn("2 + 2", python_code)
        self.assertIn("Hello, World!", python_code)
        self.assertIn("[1, 2, 3]", python_code)
        self.assertIn("if x > 5:", python_code)
        self.assertIn("for i in range(5):", python_code)

    def test_block_attributes(self):
        code = """
        <mblock math color="blue" icon="add">2 + 2</mblock>
        <mblock text color="green" icon="text">Hello</mblock>
        """
        python_code = self.parser.parse(code)
        self.assertIn("2 + 2", python_code)
        self.assertIn("Hello", python_code)

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

    def test_error_handling(self):
        # Test invalid variable declaration
        with self.assertRaises(ValueError):
            code = "<mblock variable>invalid</mblock>"
            self.parser.parse(code)

        # Test unknown block type
        code = "<mblock unknown>content</mblock>"
        python_code = self.parser.parse(code)
        self.assertIn("# Unknown block type: unknown", python_code)

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

    def test_visual_block_metadata(self):
        @moldo_function(
            block_type=BlockType.MATH,
            description="Test function",
            parameters={"x": int},
            return_type=int,
            icon="test",
            color="red",
            category="Test"
        )
        def test_func(x: int) -> int:
            return x * 2

        block = test_func.visual_block
        self.assertEqual(block.name, "test_func")
        self.assertEqual(block.block_type, BlockType.MATH)
        self.assertEqual(block.description, "Test function")
        self.assertEqual(block.parameters, {"x": int})
        self.assertEqual(block.return_type, int)
        self.assertEqual(block.icon, "test")
        self.assertEqual(block.color, "red")
        self.assertEqual(block.category, "Test")

if __name__ == "__main__":
    unittest.main() 