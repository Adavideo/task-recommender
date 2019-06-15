from user import User
from Config import Config

class Stage(object):

    def __init__(self, config):
        self.num_tasks = config.tasks_number
        self.skills = config.skills
        self.users = []

    def set_user_skills(self, user, type):
        count = 0
        user.skills = self.skills
        user_has_the_skill = {}
        for skill in self.skills:
            count += 1
            if type == count:
                user_has_the_skill[skill] = True
            else:
                user_has_the_skill[skill] = False
        user.initialize_new_skills(user_has_the_skill)

    def generate_user(self, type):
        user_name = "User type %d" % type
        user = User(user_name, "", self.num_tasks)
        self.set_user_skills(user, type)
        return user

    def initialize_users(self, user_types):
        self.user_types = user_types
        self.reset_users()

    def reset_users(self):
        self.users = []
        for user_type in self.user_types:
            new_user = self.generate_user(user_type)
            self.users.append(new_user)

    def description(self):
        #description = "Stage with users " + self.users
        description = "Stage with users: %s\n" % self.user_types
        for user in self.users:
            description += "%s %s\n" % (user.name, user.skills_thresholds)
        return description
