class NoWineError(RuntimeError):
    def __init__(self):
        super().__init__("A valid wine binary could not be found")
