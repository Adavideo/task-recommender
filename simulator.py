from user import User
from Recommender import Recommender
from task import Task
from Config import Config
from GithubSimulator import GithubSimulator
import random

# Initialization

def initialize_recommender(skills, tasks_number):
    simulator = GithubSimulator(skills, tasks_number * 2, 5)
    return Recommender(simulator)

def initialize_users(number_of_users, skills, tasks_number):
    users = []
    for i in range(1,number_of_users+1):
        user_name = "TestUser%d" % i
        test_user = User(user_name, "", tasks_number)
        test_user.load_skills_from_file(skills)
        users.append(test_user)
    return users

# Util

def print_tasks(tasks):
    for task in tasks:
        if task.not_assigned():
            print "%s. Skill required: %s. Status: %s" % (task.name, task.skill, task.state)
        else:
            print "%s. Skill required: %s. Status: %s - assigned to: %s" % (task.name, task.skill, task.state, task.assigned_to)
    print "_________________________"

def print_results(statistics, users_parameters):
    print "-" * 20
    print "STATISTICS"
    print "Completed tasks: %d  Pending tasks: %d" % (statistics["completed tasks"],statistics["pending tasks"])
    print "Pending tasks per type:"
    print statistics["pending tasks per type"]
    print "-" * 10
    print "USERS PARAMETERS:"
    print "Stimuli"
    #print users_parameters["stimuli"]
    count = 1
    for user_stimuli in users_parameters["stimuli"]:
        print "User %d: %s" % (count, user_stimuli)
        count+= 1
    print "Tasks Performance:"
    #print users_parameters["tasks performance"]
    count = 1
    for tasks_performance in users_parameters["tasks performance"]:
        print "User %d: %s" % (count, tasks_performance)
        count+= 1
    #print "Final list of tasks:"
    #print_tasks(recommender.github.tasks)


def get_statistics(tasks, skills):
    completed_tasks = 0
    pending_tasks = 0
    pending_tasks_per_type = {}
    for skill in skills:
        pending_tasks_per_type[skill] = 0
    for task in tasks:
        if task.is_closed():
            completed_tasks += 1
        else:
            pending_tasks += 1
            pending_tasks_per_type[task.skill] += 1
    return {"completed tasks":completed_tasks, "pending tasks":pending_tasks, "pending tasks per type":pending_tasks_per_type}

def get_users_parameters(users):
    stimuli = []
    tasks_performance = []
    for user in users:
        stimuli.append(user.task_allocation.tasks_stimuli)
        tasks_performance.append(user.task_allocation.tasks_performance)
    return {"stimuli":stimuli, "tasks performance":tasks_performance}

# Simulation

def get_recommendations(user, recommender):
    tasks = []
    while not tasks:
        tasks = recommender.recommend_tasks(user)
    return tasks

def asign_random_task(user, tasks):
    task_number = random.randint(1,len(tasks))
    selected_task = tasks[task_number-1]
    #print "selecting: %s" % (selected_task.name)
    selected_task.assign(user.name)
    user.assign(selected_task)

def simulate_user_behavior(user):
    if not user.working_on_task:
        recommended_tasks = get_recommendations(user, recommender)
        asign_random_task(user, recommended_tasks)
    else:
        user.work_on_task()

def simulation(iterations):
    for i in range(1, iterations+1):
        for user in users:
            simulate_user_behavior(user)



config = Config()
recommender = initialize_recommender(config.skills, config.tasks_number)

number_of_users = 3
users = initialize_users(number_of_users, config.skills, config.tasks_number)

#print "Initial list of tasks:"
#print_tasks(recommender.github.tasks)

iterations = int(raw_input("Select number of iterations: "))
simulation(iterations)

statistics = get_statistics(recommender.github.tasks, config.skills)
users_parameters = get_users_parameters(users)

print_results(statistics, users_parameters)
