from util_files.file_path_util import get_file_name, get_file_extension
import os


class FileObject:
    def __init__(self, path):
        self._file_dir = os.path.dirname(path)
        self._file_extension = get_file_extension(path)
        self._file_name = get_file_name(path)
        self._source = self._file_dir + "/" + self._file_name + self._file_extension

    @property
    def source(self):
        return self._file_dir + "/" + self._file_name  + self._file_extension

    @property
    def file_dir(self):
        return self._file_dir

    @property
    def file_extension(self):
        return self._file_extension

    @property
    def file_name(self):
        return self._file_name

    @file_dir.setter
    def file_dir(self, file_dir):
        self._file_dir = file_dir

    @file_extension.setter
    def file_extension(self, file_extension):
        self._file_extension = file_extension

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name
