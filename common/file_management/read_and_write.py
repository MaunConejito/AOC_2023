from os import path, listdir, makedirs

INPUT_REL_PATH = '..\\data\\input\\'
OUTPUT_REL_PATH = '..\\data\\output\\'

def get_input_file_names(script_path: str) -> list[str]:
    dir = path.join(path.dirname(script_path), INPUT_REL_PATH)
    return [f for f in listdir(dir) if path.isfile(path.join(dir, f))]

def read_data(script_path: str, file_name: str) -> str:
    return get_file_content(path.join(path.dirname(script_path), INPUT_REL_PATH, file_name))

def write_data(script_path: str, file_name: str, content: object) -> str:
    return write_file(path.join(path.dirname(script_path), OUTPUT_REL_PATH, file_name), str(content))

def get_file_content(absolute_path: str) -> str:
    with open(absolute_path) as file:
        return file.read()

def write_file(absolute_path: str, content: str) -> str:
    directory = path.dirname(absolute_path)
    if not path.exists(directory):
        makedirs(directory)
    with open(absolute_path, 'w+') as file:
        return file.write(content)