from task import Task
from github import Github
import random
skills = ["javascript", "css", "python", "django", "html"]

def tasks_mockup(tasks_number):
    tasks_list = []
    for i in range(1, tasks_number + 1):
        created_at = random.randint(1,5)
        skill = random.randint(0,4)
        task = Task("tarea "+ str(i), created_at, "www.github.com", skills[skill])
        tasks_list.append(task)
    return tasks_list

def extract_skills_from_labels(labels):
    for label in labels:
        if label.name in skills:
            return label.name
    return ""

def import_tasks_from_github(projectName, user):
    #tasks_list = tasks_mockup(20)
    tasks_list = []

    github = Github(user.name, user.password)
    repo = github.get_repo(projectName)

    for issue in repo.get_issues(state='open'):
        skill = extract_skills_from_labels(issue.labels)
        task = Task(issue.title, issue.created_at, issue.html_url, skill)
        task.set_description(issue.body)
        task.update_status(issue.state, issue.updated_at)
        tasks_list.append(task)
    return tasks_list
