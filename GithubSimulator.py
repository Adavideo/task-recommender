import random
from task import Task

class GithubSimulator:

    def __init__(self, skills, number_of_tasks, number_of_contributors):
        self.last_update = ""
        self.skills = skills
        self.tasks = self.tasks_mockup(number_of_tasks)
        self.number_of_contributors = number_of_contributors

    def mock_task(self, task_number):
        skill_index = random.randint(0,4)
        skill = self.skills[skill_index]
        name = "Task "+ str(task_number)
        task = Task(task_number, name, "www.github.com", skill,"")
        task.update_status("open")
        return task

    def tasks_mockup(self, tasks_number):
        tasks = []
        for i in range(1, tasks_number + 1):
            task = self.mock_task(i)
            tasks.append(task)
        return tasks

    def add_new_task(self):
        task_number = len(self.tasks) + 1
        new_task = self.mock_task(task_number)
        self.tasks.append(new_task)

    def update(self):
        self.add_new_task()
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
