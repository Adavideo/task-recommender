class User(object):

    def __init__(self, user_name, user_pass, tasks_number):
        self.name = user_name
        self.password = user_pass
        self.tasks_number = tasks_number
        self.skills_thresholds = {}

    def calculate_threshold(self, has_the_skill):
        if has_the_skill:
            threshold = 0.1
        else:
            threshold = 0.9
        return threshold

    def initialize_skills(self, skills, user_skills):
        self.skills = skills
        for skill in self.skills:
            self.skills_thresholds[skill] = self.calculate_threshold(user_skills[skill])
            #print "Umbral de %s: %f" % (skill, self.skills_thresholds[skill])

    def config_test_user(self, skills):
        mock_skills = {skills[0]: False, skills[1]: False, skills[2]: True, skills[3]: True, skills[4]: True}
        self.initialize_skills(skills, mock_skills)
