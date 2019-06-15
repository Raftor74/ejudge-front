import shutil
import os


class FileManager(object):

    EOF = '\n'

    def is_dir_exist(self, dir_path):
        return os.path.isdir(dir_path)

    def is_file_exist(self, dir_path):
        return os.path.isfile(dir_path)

    def remove_file(self, file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)
        return self

    def create_directory(self, dir_path):
        try:
            os.mkdir(dir_path)
        except FileExistsError:
            pass

        return True

    def create_directory_tree(self, dir_path):
        try:
            os.makedirs(dir_path, exist_ok=True)
        except Exception:
            pass
        return True

    def save_file(self, file_name, file_content):
        with open(file_name, mode="w", encoding="utf-8") as _file:
            _file.write(file_content)

    def remove_directory_tree(self, dir_path):
        shutil.rmtree(dir_path, True)
        return True