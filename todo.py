import sqlite3
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route('/', methods = ['GET','POST'])
def main():
    try:
        with sqlite3.connect('todo.db') as todoDb:
            todoDbCursor = todoDb.cursor()
            getDataQuery = 'SELECT * FROM todo'
            fullDataGet = todoDbCursor.execute(getDataQuery).fetchall()
            if(fullDataGet):
                return render_template('todo.html', data = fullDataGet)
            return render_template('todo.html', data = '')

    except Exception as e:
                    return "Error : " + str(e)


@app.route('/post', methods = ['GET','POST'])
def post():
    if request.method == 'POST':
        todoTitle = request.form['todo-Title']
        if todoTitle == '':
            return "Do not leave the fields blank."
        if todoTitle.strip() == '':
            return "Do not leave the fields blank."

        try:
            with sqlite3.connect('todo.db') as todoDb:
                todoDbCursor = todoDb.cursor()
                createTableQuery = 'CREATE TABLE IF NOT EXISTS todo(id INTEGER PRIMARY KEY, todo_title TEXT, todo_state TEXT)'
                todoDbCursor.execute(createTableQuery)

                valueControlQuery = 'SELECT * FROM todo WHERE todo_title = ?'
                valueControl = [todoTitle.strip()]

                data = todoDbCursor.execute(valueControlQuery, valueControl).fetchone()
                if(data):
                    return "There is such a thing to do."
                    
                insertIntoQuery = 'INSERT INTO todo(todo_title,todo_state) VALUES(?,?)'
                insertIntoValues = [todoTitle,"Completed"]
                todoDbCursor.execute(insertIntoQuery, insertIntoValues)

                todoDb.commit()

        except Exception as e:
                return "Error : " + str(e)

        return redirect(url_for('main'))


@app.route('/update/<id>')
def updateGet(id):
    global ID
    ID = id

    return render_template('todo-update.html')


@app.route('/update', methods = ['GET','POST'])
def updatePost():
    if request.method == 'POST':
        newTodoTitle = request.form['new-todo-Title']
        if newTodoTitle == '':
            return "Do not leave the fields blank."
        if newTodoTitle.strip() == '':
            return "Do not leave the fields blank."

        try:
            with sqlite3.connect('todo.db') as todoDb:
                todoDbCursor = todoDb.cursor()
                createTableQuery = 'CREATE TABLE IF NOT EXISTS todo(id INTEGER PRIMARY KEY, todo_title TEXT, todo_state TEXT)'
                todoDbCursor.execute(createTableQuery)

                valueControlQuery = 'SELECT * FROM todo WHERE todo_title = ?'
                valueControl = [newTodoTitle.strip()]

                data = todoDbCursor.execute(valueControlQuery, valueControl).fetchone()
                if(data):
                    return "There is such a thing to do."

                with sqlite3.connect('todo.db') as todoDb:
                    todoDbCursor = todoDb.cursor()
                    updateQuery = 'UPDATE todo SET todo_title = ?, todo_state = ? WHERE id = ?'
                    todoDbCursor.execute(updateQuery, [newTodoTitle.strip(), "Completed(Updated)", ID])
                    todoDb.commit()

                    return redirect(url_for('main'))

        except Exception as e:
            return "Error : " + str(e)



@app.route('/delete/<id>')
def delete(id):
    try:
        with sqlite3.connect('todo.db') as todoDb:
            todoDbCursor = todoDb.cursor()
            deleteQuery = 'DELETE FROM todo WHERE id = ?'
            todoDbCursor.execute(deleteQuery, id)
            todoDb.commit()
            return redirect(url_for('main'))

    except Exception as e:
        return "Error : " + str(e)



@app.errorhandler(404)
def error(err):
    return "Page Not Found"


if __name__ == '__main__':
    app.run(debug=True, port=5000)

