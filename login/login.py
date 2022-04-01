from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.messagebox import *
import pymysql


def forget_password():
    def reset():
        securityquescombo.current(0)
        newpassEntry.delete(0, END)
        answerforgetEntry.delete(0, END)
        mailentry.delete(0, END)
        passentry.delete(0, END)

    def reset_password():
        if securityquescombo.get() == 'Select' or answerforgetEntry.get() == '' or newpassEntry.get() == '':
            showerror('Error', 'All Fields Are Required', parent=root2)
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='u:nz48UV', database='vehicle_number')
                cur = con.cursor()
                cur.execute('select * from users where email=%s and question=%s and answer=%s',
                            (mailentry.get(), securityquescombo.get(), answerforgetEntry.get()))
                row = cur.fetchone()
                
                if row == None:
                    showerror('Error', 'Security Question or Answer is Incorrect\n\n\tPlease Try Again ', parent=root2)

                else:
                    cur.execute('update users set password=%s where email=%s', (newpassEntry.get(), mailentry.get()))
                    con.commit()
                    con.close()
                    showinfo('Success', 'Password is reset, please login with new password', parent=root2)
                    reset()
                    root2.destroy()


            except Exception as e:
                showerror('Error', f"Error due to: {e}", parent=root)

    if mailentry.get() == '':
        showerror('Error', 'Please enter the email address to reset your password', parent=root)
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='u:nz48UV', database='vehicle_number')
            cur = con.cursor()
            cur.execute('select * from users where email=%s', mailentry.get())
            row = cur.fetchone()
            if row == None:
                showerror('Error', 'Please enter the valid email address', parent=root)

            else:
                con.close()
                root2 = Toplevel()
                root2.title('Forget Password')
                root2.geometry('470x560+400+60')
                root2.config(bg='white')
                root2.focus_force()
                root2.grab_set()
                forgetLabel = Label(root2, text='Forget', font=('times new roman', 22, 'bold'), fg='black', bg='white')
                forgetLabel.place(x=128, y=10)
                forgetpassLabel = Label(root2, text='Password', font=('times new roman', 22, 'bold'), fg='green',
                                        bg='white')
                forgetpassLabel.place(x=225, y=10)

                passwordimage = PhotoImage(file='pass.png')
                forgetimageLabel = Label(root2, image=passwordimage, bg='white')
                forgetimageLabel.place(x=170, y=70)

                securityquesLabel = Label(root2, text='Security Questions', font=('times new roman', 19, 'bold'),
                                          fg='black',
                                          bg='white')
                securityquesLabel.place(x=60, y=220)
                securityquescombo = ttk.Combobox(root2, font=('times new roman', 19), state='readonly', justify=CENTER,
                                                 width=28)
                securityquescombo['values'] = (
                    'Select', 'Your First Pet Name?', 'Your Birth Place Name?', 'Your Best Friend Name?',
                    'Your Favourite Teacher?', 'Your Favourite Hobby?')
                securityquescombo.place(x=60, y=260)
                securityquescombo.current(0)

                answerforgetLabel = Label(root2, text='Answer', font=('times new roman', 19, 'bold'), fg='black',
                                          bg='white')
                answerforgetLabel.place(x=60, y=310)
                answerforgetEntry = Entry(root2, font=('times new roman', 19,), fg='black', width=30,
                                          bg='white')
                answerforgetEntry.place(x=60, y=350)

                newpassLabel = Label(root2, text='New Password', font=('times new roman', 19, 'bold'), fg='black',
                                     bg='white')
                newpassLabel.place(x=60, y=400)
                newpassEntry = Entry(root2, font=('times new roman', 19,), fg='black', width=30,
                                     bg='white')
                newpassEntry.place(x=60, y=440)

                changepassbutton = Button(root2, text='Change Password', font=('arial', 17, 'bold'), bg='green',
                                          fg='white', cursor='hand2', activebackground='green',
                                          activeforeground='white',
                                          command=reset_password)
                changepassbutton.place(x=130, y=500)

                root2.mainloop()

        except Exception as e:
            showerror('Error', f"Error due to: {e}", parent=root)


def register_window():
    root.destroy()
    import register


def signin():
    if mailentry.get() == '' or passentry.get() == '':
        showerror('Error', 'All Fields Are Required')

    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='u:nz48UV', database='vehicle_number')
            cur = con.cursor()
            cur.execute('select * from users where email=%s and password=%s', (mailentry.get(), passentry.get()))
            row = cur.fetchone()
            if row == None:
            	showerror('error', 'Invalid Email or Password')
            else:
            	showinfo('Success', 'Welcome')
            	root.destroy()
            	import App
  
            con.close()
        except Exception as e:
            showerror('Error', f"Error due to: {e}", parent=root)


root = Tk()
root.geometry('900x600+50+50')
root.title('Login Page')
bglogin = PhotoImage(file='loginbg.png')
bgloginLabel = Label(root, image=bglogin)
bgloginLabel.place(x=0, y=0)

frame = Frame(root, bg='white', width=560, height=320)
frame.place(x=180, y=140)

#userimage = PhotoImage(file='user.png') 
# Read the Image
image = Image.open("user.png") 
# Resize the image using resize() method
resize_image = image.resize((200, 200))
userimage = ImageTk.PhotoImage(resize_image)

userimageLabel = Label(frame, image=userimage, bg='white')
userimageLabel.place(x=10, y=50)

mailLabel = Label(frame, text='Email', font=('arial', 22, 'bold'), bg='white', fg='black')
mailLabel.place(x=220, y=32)
mailentry = Entry(frame, font=('arial', 22,), bg='white', fg='black')
mailentry.place(x=220, y=70)

passLabel = Label(frame, text='Password', font=('arial', 22, 'bold'), bg='white', fg='black')
passLabel.place(x=220, y=120)
passentry = Entry(frame, font=('arial', 22,), bg='white', fg='black')
passentry.place(x=220, y=160)

regbutton = Button(frame, text='Register New Account?', font=('arial', 12,), bd=0, fg='gray20', bg='white',
                   cursor='hand2', command=register_window,
                   activebackground='white', activeforeground='gray20')
regbutton.place(x=220, y=200)

forgetbutton = Button(frame, text='Forget Password?', font=('arial', 12,), bd=0, fg='red', bg='white',
                      cursor='hand2', command=forget_password,
                      activebackground='white', activeforeground='gray20')
forgetbutton.place(x=410, y=200)

loginbutton2 = Button(frame, text='Login', font=('arial', 18, 'bold'), fg='white', bg='gray20', cursor='hand2',
                      activebackground='gray20', activeforeground='white', command=signin)
loginbutton2.place(x=450, y=240)

root.mainloop()
