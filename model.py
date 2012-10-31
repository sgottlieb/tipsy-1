"""
model.py
"""
import sqlite3 
import datetime


def connect_db():
    return sqlite3.connect("tipsy.db")

def get_from_table_by_id(db, table_name, id, make_dict_fn):
    c = db.cursor()
    query_template = """SELECT * from %s WHERE id = ?"""
    query = query_template%table_name
    c.execute(query, (id,))
    row = c.fetchone()
    if row:
        return make_dict_fn(row)
    return None

class User(object):
    COLS = ['id', 'email', 'password', 'username']
    TABLE_NAME = "Users"
    def __init__(self, id, email, password, name):
        self.id = id
        self.email = email
        self.password = password
        self.name = name

    @classmethod
    def new(cls, db, email, password, name): 
        vals = [email, password, name]
        return insert_into_db(db, cls.TABLE_NAME, cls.COLS, vals)

    @classmethod
    def make(row):
        return User(row[0], row[1], row[2], row[3])

    @classmethod   
    def authenticate(cls, db, email, password):
        c = db.cursor()
        query = """SELECT * from %s WHERE email=? AND password=?"""%(cls.TABLE_NAME)
        c.execute(query, (email, password))
        result = c.fetchone()
        if result:
            return cls(*result)
        return None

    @classmethod
    def get_user(cls, db, user_id):
        return get_from_table_by_id(db, cls.TABLE_NAME, user.id, User.make)

    @classmethod
    def get_tasks(cls, db, user_id=None):
        """Get all the tasks matching the user_id, getting all the tasks in the system if the user_id is not provided. Returns the results as a list of dictionaries."""
        c = db.cursor()
        if user_id:
            query = """SELECT * from Tasks WHERE user_id = ?"""
            c.execute(query, (user_id, ))
        else:
            query = """SELECT * from Tasks"""
            c.execute(query)
        tasks = []
        rows = c.fetchall()
        for row in rows:
            task = Task.make(row)
            tasks.append(task)

        return tasks


class Task(object):
    COLS = ["id", "title", "created_at", 'completed_at', "user_id"]
    TABLE_NAME = "Tasks"
    def __init__(self, id, title, created_at, completed_at, user_id):
            self.title = title
            self.id = id
            self.created_at = created_at
            self.completed_at = completed_at
            self.user_id = user_id

    @classmethod
    def new(cls,db, title, user_id = None): 
        vals = [title, datetime.datetime.now(), None, user_id]
        return insert_into_table(db, cls.TABLE_NAME, cls.COLS, vals )

    @classmethod
    def make(cls, row):
        return Task(row[0], row[1], row[2], row[3], row[4])


    @classmethod
    def get_task(cls, db, task_id):
        return get_from_table_by_id(db, cls.TABLE_NAME,  task.id, Task.make)

    @classmethod
    def complete(cls, db, task_id):
        c = db.cursor()
        query = """UPDATE Tasks SET completed_at=DATETIME('now') WHERE id=?"""
        res = c.execute(query, (task_id,))
        if res:
            db.commit()
            return res.lastrowid
        else:
            return None

def insert_into_table(db, table_name, columns, values):
    c = db.cursor()
    query_template = """INSERT into %s values (%s)"""
    num_cols = len(columns)
    q_marks = ", ".join(["NULL"] + (["?"] * (num_cols-1)))
    query = query_template%(table_name, q_marks)
    res = c.execute(query, tuple(values))
    if res:
        db.commit()
        return res.lastrowid

# def get_tasks(db, user_id=None):
#     """Get all the tasks matching the user_id, getting all the tasks in the system if the user_id is not provided. Returns the results as a list of dictionaries."""
#     c = db.cursor()
#     if user_id:
#         query = """SELECT * from Tasks WHERE user_id = ?"""
#         c.execute(query, (user_id, ))
#     else:
#         query = """SELECT * from Tasks"""
#         c.execute(query)
#     tasks = []
#     rows = c.fetchall()
#     for row in rows:
#         task = Task.make(row)
#         tasks.append(task)

#     return tasks


#get functions

# def get_from_table_by_id(db, table_name, id, make_dict_fn):
#     c = db.cursor()
#     query_template = """SELECT * from %s WHERE id = ?"""
#     query = query_template%table_name
#     c.execute(query, (id,))
#     row = c.fetchone()
#     if row:
#         return make_dict_fn(row)
#     return None

# def get_user(db, user_id):
#     return get_from_table_by_id(db, "Users", user_id, make_user)

# def get_task(db, task_id):
#     return get_from_table_by_id(db, "Tasks", task_id, make_task)

#new functions
# def new_user(db, email, password, name):
#     vals = [email, password, name]            
#     USER_COLS = ["id", "email", "password", "username"]
#     return insert_into_table(db, "Users", USER_COLS, vals)
    
# def new_task(db, title, user_id = None):
#     vals = [title, datetime.datetime.now(), None, user_id]
#     TASK_COLS = ["id", "title", "created_at", 'completed_at', "user_id"]
#     return insert_into_table(db, "Tasks", TASK_COLS, vals )


    # fields = ["id", "email", "password", "username"]
    # return dict(zip(fields, row))

# def authenticate(db, email, password):
#     c = db.cursor()
#     query = """SELECT * from Users WHERE email=? AND password=?"""
#     c.execute(query, (email, password))
#     result = c.fetchone()
#     if result:
#         fields = ["id", "email", "password", "username"]
#         return make_user(result)
#     return None



# def complete_task(db, task_id):
#     """Mark the task with the given task_id as being complete."""
#     c = db.cursor()
#     query = """UPDATE Tasks SET completed_at=DATETIME('now') WHERE id=?"""
#     res = c.execute(query, (task_id,))
#     if res:
#         db.commit()
#         return res.lastrowid
#     else:
#         return None

# def get_tasks(db, user_id=None):
#     """Get all the tasks matching the user_id, getting all the tasks in the system if the user_id is not provided. Returns the results as a list of dictionaries."""
#     c = db.cursor()
#     if user_id:
#         query = """SELECT * from Tasks WHERE user_id = ?"""
#         c.execute(query, (user_id, ))
#     else:
#         query = """SELECT * from Tasks"""
#         c.execute(query)
#     tasks = []
#     rows = c.fetchall()
#     for row in rows:
#         task = Task.make(row)
#         tasks.append(task)

#     return tasks


# def make_task(row):
#     columns = ["id", "title", "created_at", "completed_at", "user_id"]
#     return dict(zip(columns, row))
