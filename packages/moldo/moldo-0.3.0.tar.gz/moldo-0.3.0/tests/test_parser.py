import pytest
import os
from moldo.compiler.parser import MoldoParser

def test_parse_print():
    parser = MoldoParser()
    code = '<mblock type="print">Hello, World!</mblock>'
    result = parser.parse(code)
    assert "print('Hello, World!')" in result

def test_parse_variable():
    parser = MoldoParser()
    code = '<mblock type="variable">x = 5</mblock>'
    result = parser.parse(code)
    assert 'x = 5' in result

def test_parse_math():
    parser = MoldoParser()
    code = '<mblock type="math">x + y</mblock>'
    result = parser.parse(code)
    assert 'x + y' in result

def test_parse_text():
    parser = MoldoParser()
    code = '<mblock type="text">Hello</mblock>'
    result = parser.parse(code)
    assert "print('Hello')" in result

def test_parse_list():
    parser = MoldoParser()
    code = '<mblock type="list">[1, 2, 3]</mblock>'
    result = parser.parse(code)
    assert '[1, 2, 3]' in result

def test_parse_condition():
    parser = MoldoParser()
    code = '<mblock type="condition">x > 5</mblock>'
    result = parser.parse(code)
    assert 'if x > 5:' in result

def test_parse_loop():
    parser = MoldoParser()
    code = '<mblock type="loop">i in range(5)</mblock>'
    result = parser.parse(code)
    assert 'for i in range(5):' in result

def test_parse_action():
    parser = MoldoParser()
    code = '<mblock type="action">print("Action")</mblock>'
    result = parser.parse(code)
    assert 'print("Action")' in result

def test_parse_import():
    parser = MoldoParser()
    test_module_path = os.path.join(os.path.dirname(__file__), 'test_module.py')
    code = f'<mblock type="import">{test_module_path}</mblock>'
    result = parser.parse(code)
    assert 'import sys' in result
    assert 'test_module' in result

def test_parse_invalid_xml():
    parser = MoldoParser()
    code = '<invalid>'
    with pytest.raises(ValueError):
        parser.parse(code)

def test_parse_unknown_block_type():
    parser = MoldoParser()
    code = '<mblock type="unknown">content</mblock>'
    result = parser.parse(code)
    assert '# Unknown block type: unknown' in result
    assert '# Content: content' in result

def test_parse_dictionary():
    parser = MoldoParser()
    code = '<mblock type="math">{"a": 1, "b": 2}</mblock>'
    result = parser.parse(code)
    assert '{"a": 1, "b": 2}' in result

def test_parse_dictionary_variable():
    parser = MoldoParser()
    code = '<mblock type="variable">my_dict = {"x": 10, "y": 20}</mblock>'
    result = parser.parse(code)
    assert 'my_dict = {"x": 10, "y": 20}' in result

def test_dictionary_demo():
    parser = MoldoParser()
    with open("examples/dictionary_demo.moldo", "r") as f:
        code = f.read()
    result = parser.parse(code)
    
    # Check key parts of the generated code
    assert 'student = {"name": "Alice", "age": 20, "grades": [85, 90, 95]}' in result
    assert 'name = student["name"]' in result
    assert 'student["subject"] = "Computer Science"' in result
    assert 'for key in student:' in result
    assert 'value = student[key]' in result
    assert 'print(f"{key}: {value}")' in result 