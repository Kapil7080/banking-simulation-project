from tkinter import Tk, Label, Frame, Entry, Button, messagebox, simpledialog, filedialog, END
from tkinter.ttk import Combobox
import random
import mygenerator
import dbhandler
import mailhandler
import time
import sqlite3
from PIL import Image, ImageTk
import shutil
import os
import re


def update_time():
    t = time.strftime("%A,%b %d %Y ⏰%r")
    lbl_dt.configure(text=t)
    lbl_dt.after(1000, update_time)


def customer_screen():
    frm = Frame(root, highlightbackground='black', highlightthickness=2)
    frm.configure(bg='#F1F3F4')
    frm.place(relx=0, rely=.183, relwidth=1, relheight=.76)

    def logout_click():
        frm.destroy()
        main_screen()

    def viewdetails_screen():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.21, rely=.15, relwidth=.75, relheight=.6)

        lbl_ftitle = Label(ifrm, text="This is view details screen",
                           font=('arial', 20, 'bold'), bg='white', fg='purple')
        lbl_ftitle.pack()

        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query = 'select * from users where acn=?'
        curobj.execute(query, (user_acn,))
        row = curobj.fetchone()
        conobj.close()
        details = f'''Name = {row[1]}
        ACN = {row[0]}
        Aadhar = {row[5]}
        Bal = {row[7]}
        Open Date= {row[9]}'''

        lbl_details = Label(ifrm, text=details,
                            font=('arial', 20, 'bold'), bg='white', fg='blue')
        lbl_details.place(x=200, y=100)

    def updatedetails_screen():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.21, rely=.15, relwidth=.75, relheight=.6)

        def up_details():
            name = e_name.get()
            pwd = e_pass.get()
            email = e_email.get()
            mob = e_mob.get()

            conobj = sqlite3.connect(database='bank.sqlite')
            curobj = conobj.cursor()
            query = 'update users set name=?,pass=?,email=?,mob=? where acn=?'
            curobj.execute(query, (name, pwd, email, mob, user_acn))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update", "Details Updated")
            customer_screen()

        lbl_ftitle = Label(ifrm, text="This is update details screen",
                           font=('arial', 20, 'bold'), bg='white', fg='purple')
        lbl_ftitle.pack()

        lbl_name = Label(ifrm, text="Name",
                         font=('arial', 20, 'bold'), bg='white')
        lbl_name.place(relx=.1, rely=.09)

        e_name = Entry(ifrm, font=('arial', 14), bd=5)
        e_name.place(relx=.1, rely=.18)

        lbl_email = Label(ifrm, text="Email",
                          font=('arial', 20, 'bold'), bg='white')
        lbl_email.place(relx=.1, rely=.33)

        e_email = Entry(ifrm, font=('arial', 14), bd=5)
        e_email.place(relx=.1, rely=.42)

        lbl_mob = Label(ifrm, text="Mob",
                        font=('arial', 20, 'bold'), bg='white')
        lbl_mob.place(relx=.6, rely=.33)

        e_mob = Entry(ifrm, font=('arial', 14), bd=5)
        e_mob.place(relx=.6, rely=.42)

        lbl_pass = Label(ifrm, text="Pass",
                         font=('arial', 20, 'bold'), bg='white')
        lbl_pass.place(relx=.6, rely=.09)

        e_pass = Entry(ifrm, font=('arial', 14), bd=5)
        e_pass.place(relx=.6, rely=.18)

        up_btn = Button(ifrm, text='Update Details', bd=5,
                        font=('arial', 20, 'bold'), bg='#898B8D', fg='white', cursor='hand2', command=up_details)
        up_btn.place(relx=.4, rely=.7)

        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query = 'select name,pass,email,mob from users where acn=?'
        curobj.execute(query, (user_acn,))
        tup = curobj.fetchone()
        conobj.close()

        e_name.insert(0, tup[0])
        e_pass.insert(0, tup[1])
        e_email.insert(0, tup[2])
        e_mob.insert(0, tup[3])

    def deposit_screen():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.21, rely=.15, relwidth=.75, relheight=.6)

        lbl_ftitle = Label(ifrm, text="This is deposit screen",
                           font=('arial', 20, 'bold'), bg='white', fg='purple')
        lbl_ftitle.pack()

        amt = simpledialog.askfloat("Depsoit Amount", "Enter Amount")
        if amt == None:
            return
        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query = 'update users set bal=bal+? where acn=?'
        curobj.execute(query, (amt, user_acn))
        conobj.commit()
        conobj.close()
        messagebox.showinfo("Deposit", "Amount Deposited")

    def withdraw_screen():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.21, rely=.15, relwidth=.75, relheight=.6)

        lbl_ftitle = Label(ifrm, text="This is withdraw screen",
                           font=('arial', 20, 'bold'), bg='white', fg='purple')
        lbl_ftitle.pack()

        amt = simpledialog.askfloat("Withdraw Amount", "Enter Amount")
        if amt == None:
            return

        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query = 'select bal from users where acn=?'
        curobj.execute(query, (user_acn,))
        bal = curobj.fetchone()[0]
        conobj.close()

        if amt > bal:
            messagebox.showerror("Withdraw", "Insufficient Bal")
            return

        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query = 'update users set bal=bal-? where acn=?'
        curobj.execute(query, (amt, user_acn))
        conobj.commit()
        conobj.close()
        messagebox.showinfo("Withdraw", "Amount Withdrawn")

    def transfer_screen():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.21, rely=.15, relwidth=.75, relheight=.6)

        lbl_ftitle = Label(ifrm, text="This is transfer screen",
                           font=('arial', 20, 'bold'), bg='white', fg='purple')
        lbl_ftitle.pack()

        to_acn = simpledialog.askfloat("Transfer Amount", "Enter To ACN")
        if to_acn == None:
            return

        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query = 'select * from users where acn=?'
        curobj.execute(query, (to_acn,))
        row = curobj.fetchone()
        conobj.close()
        if row == None:
            messagebox.showerror("Transfer Amount", "To ACN does not exist")
            return

        amt = simpledialog.askfloat("Withdraw Amount", "Enter Amount")
        if amt == None:
            return

        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query = 'select bal from users where acn=?'
        curobj.execute(query, (user_acn,))
        bal = curobj.fetchone()[0]
        conobj.close()

        if amt > bal:
            messagebox.showerror("Transfer Amount", "Insufficient Bal")
            return

        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query1 = 'update users set bal=bal-? where acn=?'
        query2 = 'update users set bal=bal+? where acn=?'

        curobj.execute(query1, (amt, user_acn))
        curobj.execute(query2, (amt, to_acn))

        conobj.commit()
        conobj.close()
        messagebox.showinfo(
            "Transfer Amount", f"{amt} Amount Transfered to ACN {to_acn} from ACN {user_acn}")

    def dp():
        filepath = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        shutil.copy(filepath, f'{user_acn}.jpg')

        img = Image.open(f'{user_acn}.jpg').resize((270, 180))
        imgtk = ImageTk.PhotoImage(img, master=root)

        # dp_lbl = Label(frm, image=imgtk)
        # dp_lbl.image = imgtk
        # dp_lbl.place(relx=0, rely=.06)
        dp_lbl.configure(image=imgtk)
        dp_lbl.image = imgtk

        updatedp_btn.lift()

    logout_btn = Button(frm, text='Logout', bd=5,
                        font=('arial', 20, 'bold'), bg='#898B8D', fg='white', cursor='hand2', command=logout_click)
    logout_btn.place(relx=.92, rely=0)

    conobj = sqlite3.connect(database='bank.sqlite')
    curobj = conobj.cursor()
    query = 'select name from users where acn=?'
    curobj.execute(query, user_acn,)
    name = curobj.fetchone()[0]
    conobj.close()

    lbl_wel = Label(frm, text=f"Welcome,{name}",
                    font=('arial', 20, 'bold'), bg='#F1F3F4')
    lbl_wel.place(relx=0, rely=0)

    if os.path.exists(f'{user_acn}.jpg'):
        filepath = f'{user_acn}.jpg'
    else:
        filepath = 'default.jpg'
    imgc = Image.open(filepath).resize((270, 180))
    imgctk = ImageTk.PhotoImage(imgc, master=root)
    dp_lbl = Label(frm, image=imgctk)
    dp_lbl.image = imgctk
    dp_lbl.place(relx=0, rely=.06)

    updatedp_btn = Button(frm, text='update DP', bd=5, command=dp,
                          font=('arial', 15, 'bold'), bg='blue', fg='white', cursor='hand2')
    updatedp_btn.place(relx=.05, rely=.32)

    view_btn = Button(frm, text='View Details', bd=5,
                      font=('arial', 20, 'bold'), bg='blue', fg='white',
                      width=15, cursor='hand2', command=viewdetails_screen)
    view_btn.place(relx=0, rely=.44)

    update_btn = Button(frm, text='Update Details', bd=5,
                        font=('arial', 20, 'bold'), bg='purple', fg='white',
                        width=15, cursor='hand2', command=updatedetails_screen)
    update_btn.place(relx=0, rely=.55)

    deposit_btn = Button(frm, text='Deposit', bd=5,
                         font=('arial', 20, 'bold'), bg='green', fg='white',
                         width=15, cursor='hand2', command=deposit_screen)
    deposit_btn.place(relx=0, rely=.66)

    withdraw_btn = Button(frm, text='Withdraw', bd=5,
                          font=('arial', 20, 'bold'), bg='red', fg='white',
                          width=15, command=withdraw_screen)
    withdraw_btn.place(relx=0, rely=.77)

    transfer_btn = Button(frm, text='Transfer', bd=5,
                          font=('arial', 20, 'bold'), bg='brown', fg='white',
                          width=15, cursor='hand2', command=transfer_screen)
    transfer_btn.place(relx=0, rely=.88)


def admin_screen():
    frm = Frame(root, highlightbackground='black', highlightthickness=2)
    frm.configure(bg='#F1F3F4')
    frm.place(relx=0, rely=.183, relwidth=1, relheight=.76)

    def logout_click():
        frm.destroy()
        main_screen()

    def openacn_screen():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.11, rely=.2, relwidth=.75, relheight=.6)

        def create_account():
            name = e_name.get()
            email = e_email.get().strip()  # here some strip() add extra
            adhar = e_adhar.get()
            mob = e_mob.get()
            age = e_age.get()
            gender = cb_gender.get()

            if len(name) == 0:
                messagebox.showerror("Open Account", "Name is required")
                return
            if len(email) == 0:
                messagebox.showerror("Open Account", "Email is required")
                return

            # match = re.fullmatch(
               # r"[a-zA-Z0-9_.$]+@[a-zA-Z0-9]+/.[a-zA-Z]+", email)
            match = re.fullmatch(
                r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
                email
            )
            if match == None:
                messagebox.showerror("Open Account", "Invalid Email")
                return

            if len(adhar) == 0:
                messagebox.showerror("Open Account", "Adhar is required")
                return

            if len(mob) == 0:
                messagebox.showerror("Open Account", "Mob is required")
                return
            bal = 0
            opendate = time.strftime("%A,%b %d %Y %r")
            pwd = mygenerator.generate_password()

            conobj = sqlite3.connect(database='bank.sqlite')
            curobj = conobj.cursor()
            query = 'insert into users values(null,?,?,?,?,?,?,?,?,?)'
            curobj.execute(query, (name, pwd, email, mob,
                           adhar, age, bal, gender, opendate))
            conobj.commit()
            conobj.close()

            conobj = sqlite3.connect(database='bank.sqlite')
            curobj = conobj.cursor()
            query = 'select max(acn) from users'
            curobj.execute(query)
            acn = curobj.fetchone()[0]
            conobj.close()
            mailhandler.send_openacn_email(email, name, acn, pwd)
            messagebox.showinfo(
                "Create Account", "Account opend and credentials are sent to email")
            reset()  # addd extra...

        def reset():  # add extra....
            e_name.delete(0, END)
            e_email.delete(0, END)
            e_mob.delete(0, END)
            e_adhar.delete(0, END)
            e_age.delete(0, END)
            cb_gender.current(0)

        lbl_ftitle = Label(ifrm, text="This is open account screen",
                           font=('arial', 20, 'bold'), bg='white', fg='purple')
        lbl_ftitle.pack()

        lbl_name = Label(ifrm, text="Name",
                         font=('arial', 20, 'bold'), bg='white')
        lbl_name.place(relx=.1, rely=.08)

        e_name = Entry(ifrm, font=('arial', 20), bd=5)
        e_name.place(relx=.1, rely=.16)

        lbl_email = Label(ifrm, text="Email",
                          font=('arial', 20, 'bold'), bg='white')
        lbl_email.place(relx=.1, rely=.28)

        e_email = Entry(ifrm, font=('arial', 20), bd=5)
        e_email.place(relx=.1, rely=.36)

        lbl_mob = Label(ifrm, text="Mob",
                        font=('arial', 20, 'bold'), bg='white')
        lbl_mob.place(relx=.1, rely=.48)

        e_mob = Entry(ifrm, font=('arial', 20), bd=5)
        e_mob.place(relx=.1, rely=.56)

        lbl_adhar = Label(ifrm, text="Adhar",
                          font=('arial', 20, 'bold'), bg='white')
        lbl_adhar.place(relx=.6, rely=.08)

        e_adhar = Entry(ifrm, font=('arial', 20), bd=5)
        e_adhar.place(relx=.6, rely=.16)

        lbl_age = Label(ifrm, text="Age",
                        font=('arial', 20, 'bold'), bg='white')
        lbl_age.place(relx=.6, rely=.28)

        e_age = Entry(ifrm, font=('arial', 20), bd=5)
        e_age.place(relx=.6, rely=.36)

        lbl_gender = Label(ifrm, text="Gender",
                           font=('arial', 20, 'bold'), bg='white')
        lbl_gender.place(relx=.6, rely=.48)

        cb_gender = Combobox(ifrm, font=('arial', 19), values=[
                             'Male', 'Female', 'Others'])
        cb_gender.current(0)
        cb_gender.place(relx=.6, rely=.57)

        submit_btn = Button(ifrm, text='Submit', bd=5,
                            font=('arial', 20, 'bold'), bg='#28a745', fg='white', cursor='hand2', command=create_account)
        submit_btn.place(relx=.35, rely=.8)
        apply_hover(submit_btn, "#218838")

        reset_btn = Button(ifrm, text='Reset', bd=5,
                           # add command=reset....
                           font=('arial', 20, 'bold'), bg='#fd7e14', fg='white', cursor='hand2', command=reset)
        reset_btn.place(relx=.55, rely=.8)
        apply_hover(reset_btn, "#e8590c")

    def viewacn_screen():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.11, rely=.2, relwidth=.75, relheight=.6)

        def search():
            acn = int(e_acn.get())
            conobj = sqlite3.connect(database='bank.sqlite')
            curobj = conobj.cursor()
            query = 'select name,bal,opendate,email,adhar from users where acn=?'
            curobj.execute(query, (acn,))
            row = curobj.fetchone()
            conobj.close()
            if row == None:
                messagebox.showerror("Search", "Account does not exist")
            else:
                # messagebox.showinfo("Search",row)
                details = f'Name = {row[0]}\nBal = {row[1]}'
                messagebox.showinfo("Search", details)

            reset()  # add extra...

        def reset():  # add extra....
            e_acn.delete(0, END)

        lbl_ftitle = Label(ifrm, text="This is view account screen",
                           font=('arial', 20, 'bold'), bg='white', fg='purple')
        lbl_ftitle.pack()

        lbl_acn = Label(ifrm, text="ACN",
                        font=('arial', 20, 'bold'), bg='white')
        lbl_acn.place(relx=.3, rely=.2)

        e_acn = Entry(ifrm, font=('arial', 20), bd=5)
        e_acn.place(relx=.4, rely=.2)

        search_btn = Button(ifrm, command=search, text='Search',
                            bd=5, font=('arial', 10), bg='#898B8D', fg='white', cursor='hand2')
        search_btn.place(relx=.75, rely=.2)

    def closeacn_screen():
        ifrm = Frame(frm, highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.11, rely=.2, relwidth=.75, relheight=.6)

        def close():
            acn = int(e_acn.get())

            conobj = sqlite3.connect(database='bank.sqlite')
            curobj = conobj.cursor()
            query = 'select name,email from users where acn=?'
            curobj.execute(query, (acn,))
            row = curobj.fetchone()
            conobj.close()
            if row == None:
                messagebox.showerror("Close Account", "Account does not exist")
            else:
                gen_otp = random.randint(1000, 9999)
                mailhandler.send_closeacn_email(row[1], row[0], gen_otp)
                user_otp = simpledialog.askinteger(
                    "Close Acccount", "Enter OTP")
                if user_otp == gen_otp:
                    conobj = sqlite3.connect(database='bank.sqlite')
                    curobj = conobj.cursor()
                    query = 'delete from users where acn=?'
                    curobj.execute(query, (acn,))
                    conobj.commit()
                    conobj.close()
                    messagebox.showinfo("Close Account", "Account Closed")
                else:
                    messagebox.showerror("Close Account", "Invalid OTP")
            reset()  # add extra...

        def reset():  # add extra....
            e_acn.delete(0, END)

        lbl_ftitle = Label(ifrm, text="This is close account screen",
                           font=('arial', 20, 'bold'), bg='white', fg='purple')
        lbl_ftitle.pack()

        lbl_acn = Label(ifrm, text="ACN",
                        font=('arial', 20, 'bold'), bg='white')
        lbl_acn.place(relx=.3, rely=.2)

        e_acn = Entry(ifrm, font=('arial', 20), bd=5)
        e_acn.place(relx=.4, rely=.2)

        close_btn = Button(ifrm, command=close, text='Close',
                           bd=5, font=('arial', 10), bg='#898B8D', fg="white", cursor='hand2')
        close_btn.place(relx=.75, rely=.2)

    logout_btn = Button(frm, text='Logout', bd=5,
                        font=('arial', 20, 'bold'), bg='#dc3545', fg='white', cursor='hand2', command=logout_click)
    logout_btn.place(relx=.92, rely=0)
    apply_hover(logout_btn, "#c82333")

    lbl_wel = Label(frm, text="Welcome, Admin",
                    font=('arial', 20, 'bold'), bg='#F1F3F4')
    lbl_wel.place(relx=0, rely=0)

    openacn_btn = Button(frm, text='Open Account', bd=5,
                         font=('arial', 20, 'bold'), bg='blue', fg='white', cursor='hand2', command=openacn_screen)
    openacn_btn.place(relx=.11, rely=.1)

    viewacn_btn = Button(frm, text='View Account', bd=5,
                         font=('arial', 20, 'bold'), bg='green', fg='white', cursor='hand2', command=viewacn_screen)
    viewacn_btn.place(relx=.41, rely=.1)

    closeacn_btn = Button(frm, text='Close Account', bd=5,
                          font=('arial', 20, 'bold'), bg='red', fg='white', cursor='hand2', command=closeacn_screen)
    closeacn_btn.place(relx=.71, rely=.1)


def fp_screen():
    frm = Frame(root, highlightbackground='black', highlightthickness=2)
    frm.configure(bg='#F1F3F4')
    frm.place(relx=0, rely=.183, relwidth=1, relheight=.76)

    def back_click():
        frm.destroy()
        main_screen()

    def fp_otp():
        user_acn = e_acn.get()
        user_email = e_email.get()

        conobj = sqlite3.connect(database='bank.sqlite')
        curobj = conobj.cursor()
        query = 'select name,pass from users where acn=? and email=?'
        curobj.execute(query, (user_acn, user_email))
        tup = curobj.fetchone()
        conobj.close()

        if tup == None:
            messagebox.showerror("Forgot Password", "ACN does not exist")
            return

        gen_otp = random.randint(1000, 9999)
        mailhandler.send_fpotp_email(user_email, tup[0], gen_otp)
        user_otp = simpledialog.askinteger("Forgot Pass", "OTP")
        if user_otp == None:
            return

        if gen_otp == user_otp:
            messagebox.showinfo("Forgot Password", f"Your Pass = {tup[1]}")

    back_btn = Button(frm, text='Back', bd=5,
                      font=('arial', 20, 'bold'), bg='#6c757d', fg='white', cursor='hand2', command=back_click)
    back_btn.place(relx=0, rely=.002)
    apply_hover(back_btn, "#5a6268")

    lbl_acn = Label(frm, text="User ACN",
                    font=('arial', 20, 'bold'), bg='#F1F3F4')
    lbl_acn.place(relx=.3, rely=.2)

    e_acn = Entry(frm, font=('arial', 20), bd=5)
    e_acn.place(relx=.45, rely=.2)

    lbl_email = Label(frm, text="User Email",
                      font=('arial', 20, 'bold'), bg='#F1F3F4')
    lbl_email.place(relx=.3, rely=.3)

    e_email = Entry(frm, font=('arial', 20), bd=5)
    e_email.place(relx=.45, rely=.3)

    otp_btn = Button(frm, text='Validate & Send OTP', bd=5,
                     font=('arial', 16, 'bold'), bg='#6f42c1', fg='white', cursor='hand2', command=fp_otp)
    otp_btn.place(relx=.47, rely=.42)
    apply_hover(otp_btn, "#59359a")


def main_screen():
    frm = Frame(root, highlightbackground='black', highlightthickness=2)
    frm.configure(bg='#F1F3F4')  # change color #F1F3F4 to ....
    frm.place(relx=0, rely=.183, relwidth=1, relheight=.76)

    def fp_click():
        frm.destroy()
        fp_screen()

    def reset():
        e_acn.delete(0, "end")
        e_pass.delete(0, "end")
        e_captcha.delete(0, "end")
        cb_user.current(2)

    def login_click():
        global user_acn
        user_type = cb_user.get()
        user_acn = e_acn.get()
        user_pass = e_pass.get()
        user_captcha = e_captcha.get()
        if user_type == "Admin" and user_acn == '0' and user_pass == "Admin" and user_captcha == captcha.replace(' ', ''):
            frm.destroy()
            admin_screen()
        elif user_type == "Customer" and user_captcha == captcha.replace(' ', ''):
            conobj = sqlite3.connect(database='bank.sqlite')
            curobj = conobj.cursor()
            query = 'select * from users where acn=? and pass=?'
            curobj.execute(query, (user_acn, user_pass))
            row = curobj.fetchone()
            conobj.close()
            if row == None:
                messagebox.showerror("Login", "Invalid ACN/Pass")
            else:

                frm.destroy()
                customer_screen()
        else:
            messagebox.showerror("User Type", "Invalid Credentials")

    lbl_user = Label(frm, text="User Type",
                     font=('arial', 20, 'bold'), bd=5, bg='#F1F3F4')
    lbl_user.place(relx=.3, rely=.1)

    cb_user = Combobox(frm, values=['Customer', 'Admin', '---Select---'],
                       font=('arial', 19))
    cb_user.current(2)
    cb_user.config(state='readonly')
    cb_user.place(relx=.45, rely=.1, width=304, height=40)

    lbl_acn = Label(frm, text="User ACN",
                    font=('arial', 20, 'bold'), bg='#F1F3F4')
    lbl_acn.place(relx=.3, rely=.2)

    e_acn = Entry(frm, font=('arial', 20), bd=5)
    e_acn.place(relx=.45, rely=.2, width=305, height=45)

    lbl_pass = Label(frm, text="User Pass",
                     font=('arial', 20, 'bold'), bg='#F1F3F4')
    lbl_pass.place(relx=.3, rely=.3)

    e_pass = Entry(frm, font=('arial', 20), bd=5, show='*')
    e_pass.place(relx=.45, rely=.3, width=305, height=45)

    captcha = mygenerator.generate_captcha()

    lbl_show_cap = Label(frm, text=captcha,
                         font=('arial', 20, 'bold'), bg='white', fg='purple', width=8)
    lbl_show_cap.place(relx=.47, rely=.42)

    def refresh_captcha():
        nonlocal captcha
        captcha = mygenerator.generate_captcha()
        lbl_show_cap.configure(text=captcha)

    ref_btn = Button(frm, text='🔄refresh', bg='#17a2b8', fg='white', bd=5,  width=8, cursor='hand2',
                     font=('arial', 11, 'bold'), command=refresh_captcha)
    ref_btn.place(relx=.58, rely=.42)
    apply_hover(ref_btn, "#138496")

    lbl_captch = Label(frm, text="User Captcha",
                       font=('arial', 20, 'bold'), bg='#F1F3F4')
    lbl_captch.place(relx=.3, rely=.52)

    e_captcha = Entry(frm, font=('arial', 14), bd=5)
    e_captcha.place(relx=.45, rely=.52, width=305, height=45)

    login_btn = Button(frm, text='Login', bd=5,
                       font=('arial', 16, 'bold'), bg="#28a745", fg='white', cursor='hand2', command=login_click)
    login_btn.place(relx=.47, rely=.64)
    apply_hover(login_btn, "#218838")

    reset_btn = Button(frm, text='Reset', command=reset, bd=5,
                       font=('arial', 16, 'bold'), bg='#fd7e14', cursor='hand2', fg='white')
    reset_btn.place(relx=.57, rely=.64)
    apply_hover(reset_btn, "#e8590c")

    fp_btn = Button(frm, text='Forgot Password', width=18, bd=5,
                    font=('arial', 16, 'bold'), bg="#007bff", fg='white', cursor='hand2', command=fp_click)
    fp_btn.place(relx=.466, rely=.75)
    apply_hover(fp_btn, "#0056b3")


# for button Hover....
def apply_hover(btn, hover_color):
    normal_color = btn["bg"]

    btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
    btn.bind("<Leave>", lambda e: btn.config(bg=normal_color))

root = Tk()
root.state('zoomed')
root.configure(bg='#BDC1C6')  
root.resizable(width=False, height=False)

lbl_title = Label(root, text="Banking Simulation",     
                  font=('arial', 50, 'bold', 'underline'), bg='#BDC1C6')
lbl_title.pack()

lbl_dt = Label(root, text=time.strftime("%A,%b %d %Y ⏰%r"),
               font=('arial', 20, 'bold'), bg='#BDC1C6', fg='#0B1CB2')
lbl_dt.pack(pady=20)
update_time()


img1 = Image.open('logo.jpg').resize((250, 150))
imgtk1 = ImageTk.PhotoImage(img1, master=root)

lbl_logo = Label(root, image=imgtk1)
lbl_logo.place(relx=0, rely=0)

img2 = Image.open('logo.png').resize((300, 250))
imgtk2 = ImageTk.PhotoImage(img2, master=root)

lbl_logo = Label(root, image=imgtk2, bg='#BDC1C6')
lbl_logo.place(relx=.83, rely=-.04)


lbl_footer = Label(root, text="Developed By : Kapil@ ....",
                   font=('arial', 16, 'bold'), bg='#BDC1C6', fg="#0B1CB2")
lbl_footer.pack(side='bottom', pady=10)
main_screen()
root.mainloop()
