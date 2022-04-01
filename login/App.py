from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter, sys
import mysql.connector


import main

def add():
    if bnum.get()=="":
        messagebox.showinfo("Error","Enter Number Plate",parent=root)
    
    else:
        main.add_blacklist(bnum.get())

def blacklist():
	root = Tk()
	root.geometry("700x250")
	root.title('Blacklist') 
	my_connect = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="u:nz48UV",
	  database="vehicle_number"
	)
	my_conn = my_connect.cursor()
	####### end of connection ####
	
	
	
	
	def remove_blacklist():

		def remove_plate():
		    try:
		        conn = mysql.connector.connect(host="localhost",
		                                       user="root",
		                                       password="u:nz48UV",
		                                       database="vehicle_number"
		                                       )
		        my_cursor = conn.cursor()
		        query= "delete from blacklist where numberplate = %s"
		        #val = blacklist_num1.get()
		        
		        #val = numplate1.get()
		        val = (numplate1.get(),)
		        
		        my_cursor.execute(query,val)
		        conn.commit()
		        conn.close()
		        
		        messagebox.showinfo("Success", numplate1.get() + " Removed Successfully")
		        
		        #messagebox.showinfo("Success", blacklist_num1.get() + "Removed Successfully")
		    except Exception as es:
		        messagebox.showerror("Error", f"Due to :{str(es)}")
		
		root = Tk()
		root.geometry("700x250")
		root.title('Blacklist') 
		
		numplate1 = Entry(root,textvariable='blacklist_num1', font=('times new roman', 18), bg='lightgray')
		numplate1.place(x=40, y=10, width=250)
		
		#numplate1 = Entry(root, textvariable=blacklist_num1)
		#numplate1.place(x=40, y=10)
		add = Button(root, text="Remove",command=remove_plate , cursor="hand2", bg="White")
		add.place(x=40, y=50, height=30, width=60)
	
	
	
	remove_btn = ttk.Button(root, text="remove",command=remove_blacklist)
	remove_btn.place(x=500,y=10 ,width =60, height= 25)
	
	
	
	
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
	
	
def whitelist():
	root = Tk()
	root.geometry("500x250")
	root.title('Whitelist') 
	my_connect = mysql.connector.connect(
	  host="localhost",
	  user="root",
	  passwd="u:nz48UV",
	  database="vehicle_number"
	)
	my_conn = my_connect.cursor()
	####### end of connection ####
	my_conn.execute("SELECT * FROM whitelist")
	e=Label(root,width=20,text='ID',borderwidth=2, relief='ridge',anchor='w',bg='green')
	e.grid(row=0,column=0)
	e=Label(root,width=20,text='numberplate',borderwidth=2, relief='ridge',anchor='w',bg='green')
	e.grid(row=0,column=1)
	e=Label(root,width=20,text='Date',borderwidth=2, relief='ridge',anchor='w',bg='green')
	e.grid(row=0,column=2)
	i=1
	for whitelist in my_conn: 
		for j in range(len(whitelist)):
			e = Entry(root, width=20, fg='blue') 
			e.grid(row=i, column=j) 
			e.insert(END, whitelist[j])
		i=i+1
	root.mainloop()



root = Tk()
root.geometry('1350x710+0+10')
root.title('Vehicle number plate scanning System')
bglogin = PhotoImage(file='loginbg.png')
bgloginLabel = Label(root, image=bglogin)
bgloginLabel.place(x=0, y=0)
#root['bg']='green'
root.resizable(False, False)

registerFrame = Frame(root, bg='white', width=650, height=650)
registerFrame.place(x=630, y=30)

titleLabel = Label(registerFrame, text='VNPSS', font=('arial', 22, 'bold '), bg='white',
                   fg='deep pink', )
titleLabel.place(x=200, y=5)


bnum = StringVar()
picture_btn = ttk.Button(root, text="Upload image", command=main.pic_recog)
picture_btn.place(x=100,y=100 ,width =100, height= 50)

Video_btn = ttk.Button(root, text="Video capture", command=main.video_recog)
Video_btn.place(x=220,y=100 ,width =100, height= 50)

username_entry = ttk.Entry(root, textvariable=bnum)
username_entry.place(x=100,y=230)
Add_blacklist = ttk.Button(root, text="Add to blacklist", command=add)
Add_blacklist.place(x=100,y=260 ,width =120, height= 50)

show_blacklist = ttk.Button(root, text="Show Blacklist", command=blacklist)
show_blacklist.place(x=100,y=320 ,width =110, height= 50)

show_blacklist = ttk.Button(root, text="Show whitelist", command=whitelist)
show_blacklist.place(x=220,y=320 ,width =110, height= 50)




#closebutton = Button(registerFrame, text='close', cursor='hand2', activebackground='red', activeforeground='white', command = end )
#closebutton.place(x=250, y=580,width =70, height= 30)



root.mainloop()


