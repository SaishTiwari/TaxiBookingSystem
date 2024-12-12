class Dashboard:
    def __init__(self, user_id):
        self.user_id = user_id

    def show_dashboard(self):
        print(f"Welcome to the {self.__class__.__name__}!")