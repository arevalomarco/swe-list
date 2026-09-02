"""In-Memory FS — your implementation goes here."""


class FS:
    def mkdir(self, path):
        raise NotImplementedError

    def ls(self, path):
        raise NotImplementedError

    def write(self, path, data):
        raise NotImplementedError

    def read(self, path):
        raise NotImplementedError

    def rm(self, path):
        raise NotImplementedError

    def rmdir(self, path):
        raise NotImplementedError

    def link(self, existing, new_path):
        raise NotImplementedError

    def unlink(self, path):
        raise NotImplementedError
