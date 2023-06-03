class Server:
    def __init__(self, id, user_email, user_password, server_uri, server_name, calendar_name,
                 tasks=None, sizes=None, statuses=None, types=None, priorities=None):
        self.id = id
        self.user_email = user_email
        self.user_password = user_password
        self.server_uri = server_uri
        self.server_name = server_name
        self.calendar_name = calendar_name
        self.sizes = sizes
        self.statuses = statuses
        self.priorities = priorities
        self.sizes = sizes
        self.tasks = tasks
