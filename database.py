import sqlite3
from task import Task
from datetime import date


def string_to_date(arg):
    year, month, day = arg.split("-")
    return date(int(year), int(month), int(day))


class DataBase:
    database_ = "database.db"

    def __init__(self):
        with sqlite3.connect(self.database_) as conn:
            with open("schema.sql") as f:
                conn.executescript(f.read())


    def add_new_task(self, task):
        with sqlite3.connect(self.database_) as conn:
            cur = conn.cursor()
            if len(cur.execute("SELECT title from undone_tasks where title =?",
                               (str(task.title_),)).fetchall()) == 0:
                cur.execute("INSERT into undone_tasks (time, title, is_frog) VALUES (?, ?, ?)", (str(task.date_),
                                                                                                 str(task.title_),
                                                                                                 '1' if task.is_frog_ else '0'))
            conn.commit()

    def add_old_task(self, task):
        with sqlite3.connect(self.database_) as conn:
            cur = conn.cursor()
            if len(cur.execute("SELECT title from done_tasks where title =?",
                               (str(task.title_),)).fetchall()) == 0:
                cur.execute("INSERT into done_tasks (time, title, is_frog) VALUES (?, ?, ?)", (str(task.date_),
                                                                                               str(task.title_),
                                                                                               '1' if task.is_frog_ else '0'))
            conn.commit()

    def undone_tasks(self):
        return_value = dict()
        with sqlite3.connect(self.database_) as conn:
            cur = conn.execute("SELECT * FROM undone_tasks").fetchall()
            for x in cur:
                date1 = string_to_date(x[1])
                title = x[2]
                is_frog = True if x[3] == '1' else False
                if date1 not in return_value:
                    return_value[date1] = []
                return_value[date1].append(Task(title_arg=title, date_arg=date1, is_frog_arg=is_frog))
        return return_value

    def done_tasks(self):
        return_value = dict()
        with sqlite3.connect(self.database_) as conn:
            cur = conn.execute("SELECT * FROM done_tasks").fetchall()
            for x in cur:
                date1 = string_to_date(x[1])
                title = x[2]
                is_frog = True if x[3] == '1' else False
                if date1 not in return_value:
                    return_value[date1] = []
                return_value[date1].append(Task(title_arg=title, date_arg=date1, is_frog_arg=is_frog))
        return return_value

    def delete_task(self, task):
        with sqlite3.connect(self.database_) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM done_tasks WHERE title =?", (task.title_, ))
            conn.commit()
