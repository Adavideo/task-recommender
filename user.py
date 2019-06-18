import configparser
from AdaptativeTaskAllocation import AdaptativeTaskAllocation

class User(object):

    def __init__(self, user_name, user_pass, tasks_number):
        self.name = user_name
        self.password = user_pass
        self.tasks_number = tasks_number
        self.skills_thresholds = {}
        self.working_on_task = ""
        self.time_to_finish_task = 0

    def initialize_task_allocation(self):
        self.task_allocation = AdaptativeTaskAllocation(self.skills_thresholds)

    def load_skills_from_file(self, skills):
        self.skills = skills
        user_file = configparser.ConfigParser()
        user_file.read("user_skills")
        try:
            for skill in skills:
                self.skills_thresholds[skill] = float(user_file['user_skills'][skill])
        except KeyError:
            raise Exception("User file needed or malformed.")
        self.initialize_task_allocation()

    def calculate_threshold(self, has_the_skill):
        if has_the_skill:
            threshold = 0.1
        else:
            threshold = 0.9
        return threshold

    def initialize_new_skills(self, new_user_skills):
        for skill in self.skills:
            has_the_skill = new_user_skills[skill]
            self.skills_thresholds[skill] = self.calculate_threshold(has_the_skill)
        self.initialize_task_allocation()

    def assign(self, task):
        self.working_on_task = task
        self.time_to_finish_task = 10 * self.skills_thresholds[task.skill]

    def work_on_task(self):
        self.time_to_finish_task -= 1
        if self.time_to_finish_task <= 0:
            self.complete_current_task()

    def increment_skill(self, skill):
        threshold = self.skills_thresholds[skill]
        if threshold > 0:
            self.skills_thresholds[skill] = threshold - 0.05
        if self.skills_thresholds[skill] < 0:
            self.skills_thresholds[skill] = 0

    def complete_current_task(self):
        skill = self.working_on_task.skill
        self.increment_skill(skill)
        self.working_on_task.close_task()
        self.working_on_task = ""
