from user import User
from Recommender import Recommender
from task import Task
from Config import Config


def select_user_skills():
    print "Let's config the programming languages you know. This will help filter the tasks to recommend you."
    new_user_skills = {}
    for skill in config.get_skills():
        know_skill = raw_input("Are you competent in %s (y/n): " % skill)
        new_user_skills[skill] = know_skill == "y" or know_skill == "Y"
    return new_user_skills

def menu_config_user_skills():
    user_skills = select_user_skills()
    config.user.initialize_skills(config.get_skills(), user_skills)

def menu_tasks():
    print "-" * 50 + "\n"
    tasks = recommender.recommend_tasks()
    if tasks:
        counter = 1
        for task in tasks:
            print "%d - %s. Skill required: %s" % (counter, task.name, task.skill)
            counter += 1
        selection = int(raw_input("Select a task: "))
        task = tasks[selection-1]
        print "You have selected the task %s" % task.name
        print "Here is the link: " + task.link
        print task.description
    else:
        print "Sorry. No tasks."

def main_menu():
    option = ""
    while (option != "3"):
        print "\n" + "-" * 22
        print " 1 - Configure user skills"
        print " 2 - Obtain recomendations"
        print " 3 - Exit\n"
        option = raw_input("Choose an option: ")
        if option == "1":
            menu_config_user_skills()
        elif option == "2":
            menu_tasks()
        elif option != "3":
            print "Option not valid."
        print "-" * 22 + "\n"

config = Config()
recommender = Recommender(config.user)
main_menu()
