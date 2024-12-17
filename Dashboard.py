class Dashboard:
    def __init__(self,master, user_id):
        self.master = master
        self.user_id = user_id

    def show_dashboard(self):
        print(f"Welcome to the {self.__class__.__name__}!")