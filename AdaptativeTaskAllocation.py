from Config import Config
import random

class AdaptativeTaskAllocation:

    def __init__(self, skills, skills_thresholds):
            self.skills = skills
            self.skills_thresholds = skills_thresholds
            self.tasks = []
            self.config = Config()
            self.config.load_recommender_parametters()
            self.tasks_stimuli = {}
            self.tasks_performance = {}
            self.proportion_of_tasks_per_type = {}
            self.previous_proportion_of_tasks = {}

    def count_tasks_of_type(self, task_type, tasks_list):
        number_of_tasks = 0.0
        for task in tasks_list:
            if task.skill == task_type:
                number_of_tasks += 1
        #print "Number of tasks of type %s: %f" % (task_type, number_of_tasks)
        return number_of_tasks

    def update_tasks_per_type(self):
        if self.proportion_of_tasks_per_type:
            self.previous_proportion_of_tasks = self.proportion_of_tasks_per_type
        total_number_of_tasks = len(self.tasks_list)
        for skill in self.skills:
            self.proportion_of_tasks_per_type[skill] = self.count_tasks_of_type(skill, self.tasks_list) / total_number_of_tasks

    def calculate_task_performance(self, task_type):
        if not self.previous_proportion_of_tasks:
            return self.config.task_performance_default
        else:
            current_proportion_of_tasks = self.proportion_of_tasks_per_type[task_type]
            previous_proportion_of_tasks = self.previous_proportion_of_tasks[task_type]
            scale = self.config.task_performance_scale
            medium = (scale[1] - scale[0]) / 2
            decrement = previous_proportion_of_tasks - current_proportion_of_tasks
            task_performance = scale[0] + medium + (decrement * medium)
        #print "Task performance %s: %f" % (task_type, task_performance)
        return task_performance

    def update_tasks_performance(self):
        self.update_tasks_per_type()
        for skill in self.skills:
            self.tasks_performance[skill] = self.calculate_task_performance(skill)

    def initialize_stimuli(self):
        for skill in self.skills:
            self.tasks_stimuli[skill] = self.config.default_stimuli

    def calculate_and_update_stimulus(self, task_type):
        # s(t+1) = s(t) + delta - ( alfa * N_act / N )
        # delta : increase in stimulus intensity per unit time
        # alfa : scale factor measuring the efficiency of task performance
        #N: number of potentially active individuals in the colony
        #N_act : number of active individuals
        stimulus = self.tasks_stimuli[task_type]
        delta = self.config.increase_in_stimulus_intensity
        alfa = self.tasks_performance[task_type]
        if self.total_contributors == 0:
            N = 1
        else:
            N = self.total_contributors
        N_act = self.active_contributors
        #print "contributors. total: %d  active: %d." % (N, N_act)
        self.tasks_stimuli[task_type] = stimulus + delta - (alfa * N_act / N )

    def update_stimuli(self):
        if not self.tasks_stimuli:
            self.initialize_stimuli()
        else:
            for skill in self.skills:
                self.calculate_and_update_stimulus(skill)

    def calculate_active_contributors(self, tasks_list):
        contributors = []
        for task in tasks_list:
            if task.assigned_to and task.assigned_to not in contributors:
                contributors.append(task.assigned_to)
        return len(contributors)

    def update_contributors(self, tasks_list, total_contributors):
        self.active_contributors = self.calculate_active_contributors(tasks_list)
        # The total of contributors is extracted from the number of people that has make a commit to the repository at some point.
        # Active contributors is the number of users that has an issue assigned at this mommet.
        # It is possible, if users has issues assigned but had not make any commits, that the total is lower than active users.
        # In that case, we simply assume that the total of users is the same as the active users
        if total_contributors > self.active_contributors:
            self.total_contributors = total_contributors
        else:
            self.total_contributors = self.active_contributors

    def update(self, tasks_list, total_contributors):
        self.tasks_list = tasks_list
        self.update_contributors(tasks_list, total_contributors)
        self.update_tasks_performance()
        self.update_stimuli()

    def response_probability(self, threshold, stimulus):
        # Individuals engage in task performance when the level of the task-associated stimuli exceeds their thresholds
        # Response threshold formula
        # T_0i (s) = s^n / s^n + 0i^n
        n = self.config.nonlinearity_parameter
        response_probability = (stimulus ** n) / ((stimulus ** n) + threshold ** n)
        #print "//// response probability: %s" % response_probability
        return response_probability

    def validate_if_task_pass_the_filter(self, task_type):
        #print "Filtrando tarea %s. Skill: %s. " % (task.name, task.skill)
        if task_type == "":
            return False
        task_threshold = self.skills_thresholds[task_type]
        #print "threshold for skill: %f" % task_threshold
        stimulus = self.tasks_stimuli[task_type]
        #print "Stimulus for task %s: %f" % (task_type, stimulus)
        r = random.randint(0,100) / 100.0
        if r < self.response_probability(task_threshold, stimulus):
            return True
        else:
            return False
