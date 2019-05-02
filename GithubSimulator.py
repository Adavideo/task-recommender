import random
from task import Task

class GithubSimulator:

    def __init__(self, user):
        self.last_update = ""
        self.skills = user.skills
        self.tasks_number = user.tasks_number

    def tasks_mockup(self, tasks_number):
        tasks = []
        for i in range(1, tasks_number + 1):
            skill_index = random.randint(0,4)
            task = Task(i, "tarea "+ str(i), "www.github.com", self.skills[skill_index],"")
            tasks.append(task)
        return tasks

    def import_tasks(self):
        tasks_list = self.tasks_mockup(self.tasks_number)
        return tasks_list

    def get_total_contributors(self):
        return 10
