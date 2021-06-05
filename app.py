from flask import Flask, request, redirect,url_for
from flaskwebgui import FlaskUI
from flask import render_template
import sqlite3
from sqlite3 import Error
import time

DEBUG = False
app = Flask(__name__)
ui = FlaskUI(app, start_server="flask", width=1000)

conn = sqlite3.connect('todo.db')
print("Opened Database successfully")

conn.execute("CREATE TABLE if not exists todos (pk INTEGER NOT NULL PRIMARY KEY ,task TEXT ) ")
print("Table created Successfully ")


x = "Hi this is your first Task to be Done"
# for i in range(10):
#     l1[i] = x
l1 = {}

@app.route("/")
def hello():
    time.sleep(1)
    con = sqlite3.connect('todo.db')
    con.row_factory = sqlite3.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM todos")
    row=cur.fetchall()

    for x in row:
        print(x[0],x[1])
        l1[x[0]]=x[1]
    return render_template('index.html', l=l1)


@app.route('/add', methods=["POST"])
def add():
    toadd=request.form.to_dict()
    task = toadd["toadd"]
    con=sqlite3.connect('todo.db')
    try:
        cur=con.cursor()
        cur.execute('''INSERT INTO todos(task) VALUES(?)''', ( task, ))
        con.commit()
        print("Record Successfully saved")
    except Error as e :
        print(e)
        con.rollback()
    return render_template("index.html")

@app.route("/delete", methods=["GET", "POST"])
def delete():
    print(request.values)
    z = request.form.to_dict()
    todelete = list(map(int, z['delete'].split(',')))
    if todelete:

        for x in todelete:
            con = sqlite3.connect('todo.db')
            try:
                cur = con.cursor()
                cur.execute('''DELETE FROM todos WHERE pk=?''', (x,))
                con.commit()
                l1.pop(x)
            except Error as e:
                print("Error in delete occurred ")
                con.rollback()
                print(e)
    return render_template("index.html",l=l1)


if __name__ == "__main__":
    # app.run(debug=True)
    if DEBUG:
        # call the 'app' method with flask's parameters you need
        app.run(debug=True)
    else:
        ui.run()
