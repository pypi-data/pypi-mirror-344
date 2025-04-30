class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, process='cpu'):
        if not hasattr(self, 'initialized'):
            self.process = process
            self.initialized = True

    def set_process(self, process):
        if process not in ['cpu', 'gpu']:
            raise ValueError("process must be 'cpu' or 'gpu'")
        self.process = process

    def get_process(self):
        return self.process

config = Config()