import os


class DirectoryStack:
    def __init__(self):
        self._history = []

    def pushd(self, path: str) -> str:
        assert os.path.exists(path) and os.path.isdir(path)
        self._history.insert(0, os.getcwd())
        os.chdir(path)

        return path

    def popd(self) -> str:
        assert len(self._history) > 0
        path = self._history.pop(0)
        os.chdir(path)
        return path
