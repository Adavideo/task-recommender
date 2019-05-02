from task import Task
from github import Github
import random
import datetime

class GithubConnector:

    def __init__(self, project, user):
        github = Github(user.name, user.password)
        self.repo = github.get_repo(project)
        self.last_update = ""
        self.skills = user.skills

    def extract_skills_from_labels(self, labels):
        for label in labels:
            if label.name in self.skills:
                return label.name
        return ""

    def import_tasks(self):
        self.last_update = datetime.datetime.now()
        tasks_list = []
        for issue in self.repo.get_issues(state='open'):
            skill = self.extract_skills_from_labels(issue.labels)
            task = Task(issue.title, issue.html_url, skill, issue.assignee)
            task.set_description(issue.body)
            task.update_status(issue.state)
            tasks_list.append(task)
        return tasks_list

    def get_total_contributors(self):
        contributors = self.repo.get_contributors()
        #print contributors.totalCount
        count = 0
        for _ in contributors:
            count += 1
        return count
