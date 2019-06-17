import configparser

class Config:
    """Reads the config file
    """

    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config")
        self.config = config
        try:
            self.project = config['Project']['name']
            self.user_name = config['Credentials']['user']
            self.password = config['Credentials']['pass']
            self.skills = config['Skills']['list'].split(",")
            self.tasks_number = int(config['Recommender']['tasks_number'])
        except KeyError:
            raise Exception("Config file needed or malformed. Please, copy and fill config-default.")

    def load_recommender_parametters(self):
        config = self.config
        self.nonlinearity_parameter = float(config['Recommender']['nonlinearity_parameter'])
        # [Stimuli]
        self.default_stimulus = float(config['Stimuli']['default'])
        self.increase_in_stimulus_intensity = float(config['Stimuli']['increase_in_intensity'])
        self.minimum_stimulus = float(config['Stimuli']['minimum'])
        self.maximum_stimulus = float(config['Stimuli']['maximum'])
        # [TaskPerformance]
        task_performance_scale = config['TaskPerformance']['scale'].split("-")
        self.task_performance_scale = [float(task_performance_scale[0]),float(task_performance_scale[1])]
        self.task_performance_default = float(config['TaskPerformance']['default'])
        self.task_performance_proportion_adjustment = float(config['TaskPerformance']['proportion_adjustment'])

    def load_simulator_parametters(self):
        self.iterations = int(self.config['Simulator']['iterations'])
        self.simulations = int(self.config['Simulator']['simulations'])
