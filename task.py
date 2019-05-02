class Task(object):

    def __init__(self, task_number, task_name, task_link, task_skill, assignee):
        self.number = task_number
        self.name = task_name
        self.link = task_link
        self.skill = task_skill
        self.assigned_to = assignee
        self.state = ""

    def update_status(self, state):
        self.state = state

    def set_description(self, description):
        self.description = description

    def assign(self, assignee):
        self.assigned_to = assignee

    def not_assigned(self):
        if self.assigned_to:
            return False
        else:
            return True
