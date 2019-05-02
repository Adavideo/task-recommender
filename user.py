import configparser

class User(object):

    def __init__(self, user_name, user_pass, tasks_number):
        self.name = user_name
        self.password = user_pass
        self.tasks_number = tasks_number
        self.skills_thresholds = {}
        self.working_on_task = ""

    def load_skills_from_file(self, skill_list):
        self.skills = skill_list
        user_file = configparser.ConfigParser()
        user_file.read("user_skills")
        try:
            for skill in skill_list:
                self.skills_thresholds[skill] = float(user_file['user_skills'][skill])
                #print "==== skills from user file: %s = %s" % (skill, self.skills_thresholds[skill])
        except KeyError:
            raise Exception("User file needed or malformed.")


    def calculate_threshold(self, has_the_skill):
        if has_the_skill:
            threshold = 0.1
        else:
            threshold = 0.9
        return threshold

    def initialize_new_skills(self, user_skills):
        for skill in self.skills:
            self.skills_thresholds[skill] = self.calculate_threshold(user_skills[skill])
            #print "Umbral de %s: %f" % (skill, self.skills_thresholds[skill])

    def assign(self, task):
        self.working_on_task = task

    def complete_current_task(self):
        self.working_on_task.close_task()
        self.working_on_task = ""
