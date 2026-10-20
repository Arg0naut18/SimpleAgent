from config import MAX_CHARS
import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Get the content of a file in a specified file path relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file relative to the working directory.",
                },
            },
        },
    },
}

def get_file_content(file_path: str, working_directory: str = ".") -> str:
    final_file_path = ""
    try:
        work_dir_abs_path = os.path.abspath(working_directory)
        if file_path.startswith("/"):
            if os.path.commonpath([work_dir_abs_path, file_path]) != work_dir_abs_path:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            else:
                final_file_path = file_path
        else:
            final_file_path = os.path.normpath(os.path.join(work_dir_abs_path, file_path))
            if os.path.commonpath([work_dir_abs_path, final_file_path]) != work_dir_abs_path:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            if not os.path.isfile(final_file_path):
                return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as e:
        return f'Error: Unknown error occurred.\n{e}'
    else:
        content = ""
        with open(final_file_path, 'r') as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
