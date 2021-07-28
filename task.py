from datetime import date


class Task:
    title_ = str("None")
    # description_ = str()
    date_ = date(2002, 3, 26)
    is_frog_ = bool()

    def __init__(self, title_arg="Task", date_arg=date(2002, 3, 26),
                 is_frog_arg=False):
        self.title_ = title_arg
        # self.description_ = description_arg
        self.date_ = date_arg
        self.is_frog_ = is_frog_arg

    def __repr__(self):
        return repr(self.title_ + str(self.date_) + str(self.is_frog_))

    def __eq__(self, other):
        return self.title_ == other.title_ and self.date_ == other.date_ and self.is_frog_ == other.is_frog_
