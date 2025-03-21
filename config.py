import os
import dotenv

dotenv.load_dotenv()

def get_file_paths():
    first_file_path = os.getenv("FIRST_FILE_PATH")
    second_file_path = os.getenv("SECOND_FILE_PATH")
    output_folder = os.getenv("OUTPUT_FILE_PATH")
    return output_folder, first_file_path, second_file_path
