from functools import wraps
from typing import Any, Callable, Optional, Dict, List, Type
from enum import Enum

class BlockType(Enum):
    """Types of visual blocks that can be created."""
    VARIABLE = "variable"
    FUNCTION = "function"
    CONDITION = "condition"
    LOOP = "loop"
    ACTION = "action"
    MATH = "math"
    TEXT = "text"
    LIST = "list"

class VisualBlock:
    """Represents a visual block in the Moldo editor."""
    def __init__(
        self,
        name: str,
        block_type: BlockType,
        description: str,
        parameters: Dict[str, Type],
        return_type: Optional[Type] = None,
        icon: Optional[str] = None,
        color: Optional[str] = None,
        category: Optional[str] = None
    ):
        self.name = name
        self.block_type = block_type
        self.description = description
        self.parameters = parameters
        self.return_type = return_type
        self.icon = icon
        self.color = color
        self.category = category

class MoldoFunction:
    def __init__(
        self,
        func: Callable,
        reference_name: Optional[str] = None,
        visual_block: Optional[VisualBlock] = None
    ):
        self.func = func
        self.reference_name = reference_name or func.__name__
        self.visual_block = visual_block
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
        self.__module__ = func.__module__

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)

def moldo_function(
    reference_name: Optional[str] = None,
    block_type: Optional[BlockType] = None,
    description: Optional[str] = None,
    parameters: Optional[Dict[str, Type]] = None,
    return_type: Optional[Type] = None,
    icon: Optional[str] = None,
    color: Optional[str] = None,
    category: Optional[str] = None
) -> Callable:
    """
    Decorator to mark a Python function as usable in Moldo.
    
    Args:
        reference_name: Optional name to use when referencing this function in Moldo.
                       If not provided, the function's name will be used.
        block_type: The type of visual block this function represents.
        description: Description of what the function does.
        parameters: Dictionary mapping parameter names to their types.
        return_type: The return type of the function.
        icon: Optional icon for the visual block.
        color: Optional color for the visual block.
        category: Optional category for organizing blocks.
    
    Example:
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
    """
    def decorator(func: Callable) -> MoldoFunction:
        visual_block = None
        if block_type is not None:
            visual_block = VisualBlock(
                name=reference_name or func.__name__,
                block_type=block_type,
                description=description or func.__doc__ or "",
                parameters=parameters or {},
                return_type=return_type,
                icon=icon,
                color=color,
                category=category
            )
        return MoldoFunction(func, reference_name, visual_block)
    return decorator
