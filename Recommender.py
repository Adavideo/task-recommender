from task import Task
import random
from githubConnector import import_tasks_from_github
from Config import Config

class Recommender:

    def __init__(self, user):
        self.user = user
        self.number_of_tasks = user.tasks_number
        self.skills_thresholds = user.skills_thresholds
        config = Config()
        self.project = config.project
        self.nonlinearity_parameter = int(config.nonlinearity_parameter)

    def tasks_importer(self):
        tasks_list = import_tasks_from_github(self.project, self.user)
        return tasks_list

    def stimulus_intensity(self):
        # s(t+1) = s(t) + delta - ( alfa * N_act / N )
        # delta : increase in stimulus intensity per unit time
        #alfa : scale factor measuring the efficiency of task performance
        #N: number of potentially active individuals in the colony
        #N_act : number of active individuals
        stimulus = 1
        return stimulus

    def response_threshold(self, threshold):
        # Response threshold formula
        # T_0i (s) = s^n / s^n + 0i^n
        # n = nonlinearity parameter
        n = self.nonlinearity_parameter
        stimulus = self.stimulus_intensity()
        threshold_fromula = (stimulus ** n) / ((stimulus ** n) + threshold ** n)
        #print "//// threshold: %s" % threshold_fromula
        return threshold_fromula


    def filter_task(self, task):
        #print "Filtrando tarea %s. Skill: %s. Prioridad: %d." % (task.name, task.skill, task.priority)
        if task.skill == "":
            return False
        threshold = self.skills_thresholds[task.skill]
        #print "threshold for skill: %s" % str(threshold)
        r = random.randint(0,100) / 100.0
        if r < self.response_threshold(threshold):
            return True
        else:
            return False


    def add_task_if_passes_the_filter(self, filtered_tasks, task):
        task_passes_the_filter = self.filter_task(task)
        if task_passes_the_filter:
            filtered_tasks.append(task)


    def filter_tasks(self, unfiltered_tasks):
        filtered_tasks = []

        for i in range(0, len(unfiltered_tasks)):
            if len(filtered_tasks) < self.number_of_tasks:
                self.add_task_if_passes_the_filter(filtered_tasks, unfiltered_tasks[i])
            else:
                break
        return filtered_tasks


    def recommend_tasks(self):
        unfiltered_tasks = self.tasks_importer()
        tasks_list = self.filter_tasks(unfiltered_tasks)
        return tasks_list
