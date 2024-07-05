class Session:
    __instance = None

    def __init__(self):
        if Session.__instance is not None:
            raise Exception("Невозможно создать несколько экземпляров класса Session")
        else:
            Session.__instance = self
            self.username = None
            self.role = None
            self.current_date = None
            self.work_date = None

    @staticmethod
    def get_instance():
        if Session.__instance is None:
            Session()
        return Session.__instance

    def set_username_role_date(self, username, role, current_date):
        self.username = username
        self.role = role
        self.current_date = current_date

    def set_work_date(self, work_date):
        self.work_date = work_date

    def get_role(self):
        return self.role

    def get_username(self):
        return self.username

    def get_current_date(self):
        return self.current_date

    def get_work_date(self):
        return self.work_date