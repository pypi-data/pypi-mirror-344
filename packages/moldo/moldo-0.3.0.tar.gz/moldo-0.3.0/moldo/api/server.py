from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from ..compiler.parser import MoldoParser
from ..decorators import MoldoFunction

app = FastAPI(title="Moldo API")
parser = MoldoParser()

class MoldoCode(BaseModel):
    code: str
    python_modules: Optional[Dict[str, str]] = None

class ExecutionResult(BaseModel):
    output: str
    error: Optional[str] = None

@app.post("/compile")
async def compile_code(moldo_code: MoldoCode) -> Dict[str, str]:
    """
    Compile Moldo code to Python.
    
    Args:
        moldo_code: The Moldo code to compile
        
    Returns:
        Dictionary containing the generated Python code
    """
    try:
        # Import any Python modules if provided
        if moldo_code.python_modules:
            for name, path in moldo_code.python_modules.items():
                parser.import_python_module(path)
        
        # Compile the Moldo code
        python_code = parser.parse(moldo_code.code)
        return {"python_code": python_code}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/execute")
async def execute_code(moldo_code: MoldoCode) -> ExecutionResult:
    """
    Execute Moldo code and return the result.
    
    Args:
        moldo_code: The Moldo code to execute
        
    Returns:
        Execution result containing output and any errors
    """
    try:
        # Import any Python modules if provided
        if moldo_code.python_modules:
            for name, path in moldo_code.python_modules.items():
                parser.import_python_module(path)
        
        # Compile and execute the code
        python_code = parser.parse(moldo_code.code)
        
        # Create a new namespace for execution
        namespace = {}
        
        # Execute the code
        exec(python_code, namespace)
        
        # Capture any output
        output = namespace.get('__output__', '')
        return ExecutionResult(output=output)
    except Exception as e:
        return ExecutionResult(output="", error=str(e))

@app.get("/functions")
async def get_available_functions() -> Dict[str, List[str]]:
    """
    Get a list of all available Moldo functions.
    
    Returns:
        Dictionary containing the list of available functions
    """
    return {"functions": parser.get_available_functions()}

@app.post("/functions/{name}")
async def execute_function(name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a specific Moldo function.
    
    Args:
        name: The name of the function to execute
        args: The arguments to pass to the function
        
    Returns:
        Dictionary containing the function result
    """
    try:
        result = parser.execute_function(name, **args)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
