import configparser
from user import User

class Config:
    """Reads the config file and sets the default github user and project
    """

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config")
        try:
            self.project = config['Project']['name']
            user_name = config['Credentials']['user']
            password = config['Credentials']['pass']
            skills = config['Skills']['list'].split(",")
            tasks_number = config['Tasks']['tasks_number']
            self.nonlinearity_parameter = config['Threshold']['nonlinearity_parameter']
        except KeyError:
            raise Exception("Config file needed or malformed. Please, copy and fill config-default.")
        self.user = User(user_name,password,tasks_number)
        self.user.config_test_user(skills)


    def get_skills(self):
        return self.user.skills
