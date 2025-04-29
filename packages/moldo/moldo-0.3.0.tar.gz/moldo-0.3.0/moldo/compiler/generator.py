from typing import Any, Dict, List, Optional
from antlr4 import ParserRuleContext
import xml.etree.ElementTree as ET

class PythonGenerator:
    def __init__(self):
        self.block_handlers: Dict[str, callable] = {
            # Basic blocks
            'variable': self._handle_variable,
            'input': self._handle_input,
            'print': self._handle_print,
            'if': self._handle_if,
            'for': self._handle_for,
            'while': self._handle_while,
            'function': self._handle_function,
            'call': self._handle_function_call,
            'import': self._handle_import,
            
            # Educational blocks
            'math': self._handle_math,
            'text': self._handle_text,
            'list': self._handle_list,
            'loop': self._handle_loop,
            'condition': self._handle_condition,
            'action': self._handle_action,
        }
        
        self.imported_modules: Dict[str, Any] = {}
        self.imported_functions: Dict[str, callable] = {}

    def generate(self, tree: ParserRuleContext) -> str:
        """
        Generate Python code from a Moldo parse tree.
        
        Args:
            tree: The ANTLR parse tree
            
        Returns:
            Generated Python code
        """
        try:
            return self._visit_program(tree)
        except Exception as e:
            raise ValueError(f"Error generating Python code: {str(e)}")

    def _visit_program(self, node: ParserRuleContext) -> str:
        """Visit the program node and generate Python code."""
        code = []
        imports = []
        
        # First pass: collect imports
        for child in node.getChildren():
            if isinstance(child, ParserRuleContext):
                if hasattr(child, 'mblock') and child.block_type().getText() == 'import':
                    imports.append(self._handle_import(child))
        
        # Add imports at the start
        if imports:
            code.extend(imports)
            code.append('')
        
        # Second pass: generate code
        for child in node.getChildren():
            if isinstance(child, ParserRuleContext):
                if not (hasattr(child, 'mblock') and child.block_type().getText() == 'import'):
                    code.append(self._visit_block(child))
        
        return '\n'.join(code)

    def _visit_block(self, node: ParserRuleContext) -> str:
        """Visit a block node and generate Python code."""
        try:
            if hasattr(node, 'mblock'):
                block_type = node.block_type().getText()
                handler = self.block_handlers.get(block_type)
                if handler:
                    return handler(node)
                return self._handle_unknown_block(node)
            elif hasattr(node, 'python_block'):
                return node.PYTHON_CODE().getText()
            return ''
        except Exception as e:
            raise ValueError(f"Error processing block: {str(e)}")

    def _handle_variable(self, node: ParserRuleContext) -> str:
        """Handle variable declaration and assignment."""
        content = node.block_content().getText().strip()
        try:
            name, value = content.split('=', 1)
            return f"{name.strip()} = {value.strip()}"
        except ValueError:
            raise ValueError(f"Invalid variable declaration: {content}")

    def _handle_input(self, node: ParserRuleContext) -> str:
        """Handle input block."""
        content = node.block_content().getText().strip()
        prompt = f'"{content}"' if content else '""'
        return f"input({prompt})"

    def _handle_print(self, node: ParserRuleContext) -> str:
        """Handle print block."""
        content = node.block_content().getText().strip()
        return f"print({content})"

    def _handle_if(self, node: ParserRuleContext) -> str:
        """Handle if block."""
        condition = node.block_content().getText().strip()
        return f"if {condition}:"

    def _handle_for(self, node: ParserRuleContext) -> str:
        """Handle for loop block."""
        content = node.block_content().getText().strip()
        return f"for {content}:"

    def _handle_while(self, node: ParserRuleContext) -> str:
        """Handle while loop block."""
        condition = node.block_content().getText().strip()
        return f"while {condition}:"

    def _handle_function(self, node: ParserRuleContext) -> str:
        """Handle function definition block."""
        content = node.block_content().getText().strip()
        return f"def {content}:"

    def _handle_function_call(self, node: ParserRuleContext) -> str:
        """Handle function call block."""
        content = node.block_content().getText().strip()
        return f"{content}"

    def _handle_import(self, node: ParserRuleContext) -> str:
        """Handle import block."""
        content = node.block_content().getText().strip()
        return f"import {content}"

    def _handle_math(self, node: ParserRuleContext) -> str:
        """Handle math operations block."""
        content = node.block_content().getText().strip()
        return f"{content}"

    def _handle_text(self, node: ParserRuleContext) -> str:
        """Handle text operations block."""
        content = node.block_content().getText().strip()
        return f"{content}"

    def _handle_list(self, node: ParserRuleContext) -> str:
        """Handle list operations block."""
        content = node.block_content().getText().strip()
        return f"{content}"

    def _handle_loop(self, node: ParserRuleContext) -> str:
        """Handle generic loop block."""
        content = node.block_content().getText().strip()
        return f"for {content}:"

    def _handle_condition(self, node: ParserRuleContext) -> str:
        """Handle condition block."""
        content = node.block_content().getText().strip()
        return f"if {content}:"

    def _handle_action(self, node: ParserRuleContext) -> str:
        """Handle action block."""
        content = node.block_content().getText().strip()
        return f"{content}"

    def _handle_unknown_block(self, node: ParserRuleContext) -> str:
        """Handle unknown block types."""
        block_type = node.block_type().getText()
        content = node.block_content().getText().strip()
        return f"# Unknown block type: {block_type}\n# Content: {content}"
