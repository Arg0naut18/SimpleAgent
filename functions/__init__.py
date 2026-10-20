import json
from collections.abc import Callable
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.write_file import schema_write_file, write_file
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")
    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    if function_name in function_map:
        content = function_map[function_name](**function_args)
    else:
        content = f"Error: Unknown function: {function_name}"
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": content
    }
