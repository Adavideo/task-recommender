import configparser
from user import User

class Config:
    """Reads the config file
    """

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config")
        try:
            self.project = config['Project']['name']
            self.user_name = config['Credentials']['user']
            self.password = config['Credentials']['pass']
            self.skills = config['Skills']['list'].split(",")
            self.tasks_number = int(config['Tasks']['tasks_number'])
            self.nonlinearity_parameter = config['Threshold']['nonlinearity_parameter']
        except KeyError:
            raise Exception("Config file needed or malformed. Please, copy and fill config-default.")
