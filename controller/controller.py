from lib.cryptool import encrypt, decrypt
from model.file_object import FileObject
import re


class Controller:
    def __init__(self):
        self._source = None
        self._target = None
        self._password = ""

    def can_continue(self):
        return self._source and self._target and self._password

    def encrypt(self):
        result = -1
        if self.can_continue():
            result = encrypt(self._target.source, self._source.source, self._password)
        return result

    def decrypt(self):
        result = -1
        if self.can_continue():
            result = decrypt(self._target.source, self._source.source, self._password)
        return result

    def target_event(self, name):
        result = None
        if not re.search(r'[^(a-z)|^(0-9)|^(.* )]', name) and name.strip() != "":
            result = self._target = FileObject(self.source.file_dir + "/" + name + self.source.file_extension)
        else:
            self._target = None
        return result

    def source_event(self, path):
        self.source = FileObject(path)

    def password_event(self, passwd):
        result = None
        if passwd != "":
            self._password = passwd
        return result

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def password(self):
        return self._password

    @source.setter
    def source(self, s):
        self._source = s

    @target.setter
    def target(self, t):
        self._target = t

    @password.setter
    def password(self, p=""):
        self._password = p

