import random
from task import Task

class GithubSimulator:

    def __init__(self, skills, number_of_tasks, number_of_contributors):
        self.last_update = ""
        self.skills = skills
        self.tasks = self.tasks_mockup(number_of_tasks)
        self.number_of_contributors = number_of_contributors

    def tasks_mockup(self, tasks_number):
        tasks = []
        for i in range(1, tasks_number + 1):
            skill_index = random.randint(0,4)
            task = Task(i, "tarea "+ str(i), "www.github.com", self.skills[skill_index],"")
            task.update_status("open")
            tasks.append(task)
        return tasks

    def update(self):
        #print "to do update"
        print ""

    def import_tasks(self):
        self.update()
        open_tasks = []
        for task in self.tasks:
            if task.state == "open":
                open_tasks.append(task)
        return open_tasks

    def get_total_contributors(self):
        return self.number_of_contributors
