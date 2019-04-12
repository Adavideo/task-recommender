from user import User
from recommender import recommend_tasks
from task import Task
from Config import Config

skills = ["javascript", "css", "python", "django", "html"]

def load_default_config():
    config = Config()
    user_name, password, project = config.getConfig()
    user = User(user_name,password,5)
    user.config_test_user()
    return (user, project)

def select_user_skills():
    print "Let's config the programming languages you know. This will help filter the tasks to recommend you."
    new_user_skills = {}
    for skill in skills:
        know_skill = raw_input("Are you competent in %s (y/n): " % skill)
        new_user_skills[skill] = know_skill == "y" or know_skill == "Y"
    return new_user_skills

def create_user():
    print "Creating new user"
    user_name = raw_input("User name in github: ")
    user_pass = raw_input("Pasword in github: ")
    tasks_number = int(raw_input("How many task do you want to be recommend each time (5-20): "))
    user = User(user_name, user_pass, tasks_number)
    user_skills = select_user_skills()
    user.set_skills(user_skills)
    return user

def menu_tasks(user, project):
    print "-" * 50 + "\n"
    print "Recomending tasks from project %s for the user %s" % (project, user.name)
    tasks = recommend_tasks(project, user)
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
    user, project = load_default_config()
    option = ""
    while (option != "3"):
        print "The user is %s. The project is %s." % (user.name, project)
        print "\n" + "-" * 22
        print " 1 - Change user"
        print " 2 - Obtain recomendations"
        print " 3 - Exit\n"
        option = raw_input("Choose an option: ")
        if option == "1":
            user = create_user()
        elif option == "2":
            menu_tasks(user, project)
        elif option != "3":
            print "Option not valid."
        print "-" * 22 + "\n"

main_menu()
