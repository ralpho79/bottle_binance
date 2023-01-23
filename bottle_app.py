
# A very simple Bottle Hello World app for you to get started with...
import sqlite3
from bottle import default_app, route, error, template, request

application = default_app()

@route('/')
def hello_world():
    landing_site_1 = "<h2>Welcome to my Bottle To-Do list app!</h2>"
    landing_site_2 = "<p>The following routes are implemented: <p>"
    landing_site_3 = "<p><a href=/todo>todo list</a>"
    landing_site_4 = "<p><a href=/new>new item</a>"
    landing_site_5 = "<p><a href=/edit/1>edit item</a>"
    
    landing_site = landing_site_1+landing_site_2+landing_site_3+landing_site_4+landing_site_5
    return landing_site


@route('/todo')
def todo_list():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task FROM todo WHERE status LIKE '1'")
    result = c.fetchall()
    c.close()
    output = template('make_table', rows=result)
    return output

@route('/new', method='GET')
def new_item():

    if request.GET.save:

        new = request.GET.task.strip()
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()

        c.execute("INSERT INTO todo (task,status) VALUES (?,?)", (new,1))
        new_id = c.lastrowid

        conn.commit()
        c.close()

        return '<p>The new task was inserted into the database, the ID is %s</p>' % new_id
    else:
        return template('new_task.tpl')

@route('/edit/<no:int>', method='GET')
def edit_item(no):

    if request.GET.save:
        edit = request.GET.task.strip()
        status = request.GET.status.strip()

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("UPDATE todo SET task = ?, status = ? WHERE id LIKE ?", (edit, status, no))
        conn.commit()

        return '<p>The item number %s was successfully updated</p>' % no
    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no),))
        cur_data = c.fetchone()

        return template('edit_task', old=cur_data, no=no)

@error(404)
def error404(error):
    return 'Nothing here, sorry, aka 404'
