import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str = ".", directory: str = ".") -> str:
    final_path = ""
    try:
        abs_path = os.path.abspath(working_directory)
        final_path = os.path.normpath(os.path.join(abs_path, directory))
        if not os.path.isdir(final_path):
            return f'Error: "{directory}" is not a directory'
        valid_target_dir = os.path.commonpath([abs_path, final_path]) == abs_path
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: Unknown error occurred. \n {e}'
    else:
        response = []
        for file in os.listdir(final_path):
            file_path = os.path.join(final_path, str(file))
            response.append(f"- {file}: file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)}")
        return "\n".join(response)
