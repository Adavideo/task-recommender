from user import User
from Recommender import Recommender
from task import Task
from Config import Config
from GithubSimulator import GithubSimulator
import random

# Initialization

def initialize_recommender(skills, tasks_number, adaptative):
    simulator = GithubSimulator(skills, tasks_number * 2, 5)
    return Recommender(simulator, adaptative)

def initialize_users(number_of_users, skills, tasks_number):
    users = []
    for i in range(1,number_of_users+1):
        user_name = "TestUser%d" % i
        test_user = User(user_name, "", tasks_number)
        test_user.load_skills_from_file(skills)
        users.append(test_user)
    return users

# Util

def print_simulation_header(adaptative, number_of_users, iterations):
    if adaptative:
        print "Adaptative. users: %d iterations: %d " % (number_of_users, iterations)
    else:
        print "Greedy. users: %d iterations: %d " % (number_of_users, iterations)


def print_tasks(tasks):
    for task in tasks:
        if task.not_assigned():
            print "%s. Skill required: %s. Status: %s" % (task.name, task.skill, task.state)
        else:
            print "%s. Skill required: %s. Status: %s - assigned to: %s" % (task.name, task.skill, task.state, task.assigned_to)
    print "_________________________"

def print_user_parameters(users_parameters):
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

def print_pending_tasks(statistics):
    print "Pending tasks per type:"
    print statistics["pending tasks per type"]

def print_statistics(statistics):
    print "-" * 20
    print "STATISTICS"
    print statistics



# Extracting and preparing results

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

def calculate_simulations_average(simulations_statistics):
    num_simulations = len(simulations_statistics)
    print "Simulations: %d" % num_simulations
    total_completed_tasks = 0
    total_pending_tasks = 0
    for simulation_results in simulations_statistics:
        total_completed_tasks += simulation_results["completed tasks"]
        total_pending_tasks += simulation_results["pending tasks"]
        print "Completed tasks: %d  Pending tasks: %d" % (simulation_results["completed tasks"],simulation_results["pending tasks"])
    #print_pending_tasks(statistics)
    print "completed = %f  pending = %f" % (total_completed_tasks, total_pending_tasks)
    average_completed_tasks = total_completed_tasks / num_simulations
    average_pending_tasks = total_pending_tasks / num_simulations
    return {"average_completed_tasks":average_completed_tasks, "average_pending_tasks": average_pending_tasks}

def compare_statistics(greedy_simulations_statistics, adaptative_simulations_statistics):
    greedy_average_results = calculate_simulations_average(greedy_simulations_statistics)
    adaptative_average_results = calculate_simulations_average(adaptative_simulations_statistics)
    print "Greedy"
    print greedy_average_results
    print "Adaptative"
    print adaptative_average_results

def get_users_parameters(users):
    stimuli = []
    tasks_performance = []
    for user in users:
        stimuli.append(user.task_allocation.tasks_stimuli)
        tasks_performance.append(user.task_allocation.tasks_performance)
    return {"stimuli":stimuli, "tasks performance":tasks_performance}


# Simulation

def asign_random_task(user, tasks):
    number_of_tasks = len(tasks)
    task_number = random.randint(1,number_of_tasks)
    selected_task = tasks[task_number-1]
    #print "selecting: %s" % (selected_task.name)
    selected_task.assign(user.name)
    user.assign(selected_task)

def simulate_user_behavior(user, recommender):
    #print_tasks(recommender.github.tasks)
    if not user.working_on_task:
        recommended_tasks = recommender.recommend_tasks(user)
        if recommended_tasks:
            asign_random_task(user, recommended_tasks)
    else:
        user.work_on_task()
    #print_tasks(recommender.github.tasks)

def simulate_iteration(iterations, users, recommender):
    for i in range(1, iterations+1):
        recommender.github.update()
        for user in users:
            simulate_user_behavior(user, recommender)

def run_simulation(config, iterations, number_of_users, adaptative):
    # Inicializing users
    users = initialize_users(number_of_users, config.skills, config.tasks_number)

    # Initialize recommender
    recommender = initialize_recommender(config.skills, config.tasks_number, adaptative)

    # Run the simulation
    simulate_iteration(iterations, users, recommender)

    # Get the results
    statistics = get_statistics(recommender.github.tasks, config.skills)
    #users_parameters = get_users_parameters(users)

    # Show the results
    # print_statistics(statistics)
    # print_user_parameters(users_parameters)

    return statistics

def run_several_simulations(config, num_simulations, num_iterations, num_users, adaptative):
    print_simulation_header(adaptative, num_users, num_iterations)
    statistics = []
    for i in range(0,num_simulations):
        result = run_simulation(config, num_iterations, num_users, adaptative)
        statistics.append(result)
    return statistics

# Load config file
config = Config()

# Get user input
#number_of_users = int(raw_input("Number of users: "))
num_users = 5
#iterations = int(raw_input("Select number of iterations: "))
num_iterations = 300
#adaptative = select_greedy_or_adaptative(raw_input("Greedy or adaptative task allocation? (g/a): "))
num_simulations = 10

# Runing the simulations for adaptative and greedy task allocation
adaptative = False
greedy_statistics = run_several_simulations(config, num_simulations, num_iterations, num_users, adaptative)
adaptative = True
adaptative_statistics = run_several_simulations(config, num_simulations, num_iterations, num_users, adaptative)

# Comparing the results of greedy and adaptative simulations
results = compare_statistics(greedy_statistics, adaptative_statistics)
