from task import Task
import random
from githubConnector import import_tasks_from_github


skills = ["javascript", "css", "python", "django", "html"]

def tasks_importer(project, user):
    tasks_list = import_tasks_from_github(project, user)
    return tasks_list

def filter_task(task, skills_thresholds):
    #print "Filtrando tarea %s. Skill: %s. Prioridad: %d." % (task.name, task.skill, task.priority)
    if task.skill == "":
        return False
    threshold = skills_thresholds[task.skill]
    #print "threshold for skill: %s" % str(threshold)
    r = random.randint(0,100) / 100.0
    if r > threshold:
        return True
    else:
        return False


def add_task_if_passes_the_filter(tasks_list, task, skills_thresholds):
    task_passes_the_filter = filter_task(task, skills_thresholds)
    if task_passes_the_filter:
        tasks_list.append(task)


def filter_tasks(unfiltered_tasks, number_of_tasks, skills_thresholds):
    filtered_tasks = []

    for i in range(0, len(unfiltered_tasks)):
        if len(filtered_tasks) < number_of_tasks:
            add_task_if_passes_the_filter(filtered_tasks, unfiltered_tasks[i], skills_thresholds)
        else:
            break
    return filtered_tasks


def recommend_tasks(project, user):
    unfiltered_tasks = tasks_importer(project, user)
    tasks_list = filter_tasks(unfiltered_tasks, user.tasks_number, user.skills_thresholds)
    return tasks_list
