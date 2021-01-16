class Singleton():
    """ A Singleton class to be used as a base """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class InformantConfig(metaclass=Singleton):
    """ Class to store global Informant arguments/options and configuration """

    def __init__(self):
        self.argv = {}
        self.config = {}

    def set_argv(args):
        self.argv = args

    def get_argv():
        return self.argv

    def set_config(config):
        self.config = config

    def get_config():
        return self.config
