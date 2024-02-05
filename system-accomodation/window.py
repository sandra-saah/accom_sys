from cgi import test
from os import stat
import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from typing import Counter


class TestUnit():
    def test_login(self, verdict):
        print("Login:", verdict)

    def test_update(self, verdict):
        print("Update:", verdict)

    def test_delete(self, verdict):
        print("Delete:", verdict)

#USER Class
class User:
    def _init_(self):
        self.role = 0
        self.uername = ""
        self.password = ""

    #USER Login Validation
    def validateLogin(self):
        
        q = "SELECT * FROM USER WHERE USERNAME = '" + self.username + "' AND PASSWORD = '" + self.password + "' AND ROLE = '" + str(self.role) + "';"
        cur.execute(q)

        rows = cur.fetchall()
        if len(rows) > 0:
            print("Login Successful!")
        else:
            print("Login Failed!")
        return len(rows) == 0


#HALL Class
class Hall:
    def _init_(self):
        self.lease_number = ""
        self.hall_name = ""
        self.hall_number = ""
        self.room_number = ""
        self.student_id = ""
        self.student_name = ""
        self.occupancy_status = ""
        self.cleaning_status = ""
        self.rent_per_month = ""
        self.duration = ""


    #Update HALL Class's Attributes
    def select(self, lease_number, hall_name, hall_number, room_number, student_id, student_name, occupancy_status, cleaning_status, rent_per_month, duration):
        self.lease_number = lease_number
        self.hall_name = hall_name
        self.hall_number = hall_number
        self.room_number = room_number
        self.student_id = student_id
        self.student_name = student_name
        self.occupancy_status = occupancy_status
        self.cleaning_status = cleaning_status
        self.rent_per_month = rent_per_month
        self.duration = duration

    #Update Data in Database
    def update(self, user):
        print("Vlues", self.lease_number, self.student_id, self.student_name, self.duration)
        if user != "Warden":
            q = "SELECT * FROM HALL WHERE LEASE_NUMBER = '" + self.lease_number + "' AND HALL_NUMBER = '" + self.hall_number + "' AND ROOM_NUMBER = '" + self.room_number + "';"

            cur.execute(q)
            rows = cur.fetchall()

            if (self.cleaning_status == "Offline" or self.occupancy_status == "Occupied") and len(rows) == 0:
                if self.cleaning_status == "Offline" and self.occupancy_status == "Occupied":
                    messagebox.showerror("Room is Occupied and Offline!", "To add Lease the Room shouldn't be Occupied or Offline!")
                if self.cleaning_status == "Offline":
                    messagebox.showerror("Room is Offline!", "To add Lease the Room shouldn't be Offline!")
                else:
                    messagebox.showerror("Room is Occupied!", "To add Lease the Room shouldn't be Occupied!")

                return 0

           

            if self.lease_number and self.student_id and self.student_name and self.duration:

                q = "SELECT * FROM HALL WHERE STUDENT_ID = '" + self.student_id + "' AND HALL_NUMBER != '" + self.hall_number + "' AND ROOM_NUMBER != '" + self.room_number + "';"

                cur.execute(q)
                rows = cur.fetchall()

                if len(rows) != 0:
                    messagebox.showerror("Student Already Exists!", "Student has been allocated a Room already with this ID!")
                    return 0

                q = "SELECT * FROM HALL WHERE LEASE_NUMBER = '" + self.lease_number + "' AND HALL_NUMBER != '" + self.hall_number + "' AND ROOM_NUMBER != '" + self.room_number + "';"

                cur.execute(q)
                rows = cur.fetchall()

                if len(rows) != 0:
                    messagebox.showerror("Lease Already Exists!", "Existing list found with this number!")
                    return 0

                q = "UPDATE HALL SET LEASE_NUMBER = '" + self.lease_number + "', STUDENT_ID = '" + self.student_id + "', STUDENT_NAME = '" + self.student_name + "', DURATION = '" + self.duration + "', OCCUPANCY_STATUS = 'Occupied' WHERE HALL_NAME = '" + self.hall_name + "' AND HALL_NUMBER = '" + self.hall_number + "' AND ROOM_NUMBER = '" + self.room_number + "';"

                cur.execute(q)
                conn.commit()
                return 1
            else:
                messagebox.showerror("Missing Data!", "Fill up all the required field to update!")
                return 0

            

        else:

            q = "UPDATE HALL SET CLEANING_STATUS = '" + self.cleaning_status + "' WHERE HALL_NAME = '" + self.hall_name + "' AND HALL_NUMBER = '" + self.hall_number + "' AND ROOM_NUMBER = '" + self.room_number + "';"

            cur.execute(q)
            conn.commit()

            return 2

    #Delete Lease From Database
    def delete(self, user):
        if user != "Warden":
            q = "UPDATE HALL SET LEASE_NUMBER = '', STUDENT_ID = '', STUDENT_NAME = '', DURATION = '', OCCUPANCY_STATUS = 'Unoccupied' WHERE HALL_NAME = '" + self.hall_name + "' AND HALL_NUMBER = '" + self.hall_number + "' AND ROOM_NUMBER = '" + self.room_number + "';"

            cur.execute(q)
            conn.commit()
            return 1
        else:
            messagebox.showerror("Access Limit!", "Warden can't delete any data!")
            return 0


global users, hall, testUnit 
testUnit = TestUnit()
users = User()
hall = Hall()

#Database Connection
conn = sqlite3.connect('uwe.sqlite')
cur = conn.cursor()

#Login Button Click -> Action
def btn_clicked():
    
    #Delete Data Function
    def delete():
        hall.select(ln1_entry.get(), ln2_entry.get(), ln3_entry.get(), ln4_entry.get(), ln10_entry.get(), ln5_entry.get(), ln6_entry.get(), co.get(), ln8_entry.get(), ln9_entry.get())

        deleteVar = hall.delete(user)

        if deleteVar == 0:
            testUnit.test_delete(False)
            return 0

        selected = my_tree.focus()
        values = ('', ln2_entry.get(), ln3_entry.get(), ln4_entry.get(), '', '', "Unoccupied", co.get(), ln8_entry.get(), '')
        my_tree.item(selected, text="", values=values)



    #Update Data Function
    def update():
        hall.select(ln1_entry.get(), ln2_entry.get(), ln3_entry.get(), ln4_entry.get(), ln10_entry.get(), ln5_entry.get(), ln6_entry.get(), co.get(), ln8_entry.get(), ln9_entry.get())
        updatevar = hall.update(user)

        #Check if the user is warden or not
        if updatevar == 1:
            testUnit.test_update(True)
            selected = my_tree.focus()
            values = (ln1_entry.get(), ln2_entry.get(), ln3_entry.get(), ln4_entry.get(), ln10_entry.get(), ln5_entry.get(), "Occupied", co.get(), ln8_entry.get(), ln9_entry.get())
            my_tree.item(selected, text="", values=values)

        elif updatevar == 2:
            testUnit.test_update(True)
            selected = my_tree.focus()
            values = (ln1_entry.get(), ln2_entry.get(), ln3_entry.get(), ln4_entry.get(), ln10_entry.get(), ln5_entry.get(), ln6_entry.get(), co.get(), ln8_entry.get(), ln9_entry.get())
            my_tree.item(selected, text="", values=values)

        else:
            testUnit.test_update(False)
            return 0

    #Select Tree Function
    def select(e):

        ln1_entry.config(state="normal")
        ln2_entry.config(state="normal")
        ln3_entry.config(state="normal")
        ln4_entry.config(state="normal")
        ln5_entry.config(state="normal")
        ln6_entry.config(state="normal")
        ln7_entry.config(state="normal")
        ln8_entry.config(state="normal")
        ln9_entry.config(state="normal")
        ln10_entry.config(state="normal")

        ln1_entry.delete(0, END)
        ln2_entry.delete(0, END)
        ln3_entry.delete(0, END)
        ln4_entry.delete(0, END)
        ln5_entry.delete(0, END)
        ln6_entry.delete(0, END)
        co.set("                            ")
        ln8_entry.delete(0, END)
        ln9_entry.delete(0, END)
        ln10_entry.delete(0, END)

        selected= my_tree.focus()

        values = my_tree.item(selected, 'values')

        ln1_entry.insert(0, values[0])
        ln2_entry.insert(0, values[1])
        ln3_entry.insert(0, values[2])
        ln4_entry.insert(0, values[3])
        ln10_entry.insert(0, values[4])
        ln5_entry.insert(0, values[5])
        ln6_entry.insert(0, values[6])
        co.set(values[7])
        ln8_entry.insert(0, values[8])
        ln9_entry.insert(0, values[9])

        ln2_entry.config(state="disable")
        ln3_entry.config(state="disable")
        ln4_entry.config(state="disable")
        ln6_entry.config(state="disable")
        ln8_entry.config(state="disable")

        if user == "Warden":
            ln1_entry.config(state="disable")
            ln5_entry.config(state="disable")
            ln9_entry.config(state="disable")
            ln10_entry.config(state="disable")

        if user == "Manager":
            ln7_entry.config(state="disable")


    role = n.get()
    user = n.get()
    users.username = entry1.get()
    users.password = entry0.get()

    if role == "Admin":
        users.role = 1
    elif role == "Manager":
        users.role = 2
    elif role == "Warden":
        users.role = 3
    else:
        users.role = -1
        messagebox.showwarning("Invalid User Role!", "Please choose a Role to Login!")
        return 0

    #Validation User Authentication
    isLoginValid = users.validateLogin()


    #User Login Validation Message
    if isLoginValid:
        testUnit.test_login(False)
        messagebox.showerror("Invalid Credential!", "Invalid Username or Password!")
    else:
        testUnit.test_login(True)
        messagebox.showinfo("Success", "Login Success!")
        newWindow = Toplevel(window)
 

        newWindow.title("UWE " + user + " Dashboard")
        newWindow.geometry("1600x600")

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",  background="#093545", foreground="white", rowheight=25, fieldbackground="#D3D3D3")
        style.map('Treeview', background=[('selected', '#093545')])

        #Tree Setup
        tree_frame = Frame(newWindow)
        tree_frame.pack(padx=20)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll2 = Scrollbar(tree_frame, orient='horizontal')
        tree_scroll.pack(side=RIGHT, fill=Y)
        tree_scroll2.pack(side=BOTTOM, fill=X)
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, xscrollcommand=tree_scroll2.set, selectmode="extended")
        my_tree.pack()

        tree_scroll.configure(command=my_tree.yview)
        tree_scroll2.configure(command=my_tree.xview)

        my_tree['columns'] = ('Lease Number', 'Hall Name', 'Hall Number', 'Room Number', 'Student ID', 'Student Name', 'Occupancy Status', 'Cleaning Status', 'Rent Per Month', 'Duration (Month)')

        my_tree.column('#0', width=0, stretch=NO)
        my_tree.column("Lease Number", anchor=CENTER, width=140)
        my_tree.column("Hall Name", anchor=CENTER, width=140)
        my_tree.column("Hall Number", anchor=CENTER, width=140)
        my_tree.column("Room Number", anchor=CENTER, width=140)
        my_tree.column("Student ID", anchor=CENTER, width=140)
        my_tree.column("Student Name", anchor=W, width=200)
        my_tree.column("Occupancy Status", anchor=CENTER, width=140)
        my_tree.column("Cleaning Status", anchor=CENTER, width=140)
        my_tree.column("Rent Per Month", anchor=CENTER, width=140)
        my_tree.column("Duration (Month)", anchor=CENTER, width=140)

        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("Lease Number", text="Lease Number", anchor=CENTER)
        my_tree.heading("Hall Name", text="Hall Name", anchor=CENTER)
        my_tree.heading("Hall Number", text="Hall Number", anchor=CENTER)
        my_tree.heading("Room Number", text="Room Number", anchor=CENTER)
        my_tree.heading("Student ID", text="Student ID", anchor=CENTER)
        my_tree.heading("Student Name", text="Student Name", anchor=CENTER)
        my_tree.heading("Occupancy Status", text="Occupancy Status", anchor=CENTER)
        my_tree.heading("Cleaning Status", text="Cleaning Status", anchor=CENTER)
        my_tree.heading("Rent Per Month", text="Rent Per Month", anchor=CENTER)
        my_tree.heading("Duration (Month)", text="Duration (Month)", anchor=CENTER)

        q = "SELECT LEASE_NUMBER, HALL_NAME, HALL_NUMBER, ROOM_NUMBER, STUDENT_ID, STUDENT_NAME, OCCUPANCY_STATUS, CLEANING_STATUS, RENT, DURATION FROM HALL ORDER BY HALL_NUMBER, ROOM_NUMBER;"
        cur.execute(q)

        rows = cur.fetchall()


        data = rows

        my_tree.tag_configure('oddrow', background="white")
        my_tree.tag_configure('evenrow', background="#99FEFF")

        global Counter
        count = 0

        for record in data:
            if count % 2 == 0:
                my_tree.insert(parent="", index="end", iid=count, text="", values=record, tags=('evenrow',))
            else:
                my_tree.insert(parent="", index="end", iid=count, text="", values=record, tags=('oddrow',))

            count += 1

        data_frame = LabelFrame(newWindow, text="Record")
        data_frame.pack(fill="x", expand="yes", padx=20)

        
        #Record Entry Boxes

        ln2_label = Label(data_frame, text="Hall Name")
        ln2_label.grid(row=0, column=0, padx=10, pady=10)
        ln2_entry = Entry(data_frame, state="disable")
        ln2_entry.grid(row=0, column=1, padx=10, pady=10)

        ln3_label = Label(data_frame, text="Hall Number")
        ln3_label.grid(row=0, column=2, padx=10, pady=10)
        ln3_entry = Entry(data_frame, state="disable")
        ln3_entry.grid(row=0, column=3, padx=10, pady=10)

        ln4_label = Label(data_frame, text="Room Number")
        ln4_label.grid(row=0, column=4, padx=10, pady=10)
        ln4_entry = Entry(data_frame, state="disable")
        ln4_entry.grid(row=0, column=5, padx=10, pady=10)

        

        ln6_label = Label(data_frame, text="Occupancy Status")
        ln6_label.grid(row=0, column=8, padx=10, pady=10)
        ln6_entry = Entry(data_frame, state="disable")
        ln6_entry.grid(row=0, column=9, padx=10, pady=10)

        co = tk.StringVar(window)
        co.set("                            ")
        co_list = ["Clean", "Dirty", "Offline"]

        if user == "Warden" or user == "Admin":
            ln7_label = Label(data_frame, text="Cleaning Status")
            ln7_label.grid(row=0, column=10, padx=10, pady=10)
            ln7_entry = tk.OptionMenu(data_frame, co, *co_list)
            ln7_entry.configure(bg="white", bd=0, fg="black", highlightthickness = 0)
            ln7_entry.place(width=200, height=50)
            ln7_entry.grid(row=0, column=11, padx=10, pady=10)
        elif user == "Manager":
            ln7_label = Label(data_frame, text="Cleaning Status")
            ln7_label.grid(row=0, column=10, padx=10, pady=10)
            ln7_entry = tk.OptionMenu(data_frame, co, *co_list)
            ln7_entry.configure(bg="white", bd=0, fg="black", highlightthickness = 0, state="disable")
            ln7_entry.place(width=200, height=50)
            ln7_entry.grid(row=0, column=11, padx=10, pady=10)
       
        if user == "Admin" or user == "Manager":
            ln1_label = Label(data_frame, text="Lease Number")
            ln1_label.grid(row=1, column=0, padx=10, pady=10)
            ln1_entry = Entry(data_frame)
            ln1_entry.grid(row=1, column=1, padx=10, pady=10)

            ln5_label = Label(data_frame, text="Student Name")
            ln5_label.grid(row=1, column=6, padx=10, pady=10)
            ln5_entry = Entry(data_frame)
            ln5_entry.grid(row=1, column=7, padx=10, pady=10)

            ln9_label = Label(data_frame, text="Duration (Month)")
            ln9_label.grid(row=1, column=2, padx=10, pady=10)
            ln9_entry = Entry(data_frame)
            ln9_entry.grid(row=1, column=3, padx=10, pady=10)

            ln10_label = Label(data_frame, text="Student ID")
            ln10_label.grid(row=1, column=4, padx=10, pady=10)
            ln10_entry = Entry(data_frame)
            ln10_entry.grid(row=1, column=5, padx=10, pady=10)
        elif user == "Warden":
            ln1_label = Label(data_frame, text="Lease Number")
            ln1_label.grid(row=1, column=0, padx=10, pady=10)
            ln1_entry = Entry(data_frame, state="disable")
            ln1_entry.grid(row=1, column=1, padx=10, pady=10)

            ln5_label = Label(data_frame, text="Student Name")
            ln5_label.grid(row=1, column=6, padx=10, pady=10)
            ln5_entry = Entry(data_frame, state="disable")
            ln5_entry.grid(row=1, column=7, padx=10, pady=10)

            ln9_label = Label(data_frame, text="Duration (Month)")
            ln9_label.grid(row=1, column=2, padx=10, pady=10)
            ln9_entry = Entry(data_frame, state="disable")
            ln9_entry.grid(row=1, column=3, padx=10, pady=10)

            ln10_label = Label(data_frame, text="Student ID")
            ln10_label.grid(row=1, column=4, padx=10, pady=10)
            ln10_entry = Entry(data_frame, state="disable")
            ln10_entry.grid(row=1, column=5, padx=10, pady=10)

        ln8_label = Label(data_frame, text="Rent Per Month")
        ln8_label.grid(row=0, column=6, padx=10, pady=10)
        ln8_entry = Entry(data_frame, state="disable")
        ln8_entry.grid(row=0, column=7, padx=10, pady=10)

        

        
        #command buttons to update and delete data
        button_frame = LabelFrame(newWindow, text="Commands")
        button_frame.pack(fill="x", expand="yes", padx=20)

        button1 = Button(button_frame, text="Update", command=update)
        button1.grid(row=0, column=0, padx=10, pady=10)

        button2 = Button(button_frame, text="Delete", command=delete)
        button2.grid(row=0, column=1, padx=10, pady=10)

        my_tree.bind("<ButtonRelease-1>", select)




#Login Page Setup

window = Tk()

window.geometry("1280x720")
window.configure(bg = "#093545")
canvas = Canvas(
    window,
    bg = "#093545",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 490, y = 485,
    width = 300,
    height = 45)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    640.0, 426.5,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#224957",
    fg = "white",
    highlightthickness = 0)

entry0.place(
    x = 500.0, y = 404,
    width = 280.0,
    height = 43)

canvas.create_text(
    543.5, 427.0,
    text = "Password",
    fill = "#ffffff",
    font = ("LexendDeca-Regular", int(14.0)))

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    640.0, 347.5,
    image = entry1_img)

entry2_bg = canvas.create_image(
    640.0, 268.5,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#224957",
    fg = "white",
    highlightthickness = 0)

entry1.place(
    x = 500.0, y = 325,
    width = 280.0,
    height = 43)

entry1.insert(0, "Username")
entry0.insert(0, "Password")

n = tk.StringVar(window)
n.set("Select Role")
options_list = ["Manager", "Warden", "Admin"]
entry2 = tk.OptionMenu(window, n, *options_list)
entry2.pack()
  
entry2.configure(bg="#224957", bd=0, fg="white", highlightthickness = 0)
  
entry2.place(
    x = 500.0, y = 246,
    width = 280.0,
    height = 43)

canvas.create_text(
    548.0, 348.0,
    text = "Username",
    fill = "#ffffff",
    font = ("LexendDeca-Regular", int(14.0)))

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    640.0, 360.0,
    image=background_img)

canvas.create_text(
    639.5, 179.0,
    text = "Sign in to UWE Bristol Accommodation System!",
    fill = "#ffffff",
    font = ("LexendDeca-Regular", int(16.0)))

canvas.create_text(
    640.0, 88.5,
    text = "Sign in",
    fill = "#ffffff",
    font = ("LexendDeca-Regular", int(64.0)))

window.resizable(False, False)
window.mainloop()