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

    def set_skills(self, initial_skills):
        skills = ["javascript", "css", "python", "django", "html"]

        for skill in skills:
            self.skills_thresholds[skill] = self.calculate_threshold(initial_skills[skill])
            #print "Umbral de %s: %f" % (skill, self.skills_thresholds[skill])

    def config_test_user(self):
        self.tasks_number = 5
        mock_skills = {"javascript": False, "css": False, "python": True, "django": True, "html": True}
        self.set_skills(mock_skills)
