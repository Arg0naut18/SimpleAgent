import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run the python file in a specified file path relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "description": "Arguments needed to pass to the python file to run. Defaults to None."
                }
            },
        },
    },
}

def run_python_file(
    file_path: str, args: list[str] | None = None, working_directory: str = "."
) -> str:
    final_file_path = ""
    work_dir_abs_path = ""
    try:
        work_dir_abs_path = os.path.abspath(working_directory)
        if file_path.startswith("/"):
            if os.path.commonpath([work_dir_abs_path, file_path]) != work_dir_abs_path:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            else:
                final_file_path = file_path
        else:
            final_file_path = os.path.normpath(os.path.join(work_dir_abs_path, file_path))
            if os.path.commonpath([work_dir_abs_path, final_file_path]) != work_dir_abs_path:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            if not os.path.isfile(final_file_path):
                return f'Error: "{file_path}" does not exist or is not a regular file'
            if not final_file_path.endswith(".py"):
                return f'Error: "{file_path}" is not a Python file'
    except Exception as e:
        return f'Error: Unknown error occurred during file verification.\n{e}\nPython script not executed.'
    else:
        try:
            command = ["python", final_file_path]
            if args:
                command.extend(args)
            result = subprocess.run(command, text=True, capture_output=True, cwd=work_dir_abs_path, timeout=30)
            if result.returncode != 0:
                return f"Process exited with code {result.returncode}"
            if not (result.stderr or result.stdout):
                return "No output produced"
            return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        except Exception as e:
            return f'Error: Unknown error occurred during running the python file.\n{e}'
