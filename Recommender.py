from task import Task
import random
from githubConnector import import_tasks_from_github
from Config import Config

class Recommender:

    def __init__(self, user):
        self.user = user
        self.number_of_tasks_to_recommend = user.tasks_number
        self.skills_thresholds = user.skills_thresholds
        self.skills = user.skills
        config = Config()
        self.project = config.project
        self.nonlinearity_parameter = int(config.nonlinearity_parameter)
        self.tasks_stimuli = {}
        self.default_stimuli = config.default_stimuli
        self.increase_in_stimulus_intensity = config.increase_in_stimulus_intensity
        self.tasks_performance = {}
        self.number_of_tasks_per_type = {}
        self.previous_number_of_tasks = {}

    def count_tasks_of_type(self, task_type, tasks_list):
        number_of_tasks = 0.0
        for task in tasks_list:
            if task.skill == task_type:
                number_of_tasks += 1
        print "Number of tasks of type %s: %f" % (task_type, number_of_tasks)
        return number_of_tasks

    def update_number_of_tasks_per_type(self, tasks_list):
        if self.number_of_tasks_per_type:
            self.previous_number_of_tasks = self.number_of_tasks_per_type
        for skill in self.skills:
            self.number_of_tasks_per_type[skill] = self.count_tasks_of_type(skill, tasks_list)

    def calculate_task_performance(self, task_type, tasks_list):
        total_number_of_tasks = len(tasks_list)
        current_number_of_tasks = self.number_of_tasks_per_type[task_type]
        if self.previous_number_of_tasks:
            previous_number_of_tasks = self.number_of_tasks_per_type[task_type]
            task_performance = (previous_number_of_tasks - current_number_of_tasks) / total_number_of_tasks
        else:
            task_performance = current_number_of_tasks / total_number_of_tasks
        print "Task performance %s: %f" % (task_type, task_performance)
        return task_performance

    def update_tasks_performance(self, tasks_list):
        self.update_number_of_tasks_per_type(tasks_list)
        for skill in self.skills:
            self.tasks_performance[skill] = self.calculate_task_performance(skill, tasks_list)

    def initialize_stimuli(self):
        for skill in self.skills:
            self.tasks_stimuli[skill] = self.default_stimuli

    def calculate_and_update_stimulus(self, task_type):
        # s(t+1) = s(t) + delta - ( alfa * N_act / N )
        # delta : increase in stimulus intensity per unit time
        # alfa : scale factor measuring the efficiency of task performance
        #N: number of potentially active individuals in the colony
        #N_act : number of active individuals
        stimulus = self.tasks_stimuli[task_type]
        delta = self.increase_in_stimulus_intensity
        alfa = self.tasks_performance[task_type]
        N = 10
        N_act = 3
        self.tasks_stimuli[task_type] = stimulus + delta - (alfa * N_act / N )

    def update_stimuli(self):
        if not self.tasks_stimuli:
            self.initialize_stimuli()
        else:
            for skill in self.skills:
                self.calculate_and_update_stimulus(skill)

    def tasks_importer(self):
        tasks_list = import_tasks_from_github(self.project, self.user)
        self.update_tasks_performance(tasks_list)
        self.update_stimuli()
        return tasks_list

    def response_probability(self, threshold, stimulus):
        # Individuals engage in task performance when the level of the task-associated stimuli exceeds their thresholds
        # Response threshold formula
        # T_0i (s) = s^n / s^n + 0i^n
        n = self.nonlinearity_parameter
        response_probability = (stimulus ** n) / ((stimulus ** n) + threshold ** n)
        print "//// response probability: %s" % response_probability
        return response_probability

    def validate_if_task_pass_the_filter(self, task):
        #print "Filtrando tarea %s. Skill: %s. " % (task.name, task.skill)
        if task.skill == "":
            return False
        task_threshold = self.skills_thresholds[task.skill]
        #print "threshold for skill: %f" % task_threshold
        stimulus = self.tasks_stimuli[task.skill]
        print "Stimulus for task %s: %f" % (task.skill, stimulus)
        r = random.randint(0,100) / 100.0
        if r < self.response_probability(task_threshold, stimulus):
            return True
        else:
            return False

    def add_task_if_passes_the_filter(self, filtered_tasks, task):
        task_passes_the_filter = self.validate_if_task_pass_the_filter(task)
        if task_passes_the_filter:
            filtered_tasks.append(task)

    def filter_tasks(self, unfiltered_tasks):
        filtered_tasks = []
        for i in range(0, len(unfiltered_tasks)):
            if len(filtered_tasks) < self.number_of_tasks_to_recommend:
                self.add_task_if_passes_the_filter(filtered_tasks, unfiltered_tasks[i])
            else:
                break
        return filtered_tasks

    def recommend_tasks(self):
        unfiltered_tasks = self.tasks_importer()
        tasks_list = self.filter_tasks(unfiltered_tasks)
        return tasks_list
