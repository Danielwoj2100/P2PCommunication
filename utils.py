import os


def load_file(file_path: str):
    try:
        with open(file_path, 'rb') as file:
            print(f"Loaded file {file_path}")
            data = bytearray(file.read())
        return data
    except IOError:
        print(f"Error while loading file with path: {file_path}")
        return None


def create_directory(directory_path):
    try:
        os.makedirs(directory_path)
        print(f"Directory has been created {directory_path}")
    except OSError:
        print(f"Failed to create directory: {directory_path}")


def save_file(file_path: str, data: bytearray):
    try:
        print(data)
        dir_path = "/".join(file_path.split('/')[:-1])
        print(dir_path)
        if not os.path.exists(dir_path):
            create_directory(dir_path)
        with open(file_path, "wb") as file:
            file.write(bytearray(data))
            print(f"File {file_path} written")
    except IOError:
        print(f"Error while saving file with path: {file_path}")
