# Moldo - Visual Programming Language

Moldo is a visual programming language that compiles to Python. It provides a block-based interface for creating programs while maintaining the power and flexibility of Python.

## Features

- Visual block-based programming interface
- Compiles to Python code
- Supports basic programming constructs (variables, input, loops)
- Can import and use Python functions through decorators
- Real-time code execution
- File saving and loading

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/moldo.git
cd moldo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Generate ANTLR files:
```bash
antlr4 -Dlanguage=Python3 moldo/compiler/grammar.py
```

## Usage

### Starting the API Server

```bash
uvicorn moldo.api.server:app --reload
```

### Using the Visual Editor

1. Open the visual editor in your browser
2. Drag and drop blocks to create your program
3. Click "Run" to execute the code
4. Use "Save" to save your program as a Moldo file

### Python Integration

To make Python functions available in Moldo, use the `@moldo_function` decorator:

```python
from moldo.decorators import moldo_function

@moldo_function(reference_name="add_numbers")
def add(a: int, b: int) -> int:
    return a + b
```

## Project Structure

- `moldo/compiler/` - Contains the Moldo language compiler
  - `grammar.py` - ANTLR grammar definition
  - `parser.py` - Parser implementation
  - `generator.py` - Python code generator
- `moldo/editor/` - Visual editor implementation
- `moldo/api/` - REST API server
- `moldo/decorators.py` - Python integration decorators

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 