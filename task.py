from datetime import date


class Task:
    title_ = str("None")
    # description_ = str()
    date_ = date(2002, 3, 26)
    is_frog_ = bool()

    def __init__(self, title_arg="Task", description_arg="None", date_arg=date(2002, 3, 26),
                 is_frog_arg=False):
        self.title_ = title_arg
        # self.description_ = description_arg
        self.date_ = date_arg
        self.is_frog_ = is_frog_arg
