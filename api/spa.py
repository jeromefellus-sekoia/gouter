from fastapi.staticfiles import StaticFiles


class SinglePageApplication(StaticFiles):
    def __init__(self, directory, index="index.html") -> None:
        self.index = index
        super().__init__(directory=directory, packages=None, html=True, check_dir=True)

    def lookup_path(self, path: str):
        full_path, stat_result = super().lookup_path(path)
        if stat_result is None:
            return super().lookup_path(self.index)
        return (full_path, stat_result)
