from task import Task
from datetime import date
import PySimpleGUI as sg
import webbrowser
import tkinter.font

class GraphicsApp:
    undone_tasks_ = dict()
    done_tasks_ = dict()

    def __init__(self):
        self.undone_tasks_ = dict()
        self.done_tasks_ = dict()

    def __add_task(self):
        layout1 = [[sg.Text("Write the task title:")], [sg.InputText()], [sg.Button("Next")]]
        window1 = sg.Window("To-Do app", layout1, resizable=True)
        while True:
            event, values = window1.read()
            if event == sg.WIN_CLOSED:
                return
            if event == "Next":
                break
        new_task = Task()
        new_task.title_ = values[0]
        window1.close()
        date_list = sg.popup_get_date()
        new_task.date_ = date(date_list[2], date_list[0], date_list[1])
        str1 = "Is it a frog?" # + emoji.emojize(':frog:')
        layout2 = [[sg.Text(str1)],
                   [sg.Text("About 'Eat the frog' method.", text_color='#0645AD',
                    enable_events=True, key='-LINK-')],
                   [sg.Button("Yes")],
                   [sg.Button("No")]]
        window2 = sg.Window("To-Do app", layout2, resizable=True)
        while True:
            event, values = window2.read()
            if event == sg.WIN_CLOSED:
                return
            if event == '-LINK-':
                webbrowser.open(r'https://todoist.com/productivity-methods/eat-the-frog')
            if event == "Yes":
                new_task.is_frog_ = True
                break
            if event == "No":
                new_task.is_frog_ = False
                break
        window2.close()
        if not (new_task.date_ in self.undone_tasks_):
            self.undone_tasks_[new_task.date_] = []
        self.undone_tasks_[new_task.date_].append(new_task)

    def __current(self):
        current_index = 0
        is_open = False
        while True:
            today = date.today()
            frogs = []
            usual = []
            if not (today in self.undone_tasks_):
                sg.popup("Hooray! No tasks for today! You can chill and enjoy your life.")
                if is_open:
                    window.close()
                break
            for i in range(current_index, len(self.undone_tasks_[today])):
                x = self.undone_tasks_[today][i]
                if x.is_frog_:
                    frogs.append(x)
                else:
                    usual.append(x)
            for i in range(0, current_index):
                x = self.undone_tasks_[today][i]
                if x.is_frog_:
                    frogs.append(x)
                else:
                    usual.append(x)
            undone_amount = len(frogs) + len(usual)
            all_amount = undone_amount + (len(self.done_tasks_[today]) if (today in self.done_tasks_) else 0)
            layout = [[sg.Text("Today is " + str(today))]]
            if undone_amount == 0:
                sg.popup("Congratulations! You have done all tasks for today!")
                if is_open:
                    window.close()
                break
            else:
                layout.append([sg.Text(f'You have completed {all_amount - undone_amount} from {all_amount} tasks today.'
                                       f' Good work!')])
            if len(frogs) > 0:
                current_task = frogs[len(frogs) - 1]
            else:
                current_task = usual[len(usual) - 1]
            layout.append([sg.Text("Current task:")])
            layout.append([sg.Text(current_task.title_, font=tkinter.font.ITALIC)])
            layout.append([sg.Text("Is frog?")])
            # print("Is frog?", emoji.emojize(':frog:'), end="")
            if current_task.is_frog_:
                layout.append([sg.Text("Yes", text_color='#00FF00')])
            else:
                layout.append([sg.Text("No", text_color='#FF0000')])
            layout.append([sg.Button("Done")])
            layout.append([sg.Button("Skip")])
            layout.append([sg.Button("Return")])
            window = sg.Window("Current wokflow", layout, resizable=True)
            is_open = True
            event, value = window.read()
            if event == "Done":
                if not (today in self.done_tasks_):
                    self.done_tasks_[today] = []
                self.done_tasks_[today].append(current_task)
                self.undone_tasks_[today].remove(current_task)
                if not self.undone_tasks_[today]:
                    del self.undone_tasks_[today]
                window.close()
                is_open = False
                continue
            if event == "Skip":
                if current_task.is_frog_:
                    sg.popup("You can't skip the frog!")
                    window.close()
                    continue
                current_index += 1
                current_index %= len(self.undone_tasks_[today])
                is_open = False
                window.close()
                continue
            if event == "Return" or event == sg.WIN_CLOSED:
                window.close()
                is_open = False
                break

    def __manage(self):
        date_list = sg.popup_get_date()
        find_date = date(date_list[2], date_list[0], date_list[1])
        if not (find_date in self.undone_tasks_):
            sg.popup("No tasks at this date!")
            return
        current_tasks = self.undone_tasks_[find_date]
        is_open = False
        while True:
            if len(current_tasks) == 0:
                del self.undone_tasks_[find_date]
                sg.popup("No tasks left for today!")
                if is_open:
                    window.close()
                return
            layout = [[sg.Text("Tasks for " + str(find_date))]]
            i = 0
            for task in current_tasks:
                i += 1
                temp = [sg.Text(str(i) + ")"), sg.Text(task.title_, font=tkinter.font.ITALIC), sg.Text("Is frog? ")]
                if task.is_frog_:
                    temp.append(sg.Text("Yes", text_color='#00FF00'))
                else:
                    temp.append(sg.Text("No", text_color='#FF0000'))
                temp.append(sg.Button("Delete", key=i))
                layout.append(temp)
            layout.append([sg.Button("Return")])
            window = sg.Window("Manage", layout)
            is_open = True
            event, value = window.read()
            if event == "Return" or sg.WIN_CLOSED:
                window.close()
                return
            print(event)
            if 1 <= event <= len(current_tasks):
                self.undone_tasks_[find_date].pop(event - 1)
                sg.popup("Task was successfully deleted.")
                window.close()
                is_open = False
                continue


    def run(self):
        layout = [[sg.Text("Choose what to do:")], [sg.Button("Add task")], [sg.Button("Current tasks")],
                  [sg.Button("Manage tasks")]]
        menu_window = sg.Window("To-Do app", layout, resizable=True)
        while True:
            event, values = menu_window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == "Add task":
                menu_window.hide()
                self.__add_task()
            if event == "Current tasks":
                menu_window.hide()
                self.__current()
            if event == "Manage tasks":
                menu_window.hide()
                self.__manage()
            menu_window.UnHide()
        menu_window.close()
