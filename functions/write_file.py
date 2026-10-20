import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes the specified content to the file in a specified file path relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of the file relative to the working directory.",
                },
                "content": {
                    "type": "string",
                    "description": "Content that has to be written in the specified file path. This will overwrite the existing contents of the file if it exists already."
                }
            },
        },
    },
}

def write_file(file_path: str, content: str, working_directory: str = ".") -> str:
    final_file_path = ""
    try:
        work_dir_abs_path = os.path.abspath(working_directory)
        if file_path.startswith("/"):
            if os.path.commonpath([work_dir_abs_path, file_path]) != work_dir_abs_path:
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            else:
                final_file_path = file_path
        else:
            final_file_path = os.path.normpath(os.path.join(work_dir_abs_path, file_path))
            if os.path.isdir(final_file_path):
                return f'Error: Cannot write to "{file_path}" as it is a directory'
    except Exception as e:
        return f'Error: Unknown error occurred.\n{e}'
    else:
        try:
            os.makedirs(final_file_path.rsplit("/", 1)[0], exist_ok=True)
            with open(final_file_path, 'w') as f:
                f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f'Error: Unknown error occurred.\n{e}'
