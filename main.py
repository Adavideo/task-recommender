from user import User
from recommender import recommend_tasks
from task import Task

skills = ["javascript", "css", "python", "django", "html"]

def select_user_skills():
    print "Let's config the programming languages you know. This will help filter the tasks to recommend you."
    new_user_skills = {}
    for skill in skills:
        know_skill = raw_input("Are you competent in %s (y/n): " % skill)
        new_user_skills[skill] = know_skill == "y" or know_skill == "Y"
    return new_user_skills

def create_user():
    print "Creando un usuario"
    user_name = raw_input("User name in github: ")
    user_pass = raw_input("Pasword in github: ")
    tasks_number = int(raw_input("How many task do you want to be recommend each time (5-20): "))
    user = User(user_name, user_pass, tasks_number)
    user_skills = select_user_skills()
    user.set_skills(user_skills)
    return user

def select_user():
    print "Seleccionando un usuario"
    user = User("","",0)
    user.config_mock_user()
    return user

def menu_user():
    print "\n" + "-" * 22
    print " 1 - Create new user"
    print " 2 - Select user\n"
    option = raw_input("Choose an option: ")
    if option == "1":
        user = create_user()
    elif option == "2":
        user = select_user()
    else:
        print "Option not valid."
        user = menu_user()
    print "-" * 22 + "\n"
    return user

def select_project():
    return "Adavideo/test-project"
    print "1- Brown Dispatcher"
    print "2- IPFS"
    print "3- Test project"
    option = raw_input("Choose an option: ")
    if option == "1":
        project = "llopv/BrownDispatcher"
    elif option == "2":
        project = "ipfs/go-ipfs"
    else:
        project = "Adavideo/test-project"
    return project

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
    user = select_user() # menu_user()
    project = select_project()
    print "The user is %s. The project is %s." % (user.name, project)
    menu_tasks(user, project)

main_menu()
