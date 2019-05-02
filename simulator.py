from user import User
from Recommender import Recommender
from task import Task
from Config import Config
from GithubSimulator import GithubSimulator

config = Config()
user = User(config.user_name, config.password, config.tasks_number)
user.load_skills_from_file(config.skills)
simulator = GithubSimulator(user)
recommender = Recommender(user, simulator)

tasks = recommender.recommend_tasks()
for task in tasks:
    print "%d - %s. Skill required: %s" % (task.number, task.name, task.skill)
