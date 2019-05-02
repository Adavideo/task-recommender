from task import Task
from AdaptativeTaskAllocation import AdaptativeTaskAllocation

class Recommender:

    def __init__(self, user, github):
        self.github = github
        self.number_of_tasks_to_recommend = user.tasks_number
        self.task_allocation = AdaptativeTaskAllocation(user.skills, user.skills_thresholds)

    def tasks_importer(self):
        tasks_list = self.github.import_tasks()
        # TODO: Only update when it has passed more time that it is estrablished in the config file
        total_contributors = self.github.get_total_contributors()
        self.task_allocation.update(tasks_list, total_contributors)
        return tasks_list

    def add_task_if_passes_the_filter(self, filtered_tasks, task):
        if task.not_assigned():
            task_passes_the_filter = self.task_allocation.validate_if_task_pass_the_filter(task.skill)
            if task_passes_the_filter:
                filtered_tasks.append(task)

    def filter_tasks(self, unfiltered_tasks):
        recommended_tasks = []
        for i in range(0, len(unfiltered_tasks)):
            if len(recommended_tasks) < self.number_of_tasks_to_recommend:
                self.add_task_if_passes_the_filter(recommended_tasks, unfiltered_tasks[i])
            else:
                break
        return recommended_tasks

    def recommend_tasks(self):
        unfiltered_tasks = self.tasks_importer()
        recommended_tasks = self.filter_tasks(unfiltered_tasks)
        return recommended_tasks
