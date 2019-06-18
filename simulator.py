from Recommender import Recommender
from Config import Config
from GithubSimulator import GithubSimulator
from stage import Stage
import random

# Initialization

def initialize_recommender(adaptative_mode, tasks_probabilities):
    contributors = 5
    simulator = GithubSimulator(config, contributors, tasks_probabilities)
    recommender = Recommender(simulator, adaptative_mode)
    return recommender


# Extracting and preparing results

def get_statistics(recommender):
    tasks = recommender.github.tasks
    completed_tasks = 0
    pending_tasks = 0
    for task in tasks:
        if task.is_closed():
            completed_tasks += 1
        else:
            pending_tasks += 1
    return {"completed tasks":completed_tasks, "pending tasks":pending_tasks}

def calculate_simulations_average(simulations_statistics):
    num_simulations = len(simulations_statistics)
    total_completed_tasks = 0.0
    total_pending_tasks = 0.0
    for simulation_results in simulations_statistics:
        total_completed_tasks += simulation_results["completed tasks"]
        total_pending_tasks += simulation_results["pending tasks"]
    average_completed_tasks = total_completed_tasks / num_simulations
    average_pending_tasks = total_pending_tasks / num_simulations
    #print "average completed %f pending %f" % (average_completed_tasks, average_pending_tasks)
    return {"average_completed_tasks":average_completed_tasks, "average_pending_tasks": average_pending_tasks}

def calculate_improvement(greedy, adaptative):
    if greedy == 0.0:
        improvement = adaptative * 100
    else:
        improvement = (adaptative * 100 / greedy) - 100
    return improvement

def compare_statistics(greedy_simulations_statistics, adaptative_simulations_statistics):
    greedy_average_results = calculate_simulations_average(greedy_simulations_statistics)
    adaptative_average_results = calculate_simulations_average(adaptative_simulations_statistics)
    completed_tasks_improvement = calculate_improvement(greedy_average_results["average_completed_tasks"], adaptative_average_results["average_completed_tasks"])
    pending_tasks_improvement = calculate_improvement(greedy_average_results["average_pending_tasks"], adaptative_average_results["average_pending_tasks"])
    return {"completed_tasks":completed_tasks_improvement, "pending_tasks":pending_tasks_improvement}

def print_simulations_comparisions(results):
    print " - Adaptative completed %d%% more tasks than greedy" % results["completed_tasks"]
    pending = results["pending_tasks"] * -1
    print " - Had %d%% less pending tasks when finishing the simulation" % pending


# Simulation

def asign_random_task(user, tasks):
    number_of_tasks = len(tasks)
    task_number = random.randint(1,number_of_tasks)
    selected_task = tasks[task_number-1]
    selected_task.assign(user.name)
    user.assign(selected_task)
    return selected_task.skill

def simulate_user_behavior(user, recommender):
    if not user.working_on_task:
        recommended_tasks = recommender.recommend_tasks(user)
        if recommended_tasks:
            selected_task_type = asign_random_task(user, recommended_tasks)
            if recommender.adaptative == True:
                user.task_allocation.update_tasks_performance_method2(recommended_tasks, selected_task_type)
    else:
        user.work_on_task()

def simulate_iterations(iterations, stage, recommender):
    for i in range(1, iterations+1):
        recommender.github.update()
        for user in stage.users:
            simulate_user_behavior(user, recommender)

def run_simulation(num_iterations, adaptative_mode, stage):
    # Initialize recommender
    recommender = initialize_recommender(adaptative_mode, stage.tasks_probabilities)

    # Run the simulation
    simulate_iterations(num_iterations, stage, recommender)

    # Reset the users at the end of each simulation
    stage.reset_users()

    # Get the results
    statistics = get_statistics(recommender)
    return statistics

def run_several_simulations(num_simulations, num_iterations, adaptative_mode, stage):
    statistics = []
    for i in range(1, num_simulations+1):
        result = run_simulation(num_iterations, adaptative_mode, stage)
        statistics.append(result)
    return statistics

def generate_stages():
    user_types1 = [1, 2, 3, 4, 5]
    user_types2 = [1, 1, 1, 2, 3]
    user_types3 = [1, 1, 1, 1, 1]
    user_types = [user_types1, user_types2, user_types3]

    tasks_probabilities_set1 = [20, 20, 20, 20, 20]
    tasks_probabilities_set2 = [10, 10, 10, 10, 60]
    tasks_probabilities_set3 = [60, 10, 10, 10, 10]
    tasks_probabilities_list = [tasks_probabilities_set1, tasks_probabilities_set2, tasks_probabilities_set3]

    stages = []
    for user_type in user_types:
        for tasks_probabilities in tasks_probabilities_list:
            stage = Stage(config, user_type, tasks_probabilities)
            stages.append(stage)
    return stages

# Load config file
config = Config()
config.load_simulator_parametters()

# Create stages
stages = generate_stages()

print "The results show the eficiency of Adaptative Task Allocation compared with greedy task allocation."
print "It calculates an average of the tasks completed and the pending tasks on the simulations."

for stage in stages:
    print "\nSimulation for %s" % stage.description()
    # Runing the simulations for adaptative and greedy task allocation
    adaptative_mode = False
    greedy_statistics = run_several_simulations(config.simulations, config.iterations, adaptative_mode, stage)
    adaptative_mode = True
    adaptative_statistics = run_several_simulations(config.simulations, config.iterations, adaptative_mode, stage)

    # Comparing the results of greedy and adaptative simulations
    results = compare_statistics(greedy_statistics, adaptative_statistics)
    print_simulations_comparisions(results)
