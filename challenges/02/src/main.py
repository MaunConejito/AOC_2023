from file_management import get_input_file_names, read_data, write_data
from config import SCRIPT_PATH
from part_1 import process as process_1
from part_2 import process as process_2

DATA_FILE_NAMES = get_input_file_names(SCRIPT_PATH)

for DATA_FILE_NAME in DATA_FILE_NAMES:

    input = read_data(SCRIPT_PATH, DATA_FILE_NAME)

    write_data(SCRIPT_PATH, DATA_FILE_NAME + '_1', process_1(input))
    write_data(SCRIPT_PATH, DATA_FILE_NAME + '_2', process_2(input))