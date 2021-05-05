from task import Task
from datetime import date
from flask import Flask, render_template, request, url_for, flash, redirect
from database import DataBase

app = Flask(__name__)


class Tasks:
    current_index_ = 0
    all_amount_ = 0
    undone_amount_ = 0
    current_task_ = Task()
    db = DataBase()

    def __init__(self):
        self.undone_tasks_ = self.db.undone_tasks()
        self.done_tasks_ = self.db.done_tasks()
        self.date_ = date.today()

    def get_current(self):
        frogs = []
        usual = []
        if not (self.date_ in self.undone_tasks_):
            return
        for i in range(self.current_index_, len(self.undone_tasks_[self.date_])):
            x = self.undone_tasks_[self.date_][i]
            if x.is_frog_:
                frogs.append(x)
            else:
                usual.append(x)
        for i in range(0, self.current_index_):
            x = self.undone_tasks_[self.date_][i]
            if x.is_frog_:
                frogs.append(x)
            else:
                usual.append(x)
        self.undone_amount_ = len(frogs) + len(usual)
        self.all_amount_ = self.undone_amount_ + (
            len(self.done_tasks_[self.date_]) if (self.date_ in self.done_tasks_) else 0)
        if len(frogs) > 0:
            self.current_task_ = frogs[len(frogs) - 1]
        else:
            self.current_task_ = usual[len(usual) - 1]

    def done(self):
        if not (self.date_ in self.done_tasks_):
            self.done_tasks_[self.date_] = []
        self.done_tasks_[self.date_].append(self.current_task_)
        self.db.add_old_task(self.current_task_)
        self.db.delete_task(self.current_task_)
        self.undone_tasks_[self.date_].remove(self.current_task_)
        self.undone_amount_ -= 1
        if not self.undone_tasks_[self.date_]:
            del self.undone_tasks_[self.date_]

    def delete(self, task):
        self.db.delete_task(task)
        self.undone_tasks_[task.date_].remove(task)
        if not self.undone_tasks_[task.date_]:
            del self.undone_tasks_[task.date_]

    def skip(self):  # false if frog, true otherwise
        if self.current_task_.is_frog_:
            return False
        self.current_index_ += 1
        self.current_index_ %= len(self.undone_tasks_[self.date_])

    def add(self, task):  # adds a new task in our database
        self.db.add_new_task(task)
        if task.date_ not in self.undone_tasks_:
            self.undone_tasks_[task.date_] = []
        self.undone_tasks_[task.date_].append(task)


task_db = Tasks()


@app.route('/', methods=('GET', 'POST'))
def index():
    global task_db
    task_db.date_ = date.today()
    task_db.get_current()
    if request.method == 'POST':
        if request.form['button'] == 'Skip':
            task_db.skip()
            return redirect(url_for('index'))
        if request.form['button'] == 'Done':
            task_db.done()
            return redirect(url_for('index'))
    return render_template('index.html', arg_current_task=task_db.current_task_,
                           arg_all_amount=task_db.all_amount_,
                           arg_undone_amount=task_db.undone_amount_, date=date.today())


@app.route('/add', methods=('GET', 'POST'))
def add():
    global task_db
    task_db.date_ = date.today()
    if request.method == 'POST':
        title = request.form['title']
        if request.form['IsFrog'] == "Frog":
            is_frog = True
        else:
            is_frog = False
        try:
            year, month, day = request.form['date'].split("-")
            date_ = date(int(year), int(month), int(day))
        except:
            return redirect(url_for('add'))
        new_task = Task(title_arg=title, date_arg=date_, is_frog_arg=is_frog)
        task_db.add(new_task)
        '''
        if not (new_task.date_ in undone_tasks):
            undone_tasks[new_task.date_] = []
        undone_tasks[new_task.date_].append(new_task)
        '''
        return redirect(url_for('add'))
    return render_template('add.html')


@app.route('/edit', methods=('GET', 'POST'))
def edit():
    if request.method == 'POST':
        global task_db
        task_db.date_ = date.today()
        val = request.form['button']
        date_cur, title, is_fr = val.split("$")
        year, month, day = date_cur.split("-")
        date_ = date(int(year), int(month), int(day))
        if is_fr == "True":
            is_frog = True
        else:
            is_frog = False
        cur_task = Task(title_arg=title, date_arg=date_, is_frog_arg=is_frog)
        task_db.delete(cur_task)
        return redirect(url_for('edit'))
    return render_template('edit.html', arg_undone_tasks=task_db.undone_tasks_)


@app.route('/about')
def about():
    return render_template('about.html')
