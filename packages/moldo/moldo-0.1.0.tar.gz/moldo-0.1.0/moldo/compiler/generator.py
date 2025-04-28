from typing import Any, Dict, List
from antlr4 import ParserRuleContext

class PythonGenerator:
    def __init__(self):
        self.block_handlers: Dict[str, callable] = {
            'variable': self._handle_variable,
            'input': self._handle_input,
            'print': self._handle_print,
            'if': self._handle_if,
            'for': self._handle_for,
            'while': self._handle_while,
            'function': self._handle_function,
            'call': self._handle_function_call,
        }

    def generate(self, tree: ParserRuleContext) -> str:
        """
        Generate Python code from a Moldo parse tree.
        
        Args:
            tree: The ANTLR parse tree
            
        Returns:
            Generated Python code
        """
        return self._visit_program(tree)

    def _visit_program(self, node: ParserRuleContext) -> str:
        """Visit the program node and generate Python code."""
        code = []
        for child in node.getChildren():
            if isinstance(child, ParserRuleContext):
                code.append(self._visit_block(child))
        return '\n'.join(code)

    def _visit_block(self, node: ParserRuleContext) -> str:
        """Visit a block node and generate Python code."""
        if hasattr(node, 'mblock'):
            block_type = node.block_type().getText()
            handler = self.block_handlers.get(block_type)
            if handler:
                return handler(node)
            return self._handle_unknown_block(node)
        elif hasattr(node, 'python_block'):
            return node.PYTHON_CODE().getText()
        return ''

    def _handle_variable(self, node: ParserRuleContext) -> str:
        """Handle variable declaration and assignment."""
        content = node.block_content().getText().strip()
        name, value = content.split('=', 1)
        return f"{name.strip()} = {value.strip()}"

    def _handle_input(self, node: ParserRuleContext) -> str:
        """Handle input block."""
        content = node.block_content().getText().strip()
        return f"{content} = input()"

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

    def _handle_unknown_block(self, node: ParserRuleContext) -> str:
        """Handle unknown block types."""
        block_type = node.block_type().getText()
        content = node.block_content().getText().strip()
        return f"# Unknown block type: {block_type}\n# Content: {content}"
