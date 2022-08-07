from datetime import datetime
import sqlite3

conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

# create a db
cursor.execute("""CREATE TABLE IF NOT EXISTS todo(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creation_date TEXT NOT NULL,
                deadline TEXT,
                task TEXT NOT NULL)""")


# create todo class
class Todo:
    def __init__(self, text, deadline):
        self.text = text
        self.deadline = deadline
        self.date = datetime.now()

    def __str__(self):
        if self.deadline is None:
            return f'creation date:{self.date.strftime("%d/%m/%Y %H:%M")} \n Deadline: None \n Todo: {self.text}'
        else:
            return f'creation date:{self.date.strftime("%d/%m/%Y %H:%M")} \n Deadline: {self.deadline.strftime("%d/%m/%Y %H:%M")} \n Todo: {self.text} '


# create db class to make operations on a todo list
class ToDoDatabase:

    def __init__(self):
        self.date = datetime.now()

    def add_to_db(self, task):
        if task.deadline is None:
            cursor.execute("""INSERT INTO todo(creation_date, deadline, task)
                                VALUES (?, ?, ?)""", (str(self.date.strftime("%d/%m/%Y %H:%M")),
                                                      "None",
                                                      task.text))
        else:
            cursor.execute("""INSERT INTO todo(creation_date, deadline, task)
                                VALUES (?, ?, ?)""", (str(self.date.strftime("%d/%m/%Y %H:%M")),
                                                      str(task.deadline.strftime("%d/%m/%Y %H:%M")),
                                                      task.text))
        conn.commit()

    def fetch_all(self):
        cursor.execute("""SELECT * FROM todo""")
        tasks = cursor.fetchall()
        return tasks

    def update_db(self, old_task, new_task):
        if new_task.deadline is None:
            cursor.execute(f'''UPDATE todo
                            SET creation_date = "{self.date.strftime("%d/%m/%Y %H:%M")}",
                                deadline = "None",
                                task = "{new_task.text}"
                            WHERE
                                id = {old_task}''')
        else:
            cursor.execute(f'''UPDATE todo
                            SET creation_date = "{self.date.strftime("%d/%m/%Y %H:%M")}",
                                deadline = "{new_task.deadline.strftime("%d/%m/%Y %H:%M")}",
                                task = "{new_task.text}"
                            WHERE
                                id = {old_task}''')
        conn.commit()

    def check_db(self):
        cursor.execute("""SELECT * FROM todo""")
        tasks = cursor.fetchall()
        count_task = 0
        for i in tasks:
            count_task += 1
        return bool(count_task)  # returns 1 if todo is not empty.

    def delete_task(self, task_id):
        cursor.execute(f'''DELETE FROM todo
                        WHERE id = {task_id}''')
        conn.commit()

# create a manager class, helper class for making operations
class DBManager:

    def __init__(self, database):
        self.database = database

    def add(self, task):
        self.database.add_to_db(task)

    def update(self, old_task, new_task):
        self.database.update_db(old_task, new_task)

    def count_tasks(self):
        return self.database.fetch_all()[-1][0]

    def check_id(self):
        task_list = []
        for i in range(len(self.database.fetch_all())):
            task_list.append(self.database.fetch_all()[i][0])
        return task_list

    def show_tasks(self):
        data = self.database.fetch_all()
        for task in data:
            print(task)

    def check_list(self):
        return self.database.check_db()

    def delete_task(self, task_id):
        return self.database.delete_task(task_id)


def check_input_data(db_manager):
    if not db_manager.check_list():
        print("\n Database is Empty! ")
    else:
        while True:
            db_manager.show_tasks()

            print("You can either go back to menu(by entering 'exit' or enter task id to continue")

            task_id = input("task id: ")
            if task_id.lower() == 'exit':
                return task_id

            if not task_id.isdigit():
                print("\n Please enter the digit!")
                continue

            elif int(task_id) > db_manager.count_tasks():
                print("\n Task ID out of range!")
                continue

            elif int(task_id) not in db_manager.check_id():
                print("\n entered ID is incorrect!")
                continue

            task_index = int(task_id)

            return task_index

# function to format dates that can be entered
def format_date():
    deadline_input = input("input deadline in a format(YYYY,MM,DD,HH,MM): ")
    deadline_format = deadline_input.split(',')
    deadline = datetime(int(deadline_format[0]), int(deadline_format[1]), int(deadline_format[2]), int(deadline_format[3]), int(deadline_format[4]))

    return deadline

def check_date():
    check = True
    while check:
        try:
            deadline = format_date()
            check = False
            return deadline
        except(ValueError, IndexError) as msg:
            print(msg)

# create a menu with basic components that an user can make
# opers: add task, edit task, delete task, show tasks

def main_menu():
    choice = None

    db = ToDoDatabase()
    db_manager = DBManager(db)

    # let's look at choices (user can write q for quit)
    while choice != 'q':
        print('\n Todo list menu: \n',
              '1. Add a new task \n',
              '2. Edit an existing task \n',
              '3. Delete a task \n',
              '4. Show all tasks \n',
              '5. Type q or Q for quit \n')

        choice = input("enter your choice \n").lower()

        if choice == "1":
            task = input("Type q for quit or enter task description \n")
            if task =="exit":
                continue

            has_deadline = input("has the task got deadline? type yes or no: \n")
            if has_deadline.lower() == "yes":
                deadline = check_date()
            else:
                deadline = None

            task = Todo(task, deadline)
            db_manager.add(task)

        elif choice == '2':
            old_task = check_input_data(db_manager)

            if old_task == "exit":
                continue
            else:
                task = input("new task: ")

                has_deadline = input("has the task got deadline? type yes or no: ")
                if has_deadline.lower() == "yes":
                    deadline = check_date()
                else:
                    deadline = None

                new_task = Todo(task, deadline)
                db_manager.update(old_task, new_task)
        elif choice == '3':
            task_id = check_input_data(db_manager)

            if task_id == 'exit':
                continue
            else:
                db_manager.delete_task(task_id)
        elif choice == '4':
            if db_manager.check_list():
                db_manager.show_tasks()
            else:
                print("Database is empty!")
        elif choice == 'q':
            print("See you!")
        else:
            print("Incorrect choice, please choose from: 1,2,3,4 or q")

main_menu()
cursor.close()
conn.close()






