from user import User
from Recommender import Recommender
from task import Task
from Config import Config
from GithubSimulator import GithubSimulator
from stage import Stage
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
        #test_user.load_skills_from_file(skills)
        users.append(test_user)
    return users

# Util

def print_simulation_header(adaptative, iterations):
    if adaptative:
        print "Running adaptative simulation. iterations: %d " % iterations
    else:
        print "Running greedy simulation. iterations: %d " % iterations


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
    #print "Completed tasks: %d  Pending tasks: %d" % (statistics["completed tasks"], statistics["pending tasks"])

def print_simulations_comparisions(results):
    print "Adaptative Task Allocation simulations compared with the greedy simulation (on average):"
    print " - Completed %d%% more tasks" % results["completed_tasks"]
    pending = results["pending_tasks"] * -1
    print " - Had %d%% less pending tasks when finishing the simulation" % pending



# Extracting and preparing results

def get_statistics(tasks, skills):
    completed_tasks = 0
    pending_tasks = 0
    pending_tasks_per_type = {}
    #for skill in skills:
    #    pending_tasks_per_type[skill] = 0
    for task in tasks:
        if task.is_closed():
            completed_tasks += 1
        else:
            pending_tasks += 1
            #pending_tasks_per_type[task.skill] += 1
    #return {"completed tasks":completed_tasks, "pending tasks":pending_tasks, "pending tasks per type":pending_tasks_per_type}
    return {"completed tasks":completed_tasks, "pending tasks":pending_tasks}

def calculate_simulations_average(simulations_statistics):
    num_simulations = len(simulations_statistics)
    #print "Simulations: %d" % num_simulations
    total_completed_tasks = 0.0
    total_pending_tasks = 0.0
    #print "/" * 10
    #print simulations_statistics
    for simulation_results in simulations_statistics:
        total_completed_tasks += simulation_results["completed tasks"]
        total_pending_tasks += simulation_results["pending tasks"]
        #print "Completed tasks: %d  Pending tasks: %d" % (simulation_results["completed tasks"],simulation_results["pending tasks"])
    #print_pending_tasks(statistics)
    #print "completed = %f  pending = %f" % (total_completed_tasks, total_pending_tasks)
    average_completed_tasks = total_completed_tasks / num_simulations
    average_pending_tasks = total_pending_tasks / num_simulations
    print "average completed %f pending %f" % (average_completed_tasks, average_pending_tasks)
    return {"average_completed_tasks":average_completed_tasks, "average_pending_tasks": average_pending_tasks}

def calculate_improvement(greedy, adaptative):
    #print "improvement = (%s * 100 / %s) - 100" % (adaptative, greedy)
    #print "greedy: %f adaptative: %f" % (greedy, adaptative)
    if greedy == 0.0:
        improvement = adaptative * 100
    else:
        improvement = (adaptative * 100 / greedy) - 100
    #print "improvement = %f" % improvement
    return improvement

def compare_statistics(greedy_simulations_statistics, adaptative_simulations_statistics):
    greedy_average_results = calculate_simulations_average(greedy_simulations_statistics)
    adaptative_average_results = calculate_simulations_average(adaptative_simulations_statistics)
    completed_tasks_improvement = calculate_improvement(greedy_average_results["average_completed_tasks"], adaptative_average_results["average_completed_tasks"])
    #print "completed_tasks_improvement = %s" % completed_tasks_improvement
    pending_tasks_improvement = calculate_improvement(greedy_average_results["average_pending_tasks"], adaptative_average_results["average_pending_tasks"])
    #print "pending_tasks_improvement = %s" % pending_tasks_improvement
    return {"completed_tasks":completed_tasks_improvement, "pending_tasks":pending_tasks_improvement}

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

def simulate_iterations(iterations, stage, recommender):
    for i in range(1, iterations+1):
        #print "Iteration %d of %d" % (i, num_iterations)
        recommender.github.update()
        for user in stage.users:
            simulate_user_behavior(user, recommender)

def run_simulation(num_iterations, adaptative_mode, stage):
    # Inicializing users
    #users = initialize_users(number_of_users, config.skills, config.tasks_number)

    # Initialize recommender
    recommender = initialize_recommender(config.skills, config.tasks_number, adaptative_mode)

    # Run the simulation
    simulate_iterations(num_iterations, stage, recommender)
    stage.reset_users()

    # Get the results
    statistics = get_statistics(recommender.github.tasks, config.skills)
    #users_parameters = get_users_parameters(users)

    # Show the results
    #print "Completed tasks: %d  Pending tasks: %d" % (statistics["completed tasks"], statistics["pending tasks"])
    # print_statistics(statistics)
    # print_user_parameters(users_parameters)

    return statistics

def run_several_simulations(num_simulations, num_iterations, adaptative_mode, stage):
    print_simulation_header(adaptative_mode, num_iterations)
    statistics = []
    for i in range(1,num_simulations+1):
        #print "Simulation %d of %d" % (i, num_simulations)
        result = run_simulation(num_iterations, adaptative_mode, stage)
        #result = run_simulation(config, num_iterations, num_users, adaptative)
        statistics.append(result)
    return statistics

def add_stage(user_types):
    stage = Stage(config)
    stage.initialize_users(user_types)
    stages.append(stage)

def generate_stages():
    user_types1 = [1, 2, 3, 4, 5]
    user_types2 = [1, 1, 1, 2, 3]
    user_types3 = [1, 1, 1, 1, 1]

    add_stage(user_types1)
    add_stage(user_types2)
    add_stage(user_types3)


# Load config file
config = Config()

# Get user input
#number_of_users = int(raw_input("Number of users: "))
#num_users = 5
#iterations = int(raw_input("Select number of iterations: "))
num_iterations = 50
#adaptative = select_greedy_or_adaptative(raw_input("Greedy or adaptative task allocation? (g/a): "))
num_simulations = 20

# Create stages
stages = []
generate_stages()

for stage in stages:
    print "\n\nSimulation for %s" % stage.description()
    # Runing the simulations for adaptative and greedy task allocation
    adaptative_mode = False
    greedy_statistics = run_several_simulations(num_simulations, num_iterations, adaptative_mode, stage)
    adaptative_mode = True
    adaptative_statistics = run_several_simulations(num_simulations, num_iterations, adaptative_mode, stage)

    # Comparing the results of greedy and adaptative simulations
    results = compare_statistics(greedy_statistics, adaptative_statistics)
    print_simulations_comparisions(results)
