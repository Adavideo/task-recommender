import random
from task import Task

class GithubSimulator:

    def __init__(self, skills, number_of_tasks, number_of_contributors, tasks_probabilities):
        self.last_update = ""
        self.skills = skills
        self.tasks_probabilities = tasks_probabilities
        self.tasks = self.tasks_mockup(number_of_tasks)
        self.number_of_contributors = number_of_contributors

    def task_roulete(self):
        #print self.tasks_probabilities
        r = random.randint(0,100)
        #print r
        added_probability = 0
        skill_index = 0
        for probability in self.tasks_probabilities:
            added_probability += probability
            if r <= added_probability:
                task_type = self.skills[skill_index]
                #print "selected: %s" % task_type
                break
            else:
                skill_index += 1
        #print "Returning %s" % task_type
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

    def print_tasks(self):
        for task in self.tasks:
            if task.not_assigned():
                print "%s %s %s" % (task.name, task.skill, task.state)
            else:
                print "%s %s %s - assigned to: %s" % (task.name, task.skill, task.state, task.assigned_to)
        print "-"*10

    def add_new_task(self):
        task_number = len(self.tasks) + 1
        new_task = self.mock_task(task_number)
        #print "tareas antes: %d" % len(self.tasks)
        #self.print_tasks()
        self.tasks.append(new_task)
        #print "tareas despues: %d" % len(self.tasks)
        #self.print_tasks()

    def update(self):
        self.add_new_task()

    def import_tasks(self):
        open_tasks = []
        for task in self.tasks:
            if task.state == "open":
                open_tasks.append(task)
        return open_tasks

    def get_total_contributors(self):
        return self.number_of_contributors
