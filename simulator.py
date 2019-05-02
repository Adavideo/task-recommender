from user import User
from Recommender import Recommender
from task import Task
from Config import Config
from GithubSimulator import GithubSimulator
import random

def print_tasks(tasks):
    for task in tasks:
        if task.not_assigned():
            print "%s. Skill required: %s" % (task.name, task.skill)
        else:
            print "%s. Skill required: %s - assigned to: %s" % (task.name, task.skill, task.assigned_to)
    print "_________________________"

def select_random_task(tasks):
    task_number = random.randint(1,len(tasks))
    selected_task = tasks[task_number-1]
    print "selecting: %s" % (selected_task.name)
    selected_task.assign(user.name)

def simulate_user_behavior(user, recommender):
    tasks = []
    print "Recomending tasks"
    while not tasks:
        tasks = recommender.recommend_tasks()
    select_random_task(tasks)


config = Config()
simulator = GithubSimulator(config.skills, config.tasks_number * 2, 5)

user = User("TestUser1", "", config.tasks_number)
user.load_skills_from_file(config.skills)
recommender = Recommender(user, simulator)

print "Initial list of tasks:"
print_tasks(simulator.tasks)

iterations = int(raw_input("Select number of iterations: "))
for i in range(1, iterations+1):
    simulate_user_behavior(user, recommender)

print "Final list of tasks:"
print_tasks(simulator.tasks)
