from tkinter import *
import sqlite3

root = Tk()
root.title('Lista de Tareas')
root.geometry('400x400')

conn = sqlite3.connect('tareas.db')

c = conn.cursor()

c.execute("""
    CREATE TABLE if not exists tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        completed BOOLEAN NOT NULL
    );
""")

conn.commit()


def remove(id):
    def _remove():
        c.execute("DELETE FROM tareas WHERE id = ?", (id, ))
        conn.commit()
        renderTarea()

    return _remove

#currying! Retrazamos la ejecución de una función
def complete(id):
    def _complete():
        tarea = c.execute("SELECT * from tareas WHERE id = ?", (id, )).fetchone()
        c.execute("UPDATE tareas SET completed = ? WHERE id = ?", (not tarea[3], id))
        conn.commit()
        renderTarea()


    return _complete

def renderTarea():
    rows = c.execute("SELECT * FROM tareas").fetchall()
    
    for widget in frame.winfo_children():
        widget.destroy()
        
    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows [i][2]
        color = 'white' if completed else 'black'
        l = Checkbutton(frame, text=description,fg='black', width=42, anchor='w', command= complete(id))
        l.grid(row=i, column=0, sticky='w')
        btn = Button(frame, text='Eliminar' , command=remove(id))
        btn.grid(row=i, column=1)
        l.select() if completed else l.deselect()

def addTarea():
    tarea = e.get()
    if tarea:
        c.execute("""
                    INSERT INTO tareas (description, completed) VALUES (?, ?)
                """, (tarea, False))
        conn.commit()
        e.delete(0, END)
        renderTarea()
    
    else:
        pass

l = Label(root, text='Tarea')
l.grid(row=0, column=0)

e = Entry(root, width=40)
e.grid(row=0, column=1)

btn = Button(root, text='Agregar', command=addTarea)
btn.grid(row=0, column=2)

frame = LabelFrame(root, text='Mis Tareas', padx=5, pady=5, fg='black')
frame.grid(row=1, column=0, columnspan=3, sticky='nswe', padx=5)

e.focus()

root.bind('<Return>', lambda x: addTarea())
renderTarea()
root.mainloop()