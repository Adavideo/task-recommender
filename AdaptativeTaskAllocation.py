from Config import Config
import random

class AdaptativeTaskAllocation:

    def __init__(self, skills_thresholds):
            self.skills_thresholds = skills_thresholds
            self.config = Config()
            self.config.load_recommender_parametters()
            self.tasks_stimuli = {}
            self.tasks_performance = {}
            self.proportion_of_tasks_per_type = {}
            self.previous_proportion_of_tasks = {}

    # Functions that make the calculations

    def response_probability(self, threshold, stimulus):
        # Individuals engage in task performance when the level of the task-associated stimuli exceeds their thresholds
        # Response threshold formula
        # T_0i (s) = s^n / s^n + 0i^n
        n = self.config.nonlinearity_parameter
        response_probability = (stimulus ** n) / ((stimulus ** n) + threshold ** n)
        #print "threshold: %f  stimulus: %f  Response probability: %s" % (threshold, stimulus, response_probability)
        return response_probability

    def ensure_scale(self, value, min, max):
        if value < min:
            value = min
        elif value > max:
            value = max
        return value

    def calculate_task_performance(self, task_type):
        if not self.previous_proportion_of_tasks:
            return self.config.task_performance_default
        else:
            current_proportion = self.proportion_of_tasks_per_type[task_type]
            previous_proportion = self.previous_proportion_of_tasks[task_type]
            scale = self.config.task_performance_scale
            medium = (scale[1] - scale[0]) / 2
            decrement = previous_proportion - current_proportion
            #print "%s - previous: %f  current: %f  decrement: %f " % (task_type, previous_proportion_of_tasks, current_proportion_of_tasks, decrement)
            #print "task performance %s = %f + %f + (%f * %f)" % (task_type, scale[0],medium,decrement ,medium  )
            types_of_tasks = len(self.config.skills)
            equal_proportion = 1.0/types_of_tasks
            #print "%s - equal %f  current %f" % (task_type, equal_proportion, current_proportion)
            proportion_adjustment = self.config.task_performance_proportion_adjustment
            # if there is too many tasks of some type, the performance is bad
            if (current_proportion > equal_proportion):
                proportion_adjustment = -1 * proportion_adjustment
            # if there is less tasks of some type than the equal proportion, the performance is good
            elif (current_proportion < equal_proportion):
                proportion_adjustment = proportion_adjustment
            else:
                proportion_adjustment = 0.0
            #print "%s total proportion adjustment: %f" % (task_type, proportion_adjustment)
            task_performance = scale[0] + medium + (decrement * medium) + proportion_adjustment
            task_performance = self.ensure_scale(task_performance, scale[0], scale[1])
        #print "Task performance %s: %f" % (task_type, task_performance)
        return task_performance

    def calculate_stimulus(self, task_type):
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
        new_stimulus = stimulus + delta - (alfa * N_act / N )
        #print "%s stimulus = %s + %s - (%s * %s / %s) = %s" % (task_type, stimulus, delta, alfa, N_act, N, new_stimulus)
        new_stimulus = self.ensure_scale(new_stimulus, self.config.minimum_stimulus, self.config.maximum_stimulus)
        #print "stimulus %s: %f" % (task_type, new_stimulus)
        return new_stimulus

    def calculate_active_contributors(self, tasks):
        contributors = []
        for task in tasks:
            if task.assigned_to and task.assigned_to not in contributors:
                contributors.append(task.assigned_to)
        return len(contributors)

    # util

    def count_tasks_of_type(self, task_type, tasks):
        number_of_tasks = 0.0
        for task in tasks:
            if task.skill == task_type:
                number_of_tasks += 1
        #print "Number of tasks of type %s: %f" % (task_type, number_of_tasks)
        return number_of_tasks


    # UPDATE functions

    def update_contributors(self, tasks, total_contributors):
        self.active_contributors = self.calculate_active_contributors(tasks)
        # The total of contributors is extracted from the number of people that has make a commit to the repository at some point.
        # Active contributors is the number of users that has an issue assigned at this mommet.
        # It is possible, if users has issues assigned but had not make any commits, that the total is lower than active users.
        # In that case, we simply assume that the total of users is the same as the active users
        if total_contributors > self.active_contributors:
            self.total_contributors = total_contributors
        else:
            self.total_contributors = self.active_contributors
        #print "Update contributors. Total: %d  Active: %d " % (self.total_contributors, self.active_contributors)

    def update_tasks_per_type(self, tasks):
        if self.proportion_of_tasks_per_type:
            for skill in self.config.skills:
                self.previous_proportion_of_tasks[skill] = self.proportion_of_tasks_per_type[skill]
        total_number_of_tasks = len(tasks)
        if total_number_of_tasks == 0:
            for skill in self.config.skills:
                self.proportion_of_tasks_per_type[skill] = 0
        else:
            for skill in self.config.skills:
                self.proportion_of_tasks_per_type[skill] = self.count_tasks_of_type(skill, tasks) / total_number_of_tasks

    def update_tasks_performance(self, tasks):
        self.update_tasks_per_type(tasks)
        for skill in self.config.skills:
            self.tasks_performance[skill] = self.calculate_task_performance(skill)

    def initialize_stimuli(self):
        for skill in self.config.skills:
            self.tasks_stimuli[skill] = self.config.default_stimulus

    def update_stimuli(self):
        if not self.tasks_stimuli:
            self.initialize_stimuli()
        else:
            for skill in self.config.skills:
                new_stimulus = self.calculate_stimulus(skill)
                self.tasks_stimuli[skill] = new_stimulus

    def update(self, tasks, total_contributors):
        self.update_contributors(tasks, total_contributors)
        self.update_tasks_performance(tasks)
        self.update_stimuli()


    # Main function for the filtering

    def validate_if_task_pass_the_filter(self, skill):
        if skill == "":
            return False
        task_threshold = self.skills_thresholds[skill]
        #print "threshold for skill: %f" % task_threshold
        stimulus = self.tasks_stimuli[skill]
        #print "Stimulus for task %s: %f" % (skill, stimulus)
        r = random.randint(0,100) / 100.0
        if r < self.response_probability(task_threshold, stimulus):
            return True
        else:
            return False
