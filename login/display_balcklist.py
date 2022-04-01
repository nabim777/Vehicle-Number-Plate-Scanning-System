import mysql.connector
import tkinter  as tk 
from tkinter import * 
root = tk.Tk()
root.geometry("500x250")
root.title('Blacklist') 
my_connect = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="u:nz48UV",
  database="vehicle_number"
)
my_conn = my_connect.cursor()
####### end of connection ####
my_conn.execute("SELECT * FROM blacklist")
e=Label(root,width=20,text='ID',borderwidth=2, relief='ridge',anchor='w',bg='green')
e.grid(row=0,column=0)
e=Label(root,width=20,text='numberplate',borderwidth=2, relief='ridge',anchor='w',bg='green')
e.grid(row=0,column=1)
e=Label(root,width=20,text='Date',borderwidth=2, relief='ridge',anchor='w',bg='green')
e.grid(row=0,column=2)
i=1
for blacklist in my_conn: 
    for j in range(len(blacklist)):
        e = Entry(root, width=20, fg='blue') 
        e.grid(row=i, column=j) 
        e.insert(END, blacklist[j])
    i=i+1
root.mainloop()
