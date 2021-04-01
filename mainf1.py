import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import sys

win = tk.Tk()
win.title("Student Management System")
win.geometry("1350x700+0+0")

title = ttk.Label(win, text="Student Management System",font=("sans-serif",40,'bold'), background='aliceblue',foreground='black',border=10,relief=tk.GROOVE,anchor=tk.CENTER)
title.pack(side = tk.TOP, fill=tk.X)

# Liscence Verification
liscensed_prod = True
if liscensed_prod:
    pass
else:
    messagebox.showwarning("Liscence Verification", "Please buy the product to use all features.")

# all variables
Roll_no = tk.StringVar()
name = tk.StringVar()
email = tk.StringVar()
gender = tk.StringVar()
contact = tk.StringVar()
dob = tk.StringVar()
address = tk.StringVar()
search_by = tk.StringVar()
search_text = tk.StringVar()

# manage frame 
manage_frame = tk.Frame(win,border=4,relief=tk.RIDGE,background='lightgrey')
manage_frame.place(x=20,y=70,width=450,height=570)

m_title = ttk.Label(manage_frame, text="Manage Students",font=("sans-serif",30,'bold'),anchor=tk.CENTER,background="lightgrey")
m_title.grid(row=0,columnspan=2,padx=2,pady=2)
# m_title.pack(side=tk.TOP,fill=tk.X)

lbl_roll = ttk.Label(manage_frame,text="Roll No.",font=("sans-serif",20,'bold'),anchor=tk.CENTER,background="lightgrey")
lbl_roll.grid(row=1,column=0,pady=10,padx=20,sticky=tk.W)

txt_roll = ttk.Entry(manage_frame,font=("sans-serif",15,'bold'),textvariable=Roll_no)
txt_roll.grid(row=1,column=1,pady=5,padx=6)

lbl_name = ttk.Label(manage_frame,text="Name",font=("sans-serif",20,'bold'),anchor=tk.CENTER,background="lightgrey")
lbl_name.grid(row=2,column=0,pady=10,padx=20,sticky=tk.W)

txt_name = ttk.Entry(manage_frame,font=("sans-serif",15,'bold'),textvariable=name)
txt_name.grid(row=2,column=1,pady=5,padx=6)

lbl_email = ttk.Label(manage_frame,text="Email",font=("sans-serif",20,'bold'),anchor=tk.CENTER,background="lightgrey")
lbl_email.grid(row=3,column=0,pady=10,padx=20,sticky=tk.W)

txt_email = ttk.Entry(manage_frame,font=("sans-serif",15,'bold'),textvariable=email)
txt_email.grid(row=3,column=1,pady=5,padx=6)

lbl_gender = ttk.Label(manage_frame,text="Gender",font=("sans-serif",20,'bold'),anchor=tk.CENTER,background="lightgrey")
lbl_gender.grid(row=4,column=0,pady=10,padx=20,sticky=tk.W)

combo_gender = ttk.Combobox(manage_frame,font=("sans-serif",14,'bold'),state='readonly',textvariable=gender)
combo_gender['values']=('Male','Female','Others')
combo_gender.grid(row=4,column=1,padx=6,pady=5)

lbl_contact = ttk.Label(manage_frame,text="Contact",font=("sans-serif",20,'bold'),anchor=tk.CENTER,background="lightgrey")
lbl_contact.grid(row=5,column=0,pady=10,padx=20,sticky=tk.W)

txt_contact = ttk.Entry(manage_frame,font=("sans-serif",15,'bold'),textvariable=contact)
txt_contact.grid(row=5,column=1,pady=5,padx=6)

lbl_dob = ttk.Label(manage_frame,text="D.O.B",font=("sans-serif",20,'bold'),anchor=tk.CENTER,background="lightgrey")
lbl_dob.grid(row=6,column=0,pady=10,padx=20,sticky=tk.W)

txt_dob = ttk.Entry(manage_frame,font=("sans-serif",15,'bold'),textvariable=dob)
txt_dob.grid(row=6,column=1,pady=5,padx=6)

lbl_address = ttk.Label(manage_frame,text="Address",font=("sans-serif",20,'bold'),anchor=tk.CENTER,background="lightgrey")
lbl_address.grid(row=7,column=0,pady=10,padx=20,sticky=tk.W)

txt_address = tk.Text(manage_frame,width=30,height=4)
txt_address.grid(row=7,column=1,pady=5,padx=6,sticky=tk.W)

# button frame

button_frame = tk.Frame(manage_frame,border=4,relief=tk.RIDGE,background='lightgrey')
button_frame.place(x=10,y=500,width=430)

def fetch_data():
    con=pymysql.connect(host="localhost",user="root",password="",database="stm1t1")
    cur=con.cursor()
    cur.execute("select * from students")
    rows=cur.fetchall()
    if len(rows)!=0:
        student_table.delete(*student_table.get_children())
        for row in rows:
            student_table.insert('',tk.END,values=row)
        con.commit()
    con.close()

def add_students():
    if Roll_no.get() == "" or name.get() == "":
        messagebox.showerror("Error!", "Please enter all the fields")
    else:
        con=pymysql.connect(host="localhost",user="root",password="",database="stm1t1")
        cur=con.cursor()
        cur.execute("insert into students values(%s,%s,%s,%s,%s,%s,%s)",(Roll_no.get(),name.get(),email.get(),gender.get(),contact.get(),dob.get(),txt_address.get(1.0,tk.END)))
        con.commit()
        fetch_data()
        clear()
        con.close()
        messagebox.showinfo("Success","Student record has been inserted successfully!")

def clear():
    Roll_no.set("")
    name.set("")
    email.set("")
    gender.set("")
    contact.set("")
    dob.set("")
    txt_address.delete("1.0",tk.END)

def get_cursor(event):
    '''It will get the selected data from treeview '''
    cursor_row = student_table.focus()
    contents = student_table.item(cursor_row)
    row = contents['values']
    Roll_no.set(row[0])
    name.set(row[1])
    email.set(row[2])
    gender.set(row[3])
    contact.set(row[4])
    dob.set(row[5])
    txt_address.delete("1.0",tk.END)
    txt_address.insert(tk.END,row[6])

def update_data():
    '''This function will update the data in database '''
    con=pymysql.connect(host="localhost",user="root",password="",database="stm1t1")
    cur=con.cursor()
    cur.execute("update students set name=%s,email=%s,gender=%s,contact=%s,dob=%s,address=%s where roll_no=%s",(name.get(),email.get(),gender.get(),contact.get(),dob.get(),txt_address.get(1.0,tk.END),Roll_no.get()))
    con.commit()
    fetch_data()
    clear()
    con.close()

def delete_data():
    '''This function will delete data from database '''
    con=pymysql.connect(host="localhost",user="root",password="",database="stm1t1")
    cur=con.cursor()
    cur.execute("delete from students where roll_no=%s",Roll_no.get())
    con.commit()
    fetch_data()
    # clear() ---> This has been disabled to so that the user can get the data if he delets it by mistake
    con.close()

def search_data():
    con=pymysql.connect(host="localhost",user="root",password="",database="stm1t1")
    cur=con.cursor()
    cur.execute("select * from students where "+str(search_by.get())+" like '%"+str(search_text.get())+"%'")
    rows=cur.fetchall()
    if len(rows)!=0:
        student_table.delete(*student_table.get_children())
        for row in rows:
            student_table.insert('',tk.END,values=row)
        con.commit()
    con.close()


add_btn = ttk.Button(button_frame,text="Add",width=10,command=add_students)
add_btn.grid(row=0,column=0,padx=10,pady=10)

update_btn = ttk.Button(button_frame,text="Update",width=10,command=update_data)
update_btn.grid(row=0,column=1,padx=10,pady=10)

delete_btn = ttk.Button(button_frame,text="Delete",width=10,command=delete_data)
delete_btn.grid(row=0,column=2,padx=10,pady=10)

clear_btn = ttk.Button(button_frame,text="Clear",width=10,command=clear)
clear_btn.grid(row=0,column=3,padx=10,pady=10)

# detail frame
detail_frame = tk.Frame(win,border=4,relief=tk.RIDGE,background='lightgrey')
detail_frame.place(x=500,y=70,width=800,height=550)

lblSearch = ttk.Label(detail_frame,text="Search By",background='lightgrey',font=('sans-serif',12,'bold'))
lblSearch.grid(row=0,column=0,padx=20,pady=10,sticky=tk.W)

combo_search = ttk.Combobox(detail_frame,textvariable=search_by,font=("sans-serif",14,'bold'),state='readonly')
combo_search['values']=('Roll_No','Name','Contact')
combo_search.grid(row=0,column=1,padx=6,pady=5)

txt_search = ttk.Entry(detail_frame,textvariable=search_text,font=("sans-serif",15,'bold'))
txt_search.grid(row=0,column=2,pady=5,padx=6)

search_btn = ttk.Button(detail_frame,text="Search",width=10,command=search_data)
search_btn.grid(row=0,column=3,padx=10,pady=10)

showall_btn = ttk.Button(detail_frame,text="Show All",width=10,command=fetch_data)
showall_btn.grid(row=0,column=4,padx=7,pady=10)

# table frame
table_frame = tk.Frame(detail_frame,border=4,relief=tk.RIDGE,background='lightgrey')
table_frame.place(x=10,y=70,width=760,height=450)

scroll_x = tk.Scrollbar(table_frame,orient=tk.HORIZONTAL)
scorll_y = tk.Scrollbar(table_frame,orient=tk.VERTICAL)
student_table = ttk.Treeview(table_frame,columns=("Roll",'Name','E-mail','Gender','Contact','D.O.B','Address'),xscrollcommand=scroll_x.set,yscrollcommand=scorll_y.set)
scroll_x.pack(side=tk.BOTTOM,fill=tk.X)
scorll_y.pack(side=tk.RIGHT,fill=tk.Y)
scroll_x.config(command=student_table.xview)
scorll_y.config(command=student_table.yview)
student_table.heading("Roll",text="Roll No.")
student_table.heading("Name",text="Name")
student_table.heading("E-mail",text="E-mail")
student_table.heading("Gender",text="Gender")
student_table.heading("Contact",text="Contact")
student_table.heading("D.O.B",text="D.O.B")
student_table.heading("Address",text="Address")
student_table['show'] = 'headings'
student_table.column("Roll",width=100)
student_table.column("Name",width=100)
student_table.column("E-mail",width=100)
student_table.column("Gender",width=100)
student_table.column("Contact",width=100)
student_table.column("D.O.B",width=100)
student_table.column("Address",width=150)

student_table.pack(fill=tk.BOTH,expand=True)
student_table.bind("<ButtonRelease-1>",get_cursor)
try:
    fetch_data()    
except: 
    messagebox.showerror("Database Error!", "Sorry we are unable to fetch data from database. Please try troubleshooting.")
    sys.exit()
    

# progrees bar 
# pgbar = ttk.Progressbar(win,orient=tk.HORIZONTAL, length=100,mode=)
# pgbar.pack(side=yk.BOTTOM)


win.mainloop()