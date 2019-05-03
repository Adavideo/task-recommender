from task import Task

class Recommender:

    def __init__(self, github):
        self.github = github

    def add_task_if_passes_the_filter(self, task_allocation, filtered_tasks, task):
        if task.not_assigned():
            task_passes_the_filter = task_allocation.validate_if_task_pass_the_filter(task.skill)
            if task_passes_the_filter:
                filtered_tasks.append(task)

    def filter_tasks(self, user, unfiltered_tasks):
        recommended_tasks = []
        for i in range(0, len(unfiltered_tasks)):
            if len(recommended_tasks) < user.tasks_number:
                self.add_task_if_passes_the_filter(user.task_allocation, recommended_tasks, unfiltered_tasks[i])
            else:
                break
        return recommended_tasks

    def update_task_allocation(self, task_allocation, tasks):
        # TODO: Only update when it has passed more time that it is estrablished in the config file
        total_contributors = self.github.get_total_contributors()
        task_allocation.update(tasks, total_contributors)

    def recommend_tasks(self, user):
        unfiltered_tasks = self.github.import_tasks()
        self.update_task_allocation(user.task_allocation, unfiltered_tasks)
        recommended_tasks = self.filter_tasks(user, unfiltered_tasks)
        return recommended_tasks
