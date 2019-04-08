class Task(object):

    def __init__(self, task_name, created_at, task_link, task_skill):
        self.name = task_name
        self.link = task_link
        self.skill = task_skill
        self.state = ""
        self.created_at = created_at
        self.updated_at = ""
        self.description = ""


    def set_description(self, description):
        self.description = description


    def update_status(self, state, updated_at):
        self.state = state
        self.updated_at = updated_at
