from user import User
from Recommender import Recommender
from task import Task
from Config import Config
from GithubSimulator import GithubSimulator
import random

def print_tasks(tasks):
    for task in tasks:
        if task.not_assigned():
            print "%s. Skill required: %s. Status: %s" % (task.name, task.skill, task.state)
        else:
            print "%s. Skill required: %s. Status: %s - assigned to: %s" % (task.name, task.skill, task.state, task.assigned_to)
    print "_________________________"

def select_random_task(user, tasks):
    task_number = random.randint(1,len(tasks))
    selected_task = tasks[task_number-1]
    print "selecting: %s" % (selected_task.name)
    selected_task.assign(user.name)
    user.assign(selected_task)

def get_recommendations_and_select_task(user, recommender):
    tasks = []
    while not tasks:
        tasks = recommender.recommend_tasks()
    select_random_task(user, tasks)

def simulate_user_behavior(user, recommender):
    if not user.working_on_task:
        get_recommendations_and_select_task(user, recommender)
    else:
        user.complete_current_task()



config = Config()
simulator = GithubSimulator(config.skills, config.tasks_number * 2, 5)

test_user = User("TestUser1", "", config.tasks_number)
test_user.load_skills_from_file(config.skills)
recommender = Recommender(test_user, simulator)

print "Initial list of tasks:"
print_tasks(simulator.tasks)

iterations = int(raw_input("Select number of iterations: "))
for i in range(1, iterations+1):
    simulate_user_behavior(test_user, recommender)

print "-" * 10
print "Final list of tasks:"
print_tasks(simulator.tasks)
