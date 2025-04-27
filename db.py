from tkinter import *
from tkinter import messagebox
import mysql.connector as myconn

screen = Tk()
screen.geometry("900x500")
screen.resizable(False, False)
screen.title("Registration Form")
screen.configure(bg="#f0f0f0")  # Light gray background

def clear():
    nentry.delete(0, END)
    aentry.delete(0, END)
    mentry.delete(0, END)
    eentry.delete(0, END)
    pri.delete(1.0, END)

def register():
    naame = name.get()
    aage = age.get()
    mmobile = mobile.get()
    eemail = email.get()

    if not naame or not aage or not mmobile or not eemail:
        messagebox.showerror("Input Error", "All fields must be filled")
        return

    try:
        mydb = myconn.connect(host="localhost", user="root", password="", database="python_form")
        db_cursor = mydb.cursor()

        insert_query = "INSERT INTO py_form (Name, Age, Mobile, Email) VALUES (%s, %s, %s, %s)"
        insert_values = (naame, aage, mmobile, eemail)

        db_cursor.execute(insert_query, insert_values)
        mydb.commit()

        db_cursor.execute("SELECT * FROM py_form WHERE Name = %s", (naame,))
        records = db_cursor.fetchall()

        pri.delete(1.0, END)

        for record in records:
            pri.insert(END, f"Name: {record[0]}, Age: {record[1]}, Mobile: {record[2]}, Email: {record[3]}\n\n")

    except myconn.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")

    finally:
        if mydb.is_connected():
            db_cursor.close()
            mydb.close()

    try:
        with open("student.txt", "a") as f:
            f.write(f"Name: {naame}\n")
            f.write(f"Age: {aage}\n")
            f.write(f"Mobile: {mmobile}\n")
            f.write(f"Email: {eemail}\n")

    except Exception as e:
        messagebox.showerror("File Error", f"Error writing to file: {e}")
        return

def show():
    search_term = sentry.get()
    if not search_term:
        messagebox.showwarning("Search Error", "Please enter a search term.")
        return

    try:
        mydb = myconn.connect(host="localhost", user="root", password="", database="python_form")
        db_cursor = mydb.cursor()

        search_query = """
        SELECT * FROM py_form 
        WHERE Name LIKE %s OR Mobile LIKE %s OR Email LIKE %s
        """
        search_values = ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%')
        db_cursor.execute(search_query, search_values)

        results = db_cursor.fetchall()

        pri.delete(1.0, END)

        if results:
            for record in results:
                pri.insert(END, f"Name: {record[0]}\n")
                pri.insert(END, f"Age: {record[1]}\n")
                pri.insert(END, f"Mobile: {record[2]}\n")
                pri.insert(END, f"Email: {record[3]}\n")
                pri.insert(END, "--------------------------------------\n")
        else:
            pri.insert(END, "No matching records found.\n")

    except myconn.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        if mydb.is_connected():
            db_cursor.close()
            mydb.close()

def showall():
    try:
        mydb = myconn.connect(host="localhost", user="root", password="", database="python_form")
        db_cursor = mydb.cursor()

        db_cursor.execute("SELECT * FROM py_form")
        records = db_cursor.fetchall()

        pri.delete(1.0, END)

        if records:
            for record in records:
                pri.insert(END, f"Name: {record[0]}\n")
                pri.insert(END, f"Age: {record[1]}\n")
                pri.insert(END, f"Mobile: {record[2]}\n")
                pri.insert(END, f"Email: {record[3]}\n")
                pri.insert(END, "-----------------------------------------------------------------------\n")
        else:
            pri.insert(END, "No records found.\n")

    except myconn.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        if mydb.is_connected():
            db_cursor.close()
            mydb.close()

Label(screen, text="Registration Form", font="Arial 24 bold", bg="#ff4d4d", fg="white").pack(fill=BOTH, pady=10)
Label(screen, text="Name", font=("Arial", 14), bg="#f0f0f0").place(x=30, y=70)
Label(screen, text="Age", font=("Arial", 14), bg="#f0f0f0").place(x=30, y=110)
Label(screen, text="Mobile", font=("Arial", 14), bg="#f0f0f0").place(x=30, y=150)
Label(screen, text="Email", font=("Arial", 14), bg="#f0f0f0").place(x=30, y=190)

name = StringVar()
age = StringVar()
mobile = StringVar()
email = StringVar()

nentry = Entry(screen, font=("Arial", 12), bd=4, textvariable=name)
nentry.place(x=100, y=70)
aentry = Entry(screen, font=("Arial", 12), bd=4, textvariable=age)
aentry.place(x=100, y=110)
mentry = Entry(screen, font=("Arial", 12), bd=4, textvariable=mobile)
mentry.place(x=100, y=150)
eentry = Entry(screen, font=("Arial", 12), bd=4, textvariable=email)
eentry.place(x=100, y=190)

f = Frame(screen, width=520, height=450, relief=RAISED, bd=4, highlightbackground="gray", bg="#e6f7ff", highlightthickness=2)
f.place(x=380, y=50)

search_frame = Label(f, text="Search", font=("Arial", 14), bg="#e6f7ff")
search_frame.place(x=5, y=18)

sentry = Entry(f, font=("Arial", 12), bd=2)
sentry.place(x=80, y=18)

Button(f, text="Show", font=("Arial", 12), bg="#0073e6", fg="white", command=show).place(x=330, y=18)
Button(f, text="Show All", font=("Arial", 12), bg="#0073e6", fg="white", command=showall).place(x=390, y=18)

pri = Text(f, font=("Arial", 12), width=56, height=19, bg="#ffffff", fg="#000000")
pri.place(x=0, y=70)

Button(screen, text="Register", font=("Arial", 14), bg="#ff4d4d", fg="white", command=register).place(x=40, y=250)
Button(screen, text="Clear", font=("Arial", 14), bg="#ff4d4d", fg="white", command=clear).place(x=150, y=250)
Button(screen, text="Exit", font=("Arial", 14), bg="#333333", fg="white", command=screen.quit).place(x=250, y=250)

screen.mainloop()
