from task import Task

class Recommender:

    def __init__(self, github, adaptative):
        self.github = github
        self.adaptative = adaptative

    def validate_task_pass_the_filter(self, task_allocation, task):
        task_pass_the_filter = False
        if task.not_assigned():
            if self.adaptative:
                task_pass_the_filter = task_allocation.validate_if_task_pass_the_filter(task.skill)
            else:
                task_pass_the_filter = True
        return task_pass_the_filter

    def filter_tasks(self, user, unfiltered_tasks):
        recommended_tasks = []
        for i in range(0, len(unfiltered_tasks)):
            if len(recommended_tasks) < user.tasks_number:
                task = unfiltered_tasks[i]
                task_pass_the_filter = self.validate_task_pass_the_filter(user.task_allocation, task)
                if task_pass_the_filter:
                    recommended_tasks.append(task)
            else:
                break
        return recommended_tasks

    def update_task_allocation(self, task_allocation, tasks):
        # TODO: Only update when it has passed more time that it is estrablished in the config file
        total_contributors = self.github.get_total_contributors()
        task_allocation.update(tasks, total_contributors)

    def recommend_tasks(self, user):
        unfiltered_tasks = self.github.import_tasks()
        if self.adaptative:
            self.update_task_allocation(user.task_allocation, unfiltered_tasks)
        if not unfiltered_tasks:
            return []
        recommended_tasks = []
        while not recommended_tasks:
            recommended_tasks = self.filter_tasks(user, unfiltered_tasks)
        return recommended_tasks
