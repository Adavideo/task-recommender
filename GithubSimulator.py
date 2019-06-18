import random
from task import Task

class GithubSimulator:

    def __init__(self, config, number_of_contributors, tasks_probabilities):
        self.last_update = ""
        self.skills = config.skills
        self.tasks_probabilities = tasks_probabilities
        self.tasks = self.tasks_mockup(config.tasks_number * 2)
        self.number_of_contributors = number_of_contributors
        self.new_tasks_per_iteration = config.new_tasks_per_iteration

    def task_roulete(self):
        r = random.randint(0,100)
        added_probability = 0
        skill_index = 0
        for probability in self.tasks_probabilities:
            added_probability += probability
            if r <= added_probability:
                task_type = self.skills[skill_index]
                break
            else:
                skill_index += 1
        return task_type

    def mock_task(self, task_number):
        skill = self.task_roulete()
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
        for i in range(0, self.new_tasks_per_iteration):
            self.add_new_task()

    def import_tasks(self):
        open_tasks = []
        for task in self.tasks:
            if task.state == "open":
                open_tasks.append(task)
        return open_tasks

    def get_total_contributors(self):
        return self.number_of_contributors
