"""
Wrote by Google Bard and modified by kensoi :)
"""

import os


def clear_env(file_data: str):
    """
    clears file
    """
    for line in file_data.split("\n"):
        if line == "" or "=" not in line or line.startswith("#"):
            continue

        if "#" in line:
            yield line[:line.find("#")]
            continue

        yield tuple(line.split("=", 1))

def convert_env_to_json(path_to_file: str) -> str:
    """
    Конвертирует файл в формате .env в файл в формате .json.

    Args:
        path: Путь к файлу в формате .env.

    """

    path_to_new_file = f"{path_to_file[:path_to_file.rfind('.')]}.json"

    with open(path_to_file, "r", encoding="utf-8") as file:
        env_data = file.read()

    parsed_data = list(clear_env(env_data))
    with open(path_to_new_file, "r+", encoding="utf-8") as new_file:
        content = "{"
        for index, (key, value) in enumerate(parsed_data):
            content += f"\n\t\"{key}\":\"{value}\""

            if index + 1 != len(parsed_data):
                content += ","

        content += "\n}"

        new_file.write(content)

    return path_to_new_file

if __name__ == "__main__":
    convert_env_to_json(os.path.join(os.getcwd(), ".env"))
