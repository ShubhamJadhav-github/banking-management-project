from tkinter import *
from tkcalendar import *
from tkinter import messagebox
import mysql.connector
import os
from PIL import Image, ImageTk
import datetime

f1 = ('calibre', 15, 'bold')
f2 = ('calibre', 10)
f3 = ('calibre', 15)


class BankWindows:

    def __init__(self):
        self.showmainwindow()

    @staticmethod
    def show_close_account_window(win2):
        def closeacfunction(acno):
            reason = closeacreasonentry.get(1.0, 'end-1c')
            if reason == "":
                messagebox.showerror("Empty Field", "Please provide reason to close the account")
            else:
                mydb = mysql.connector.connect(host='localhost',
                                               database='bank',
                                               user='root',
                                               charset='utf8',
                                               password='')
                mycur = mydb.cursor()
                mycur.execute("select * from applicant where apno = " + str(acno))
                resultofcloseacc = mycur.fetchone()
                if mycur.rowcount == 0:
                    messagebox.showerror("Something Went Wrong !!!", "Account Not Found in Database")
                else:
                    confirm = messagebox.askyesnocancel("Are You Sure ?",
                                                        "\nAccount No = "
                                                        + str(acno) +
                                                        "\nAccount Holder's Name = "
                                                        + str(resultofcloseacc[1]) +
                                                        "\nReturning Amount = "
                                                        + str(resultofcloseacc[8]) +
                                                        "\nDo You Really Want To Close The Account ?")
                    if confirm:
                        name = resultofcloseacc[1]
                        add = resultofcloseacc[2]
                        city = resultofcloseacc[3]
                        nomini = resultofcloseacc[7]
                        returnamount = resultofcloseacc[8]

                        today = datetime.date.today()
                        formatted_date = today.strftime("%d-%m-%Y")

                        quer = "insert into closeacc (cldate, apno, reason, ramount) values('" + formatted_date + "', " + str(
                            acno) + ", '" + reason + "', '" + str(returnamount) + "')"
                        mycur.execute(quer)
                        mydb.commit()

                        quer = "delete from applicant where apno = " + str(acno)
                        mycur.execute(quer)
                        mydb.commit()

                        if mycur.rowcount == 0:
                            messagebox.showerror("Something Went Wrong", "Unable to close the account")
                        else:
                            messagebox.showinfo("Done",
                                                "Account Has Been Closed Successfully!!\nAccount No = " + str(acno) +
                                                "\nAccout Holder's Name = " + name +
                                                "\nAddress = " + add +
                                                "\nCity = " + city +
                                                "\nNomini = " + nomini +
                                                "\nAmount Returned = " + str(returnamount))
                            closeaccountwindow.destroy()

        def searchaccount():
            ac = searchbarentry.get()
            if ac == '':
                messagebox.showerror("Empty Field", "Please Provide Account Number")
            else:
                try:
                    ac = int(searchbarentry.get())
                    mydb = mysql.connector.connect(host='localhost',
                                                   user='root',
                                                   password='',
                                                   charset='utf8',
                                                   database='bank')
                    mycur = mydb.cursor()
                    queu = "select * from applicant where apno=" + str(ac)
                    mycur.execute(queu)
                    result = mycur.fetchone()
                    if result is not None:
                        labelnameanswer.config(text=result[1])
                        labelname.place(x=55, y=70)
                        labelnameanswer.place(x=300, y=71)

                        labeladdanswer.config(text=result[2])
                        labeladd.place(x=55, y=120)
                        labeladdanswer.place(x=300, y=120)

                        labelcityanswer.config(text=result[3])
                        labelcity.place(x=55, y=170)
                        labelcityanswer.place(x=300, y=170)

                        labelcontactanswer.config(text=result[4])
                        labelcontact.place(x=55, y=220)
                        labelcontactanswer.place(x=300, y=220)

                        labelbdateanswer.config(text=result[5])
                        labelbdate.place(x=55, y=270)
                        labelbdateanswer.place(x=300, y=270)

                        labelgenderanswer.config(text=result[6])
                        labelgender.place(x=55, y=320)
                        labelgenderanswer.place(x=300, y=320)

                        labelnominianswer.config(text=result[7])
                        labelnomini.place(x=55, y=370)
                        labelnominianswer.place(x=300, y=370)

                        labelbalanceanswer.config(text=result[8])
                        labelbalance.place(x=55, y=420)
                        labelbalanceanswer.place(x=300, y=420)

                        closeacreasonlabel.place(x=20, y=470)
                        closeacreasonentry.place(x=300, y=470)
                        closeacbutton.place(x=250, y=570)
                        closeacbutton.config(command=lambda: closeacfunction(ac))

                    elif mycur.rowcount == 0:
                        # To Hide all the elements in the window
                        for widget in closeaccountwindow.winfo_children():
                            widget.place_forget()
                        searchbarlabel.place(x=20, y=20)
                        searchbarentry.place(x=300, y=20)
                        searchbtn.place(x=530, y=20)
                        messagebox.showerror("Not Found", "Account Does Not Exists")
                    else:
                        messagebox.showerror("Not Found", "Account Does Not Exists")
                except ValueError:
                    messagebox.showerror("Invalid", "Account number contains only numbers")

        closeaccountwindow = Toplevel(win2)
        closeaccountwindow.title("close")
        closeaccountwindow.geometry("600x650+475+80")
        closeaccountwindow.resizable(False, False)

        searchbarlabel = Label(closeaccountwindow, text="Search by Account Number", font=f1)
        searchbarlabel.place(x=20, y=20)
        searchbarentry = Entry(closeaccountwindow, font=f1)
        searchbarentry.place(x=300, y=20)
        searchbtn = Button(closeaccountwindow, text="Search", font=f2, command=searchaccount)
        searchbtn.place(x=530, y=20)

        labelname = Label(closeaccountwindow, font=f1, text="Account Holder's Name")
        labelnameanswer = Label(closeaccountwindow, font=f3, text="Shubham", fg='blue')

        labeladd = Label(closeaccountwindow, font=f1, text="Address")
        labeladdanswer = Label(closeaccountwindow, font=f3, text="Walwadi", fg='blue')

        labelcity = Label(closeaccountwindow, font=f1, text="City")
        labelcityanswer = Label(closeaccountwindow, font=f3, fg='blue', text="Dhule")

        labelcontact = Label(closeaccountwindow, font=f1, text="Contact")
        labelcontactanswer = Label(closeaccountwindow, font=f3, fg='blue', text="9898989898")

        labelbdate = Label(closeaccountwindow, font=f1, text="Date of Birth")
        labelbdateanswer = Label(closeaccountwindow, font=f3, fg='blue', text="08-06-2002")

        labelgender = Label(closeaccountwindow, font=f1, text="Gender")
        labelgenderanswer = Label(closeaccountwindow, font=f3, fg='blue', text='Male')

        labelnomini = Label(closeaccountwindow, font=f1, text='Nomini')
        labelnominianswer = Label(closeaccountwindow, font=f3, fg='blue', text='Chetana')

        labelbalance = Label(closeaccountwindow, font=f1, text="Returning Amount")
        labelbalanceanswer = Label(closeaccountwindow, font=f3, fg='blue', text='30000')

        closeacreasonlabel = Label(closeaccountwindow, text='Reason To close Amount', font=f1)
        closeacreasonentry = Text(closeaccountwindow, height=3, width=20, font=f1)

        closeacbutton = Button(closeaccountwindow, text='close', font=f1, command=closeacfunction)

        # Make the Save As dialog modal (disable main window)
        closeaccountwindow.transient(win2)
        closeaccountwindow.grab_set()
        win2.wait_window(closeaccountwindow)  # Wait for the dialog to be closed before continuing
        closeaccountwindow.mainloop()

    @staticmethod
    def show_withdrawl_amount_window(win2):
        def withdrawlmoneyfunction(acno):
            withdrawlamount = withdrawlamountentry.get()

            if withdrawlamount == '':
                messagebox.showerror("Empty Field", "Please Enter withdrawl Amount")
            else:
                try:
                    withdrawlamount = int(withdrawlamountentry.get())
                    mydb = mysql.connector.connect(host='localhost',
                                                   database='bank',
                                                   user='root',
                                                   charset='utf8',
                                                   password='')
                    mycur = mydb.cursor()
                    mycur.execute("select * from applicant where apno = " + str(acno))
                    result = mycur.fetchone()
                    if result is not None:
                        mycur.execute("select balance from applicant where apno = " + str(acno))
                        result = mycur.fetchone()
                        if withdrawlamount > result[0]:
                            messagebox.showerror("Balance Problem", "Insufficient Balance")
                        else:
                            balance = result[0] - withdrawlamount
                            today = datetime.date.today()
                            formatted_date = today.strftime("%d-%m-%Y")
                            que = "update applicant set balance = " + str(balance) + " where apno = " + str(acno)
                            mycur.execute(que)
                            mydb.commit()
                            que = "insert into withdrawl(sldate, apno, amount) values('" + formatted_date + "', '" + str(
                                acno) + "', '" + str(withdrawlamount) + "')"
                            mycur.execute(que)
                            mydb.commit()
                            if mycur.rowcount == 0:
                                messagebox.showerror("Something Went Wront", "Unable to Make Transaction")
                            else:
                                messagebox.showinfo("Done", "Transaction has been done successfully\nAccount No = " + str(
                                    acno) + "\nwithdrawl Amount = " + str(withdrawlamount))
                            withdrawlwindow.destroy()
                except ValueError:
                    messagebox.showerror("Invalid", "Invalid Amount")

        def searchaccountforwithdrawl():
            ac = searchbarentry.get()
            if ac == '':
                messagebox.showerror("Empty Field", "Please Provide Account Number")
            else:
                try:
                    ac = int(searchbarentry.get())
                    mydb = mysql.connector.connect(host='localhost',
                                                   user='root',
                                                   password='',
                                                   charset='utf8',
                                                   database='bank')
                    mycur = mydb.cursor()
                    q = "select * from applicant where apno=" + str(ac)
                    mycur.execute(q)
                    result = mycur.fetchone()
                    if result is not None:

                        labelnameanswer.config(text=result[1])
                        labelname.place(x=55, y=70)
                        labelnameanswer.place(x=300, y=71)

                        labeladdanswer.config(text=result[2])
                        labeladd.place(x=55, y=120)
                        labeladdanswer.place(x=300, y=120)

                        labelcityanswer.config(text=result[3])
                        labelcity.place(x=55, y=170)
                        labelcityanswer.place(x=300, y=170)

                        labelcontactanswer.config(text=result[4])
                        labelcontact.place(x=55, y=220)
                        labelcontactanswer.place(x=300, y=220)

                        labelbalanceanswer.config(text=result[8])
                        labelbalance.place(x=55, y=270)
                        labelbalanceanswer.place(x=300, y=270)

                        withdrawlamountlabel.place(x=20, y=320)
                        withdrawlamountentry.place(x=300, y=320)

                        withdrawlbutton.place(x=250, y=370)
                        withdrawlbutton.config(command=lambda: withdrawlmoneyfunction(result[0]))

                    elif mycur.rowcount == 0:
                        # To Hide all the elements in the window
                        for widget in withdrawlwindow.winfo_children():
                            widget.place_forget()
                        searchbarlabel.place(x=20, y=20)
                        searchbarentry.place(x=300, y=20)
                        searchbtn.place(x=530, y=20)
                        messagebox.showerror("Not Found", "Account Does Not Exists")
                    else:
                        messagebox.showerror("Not Found", "Account Does Not Exists")
                except ValueError:
                    messagebox.showerror("Invalid", "Account number contains only numbers")

        withdrawlwindow = Toplevel(win2)
        withdrawlwindow.title("Withdrawl")
        withdrawlwindow.geometry("600x550+475+150")
        withdrawlwindow.resizable(False, False)

        searchbarlabel = Label(withdrawlwindow, text="Search by Account Number", font=f1)
        searchbarlabel.place(x=20, y=20)
        searchbarentry = Entry(withdrawlwindow, font=f1)
        searchbarentry.place(x=300, y=20)
        searchbtn = Button(withdrawlwindow, text="Search", font=f2, command=searchaccountforwithdrawl)
        searchbtn.place(x=530, y=20)

        labelname = Label(withdrawlwindow, font=f1, text="Account Holder's Name")
        labelnameanswer = Label(withdrawlwindow, font=f3, text="-----", fg='blue')

        labeladd = Label(withdrawlwindow, font=f1, text="Address")
        labeladdanswer = Label(withdrawlwindow, font=f3, text="-----", fg='blue')

        labelcity = Label(withdrawlwindow, font=f1, text="City")
        labelcityanswer = Label(withdrawlwindow, font=f3, fg='blue', text="-----")

        labelcontact = Label(withdrawlwindow, font=f1, text="Contact")
        labelcontactanswer = Label(withdrawlwindow, font=f3, fg='blue', text="-------")

        labelbalance = Label(withdrawlwindow, font=f1, text="Balance")
        labelbalanceanswer = Label(withdrawlwindow, font=f3, fg='blue', text='------')

        withdrawlamountlabel = Label(withdrawlwindow, text='Enter withdrawl Amount', font=f1)
        withdrawlamountentry = Entry(withdrawlwindow, font=f1)

        withdrawlbutton = Button(withdrawlwindow, text='withdrawl', font=f1, command=withdrawlmoneyfunction)

        # Make the Save As dialog modal (disable main window)
        withdrawlwindow.transient(win2)
        withdrawlwindow.grab_set()
        win2.wait_window(withdrawlwindow)  # Wait for the dialog to be closed before continuing
        withdrawlwindow.mainloop()

    @staticmethod
    def show_search_account_details_window(win2):

        def searchaccountdetails():
            ac = searchbarentry.get()
            if ac == '':
                messagebox.showerror("Empty Field", "Please Provide Account Number")
            else:
                try:
                    ac = int(searchbarentry.get())
                    mydb = mysql.connector.connect(host='localhost',
                                                   user='root',
                                                   password='',
                                                   charset='utf8',
                                                   database='bank')
                    mycur = mydb.cursor()
                    q = "select * from applicant where apno=" + str(ac)
                    mycur.execute(q)
                    result = mycur.fetchone()
                    if result is not None:
                        labelnameanswer.config(text=result[1])
                        labelname.place(x=55, y=70)
                        labelnameanswer.place(x=300, y=71)

                        labeladdanswer.config(text=result[2])
                        labeladd.place(x=55, y=120)
                        labeladdanswer.place(x=300, y=120)

                        labelcityanswer.config(text=result[3])
                        labelcity.place(x=55, y=170)
                        labelcityanswer.place(x=300, y=170)

                        labelcontactanswer.config(text=result[4])
                        labelcontact.place(x=55, y=220)
                        labelcontactanswer.place(x=300, y=220)

                        labelbdateanswer.config(text=result[5])
                        labelbdate.place(x=55, y=270)
                        labelbdateanswer.place(x=300, y=270)

                        labelgenderanswer.config(text=result[6])
                        labelgender.place(x=55, y=320)
                        labelgenderanswer.place(x=300, y=320)

                        labelnominianswer.config(text=result[7])
                        labelnomini.place(x=55, y=370)
                        labelnominianswer.place(x=300, y=370)

                        labelbalanceanswer.config(text=result[8])
                        labelbalance.place(x=55, y=420)
                        labelbalanceanswer.place(x=300, y=420)

                    elif mycur.rowcount == 0:
                        # To Hide all the elements in the window
                        for widget in searchwindow.winfo_children():
                            widget.place_forget()
                        searchbarlabel.place(x=20, y=20)
                        searchbarentry.place(x=300, y=20)
                        searchbtn.place(x=530, y=20)
                        messagebox.showerror("Not Found", "Account Does Not Exists")
                    else:
                        messagebox.showerror("Not Found", "Account Does Not Exists")
                except ValueError:
                    messagebox.showerror("Invalid", "Account number contains only numbers")

        searchwindow = Toplevel(win2)
        searchwindow.title("Search Account Details")
        searchwindow.geometry("600x550+475+150")
        searchwindow.resizable(False, False)

        searchbarlabel = Label(searchwindow, text="Search by Account Number", font=f1)
        searchbarentry = Entry(searchwindow, font=f1)
        searchbtn = Button(searchwindow, text="Search", font=f2, command=searchaccountdetails)
        searchbarlabel.place(x=20, y=20)
        searchbarentry.place(x=300, y=20)
        searchbtn.place(x=530, y=20)

        labelname = Label(searchwindow, font=f1, text="Account Holder's Name")
        labelnameanswer = Label(searchwindow, font=f3, text="Shubham", fg='blue')

        labeladd = Label(searchwindow, font=f1, text="Address")
        labeladdanswer = Label(searchwindow, font=f3, text="Walwadi", fg='blue')

        labelcity = Label(searchwindow, font=f1, text="City")
        labelcityanswer = Label(searchwindow, font=f3, fg='blue', text="Dhule")

        labelcontact = Label(searchwindow, font=f1, text="Contact")
        labelcontactanswer = Label(searchwindow, font=f3, fg='blue', text="9898989898")

        labelbdate = Label(searchwindow, font=f1, text="Date of Birth")
        labelbdateanswer = Label(searchwindow, font=f3, fg='blue', text="08-06-2002")

        labelgender = Label(searchwindow, font=f1, text="Gender")
        labelgenderanswer = Label(searchwindow, font=f3, fg='blue', text='Male')

        labelnomini = Label(searchwindow, font=f1, text='Nomini')
        labelnominianswer = Label(searchwindow, font=f3, fg='blue', text='Chetana')

        labelbalance = Label(searchwindow, font=f1, text="Balance")
        labelbalanceanswer = Label(searchwindow, font=f3, fg='blue', text='30000')

        # Make the Save As dialog modal (disable main window)
        searchwindow.transient(win2)
        searchwindow.grab_set()
        win2.wait_window(searchwindow)  # Wait for the dialog to be closed before continuing
        searchwindow.mainloop()

    @staticmethod
    def show_deposit_window(win2):
        def depositemoneyfunction(acno):
            # transactiontype = trtype.get()
            depositamount = depositamountentry.get()
            depositparticulars = trtype.get()
            if depositparticulars == 0:
                depositparticulars = "Cash"
            elif depositparticulars == 1:
                depositparticulars = "Cheque"
            elif depositparticulars == 2:
                depositparticulars = "Money Order"
            elif depositparticulars == 3:
                depositparticulars = "Demand Draft"

            if depositamount == '':
                messagebox.showerror("Empty Field", "Please Enter Deposite Amount")
            else:
                try:
                    depositamount = int(depositamountentry.get())
                    mydb = mysql.connector.connect(host='localhost',
                                                   database='bank',
                                                   user='root',
                                                   charset='utf8',
                                                   password='')
                    mycur = mydb.cursor()
                    mycur.execute("select balance from applicant where apno = " + str(acno))
                    result = mycur.fetchone()
                    totalamount = depositamount + result[0]
                    today = datetime.date.today()
                    formatted_date = today.strftime("%d-%m-%Y")
                    qu = "insert into deposit(sldate, apno, perticular, amount) values('" + formatted_date + "', " + str(
                        acno) + ", '" + depositparticulars + "', " + str(depositamount) + ")"
                    mycur.execute(qu)
                    mydb.commit()
                    qu = "update applicant set balance=" + str(totalamount) + " where apno=" + str(acno)
                    mycur.execute(qu)
                    mydb.commit()
                    if mycur.rowcount == 0:
                        messagebox.showerror("Something Went Wront", "Unable to Make Transaction")
                    else:
                        messagebox.showinfo("Done", "Transaction has been done successfully\nAccount No = " + str(
                            acno) + "\nDeposit Amount = " + str(depositamount))
                        depositwindow.destroy()
                except ValueError:
                    messagebox.showerror("Invalid", "Invalid Amount")

        def searchaccount():
            ac = searchbarentry.get()
            if ac == '':
                messagebox.showerror("Empty Field", "Please Provide Account Number")
            else:
                try:
                    ac = int(searchbarentry.get())
                    mydb = mysql.connector.connect(host='localhost',
                                                   user='root',
                                                   password='',
                                                   charset='utf8',
                                                   database='bank')
                    mycur = mydb.cursor()
                    q = "select * from applicant where apno=" + str(ac)
                    mycur.execute(q)
                    result = mycur.fetchone()
                    if result is not None:
                        depositamountlabel.place(x=50, y=70)
                        depositamountentry.place(x=300, y=70)

                        transactiontypelabel.place(x=110, y=120)
                        cash.place(x=300, y=120)
                        cheque.place(x=300, y=170)
                        moneyorder.place(x=300, y=220)
                        demanddraft.place(x=300, y=270)

                        depositbutton.place(x=250, y=470)
                        depositbutton.config(command=lambda: depositemoneyfunction(result[0]))

                    elif mycur.rowcount == 0:
                        # To Hide all the elements in the window
                        for widget in depositwindow.winfo_children():
                            widget.place_forget()
                        searchbarlabel.place(x=20, y=20)
                        searchbarentry.place(x=300, y=20)
                        searchbtn.place(x=530, y=20)
                        messagebox.showerror("Not Found", "Account Does Not Exists")
                    else:
                        messagebox.showerror("Not Found", "Account Does Not Exists")
                except ValueError:
                    messagebox.showerror("Invalid", "Account number contains only numbers")

        depositwindow = Toplevel(win2)
        depositwindow.title("Deposite")
        depositwindow.geometry("600x550+475+150")
        depositwindow.resizable(False, False)

        searchbarlabel = Label(depositwindow, text="Search by Account Number", font=f1)
        searchbarlabel.place(x=20, y=20)
        searchbarentry = Entry(depositwindow, font=f1)
        searchbarentry.place(x=300, y=20)
        searchbtn = Button(depositwindow, text="Search", font=f2, command=searchaccount)
        searchbtn.place(x=530, y=20)

        depositamountlabel = Label(depositwindow, text='Enter Deposite Amount', font=f1)
        depositamountentry = Entry(depositwindow, font=f1)

        transactiontypelabel = Label(depositwindow, text='Transaction type', font=f1)
        trtype = IntVar()
        cash = Radiobutton(depositwindow, text="Cash", font=f1, variable=trtype, value=0)
        cheque = Radiobutton(depositwindow, text="Cheque", font=f1, variable=trtype, value=1)
        moneyorder = Radiobutton(depositwindow, text="Money Order", font=f1, variable=trtype, value=2)
        demanddraft = Radiobutton(depositwindow, text="Demand Draft", font=f1, variable=trtype, value=3)
        depositbutton = Button(depositwindow, text='Deposit', font=f1, command=depositemoneyfunction)

        # Make the Save As dialog modal (disable main window)
        depositwindow.transient(win2)
        depositwindow.grab_set()
        win2.wait_window(depositwindow)  # Wait for the dialog to be closed before continuing
        depositwindow.mainloop()

    @staticmethod
    def show_change_account_details_window(win2):

        def submitchangedinfo(apno):
            cname = nameentry.get()
            cadd = addentry.get()
            ccity = cityentry.get()
            ccontact = contactentry.get()
            cbdate = bdateentry.get()
            cgender = v1.get()
            if cgender == 0:
                cgender = 'Male'
            elif cgender == 1:
                cgender = 'Female'
            elif cgender == 2:
                cgender = 'Other'

            cnomini = nominientry.get()

            if cname == "" or cadd == "" or ccity == "" or ccontact == "" or cbdate == "" or cgender == "" or cnomini == "":
                messagebox.showerror("Empty Field", "Empty Field Not Allowed")
            else:
                try:
                    ccontact = int(contactentry.get())
                    mydb = mysql.connector.connect(host='localhost',
                                                   password='',
                                                   user='root',
                                                   database='bank',
                                                   charset='utf8')
                    mycur = mydb.cursor()
                    q = (
                            "update applicant set apname='" + cname + "', apadd='" + cadd + "', city='" + ccity + "', contact='" +
                            str(ccontact) + "', bdate='" + cbdate + "', gender='" + cgender + "', nomini='" + cnomini +
                            "' where apno=" + str(apno))
                    mycur.execute(q)
                    mydb.commit()
                    if mycur.rowcount != 0:
                        messagebox.showinfo("Done", "Account Details Updated Successfully")
                    else:
                        messagebox.showerror("Unable to create account", "Something Went Wrong !!!")

                except ValueError:
                    messagebox.showinfo("Invalid", "Invalid Contact Number")
                    contactentry.delete(0, END)

        def searchaccount():
            ac = searchbarentry.get()
            if ac == '':
                messagebox.showerror("Empty Field", "Please Provide Account Number")
            else:
                try:
                    ac = int(searchbarentry.get())
                    mydb = mysql.connector.connect(host='localhost',
                                                   user='root',
                                                   password='',
                                                   charset='utf8',
                                                   database='bank')
                    mycur = mydb.cursor()
                    q = "select * from applicant where apno=" + str(ac)
                    mycur.execute(q)
                    result = mycur.fetchone()
                    if result is not None:
                        namelabel.place(x=50, y=70)
                        nameentry.place(x=300, y=70)
                        nameentry.delete(0, END)
                        nameentry.insert(0, result[1])

                        addlabel.place(x=85, y=120)
                        addentry.place(x=300, y=120)
                        addentry.delete(0, END)
                        addentry.insert(0, result[2])

                        citylabel.place(x=232, y=170)
                        cityentry.place(x=300, y=170)
                        cityentry.delete(0, END)
                        cityentry.insert(0, result[3])

                        contactlabel.place(x=195, y=220)
                        contactentry.place(x=300, y=220)
                        contactentry.delete(0, END)
                        contactentry.insert(0, result[4])

                        bdatelabel.place(x=150, y=270)
                        bdateentry.place(x=300, y=273)
                        bdateentry.delete(0, END)
                        bdateentry.insert(0, result[5])

                        genderlabel.place(x=200, y=320)
                        m.place(x=300, y=320)
                        f.place(x=375, y=320)
                        o.place(x=470, y=320)
                        if result[6] == 'Male':
                            v1.set(0)
                        elif result[6] == 'Female':
                            v1.set(1)
                        elif result[6] == 'Other':
                            v1.set(2)

                        nominilabel.place(x=205, y=370)
                        nominientry.place(x=300, y=370)
                        nominientry.delete(0, END)
                        nominientry.insert(0, result[7])

                        submitbutton.place(x=250, y=470)
                        submitbutton.config(command=lambda: submitchangedinfo(result[0]))

                    elif mycur.rowcount == 0:
                        # To Hide all the elements in the window
                        for widget in changeaccountdetailswindow.winfo_children():
                            widget.place_forget()
                        searchbarlabel.place(x=20, y=20)
                        searchbarentry.place(x=300, y=20)
                        searchbtn.place(x=530, y=20)
                        messagebox.showerror("Not Found", "Account Does Not Exists")
                    else:
                        messagebox.showerror("Not Found", "Account Does Not Exists")
                except ValueError:
                    messagebox.showerror("Invalid", "Account number contains only numbers")

        changeaccountdetailswindow = Toplevel(win2)
        changeaccountdetailswindow.title("Change Account Info")
        changeaccountdetailswindow.geometry("600x550+475+150")
        changeaccountdetailswindow.resizable(False, False)
        v1 = IntVar()

        searchbarlabel = Label(changeaccountdetailswindow, text="Search by Account Number", font=f1)
        searchbarlabel.place(x=20, y=20)
        searchbarentry = Entry(changeaccountdetailswindow, font=f1)
        searchbarentry.place(x=300, y=20)
        searchbtn = Button(changeaccountdetailswindow, text="Search", font=f2, command=searchaccount)
        searchbtn.place(x=530, y=20)

        namelabel = Label(changeaccountdetailswindow, text="Account Holder's Name", font=f1)
        nameentry = Entry(changeaccountdetailswindow, font=f1)

        addlabel = Label(changeaccountdetailswindow, text="Permanant Address", font=f1)
        addentry = Entry(changeaccountdetailswindow, font=f1)

        citylabel = Label(changeaccountdetailswindow, text="City", font=f1)
        cityentry = Entry(changeaccountdetailswindow, font=f1)

        contactlabel = Label(changeaccountdetailswindow, text="Contact", font=f1)
        contactentry = Entry(changeaccountdetailswindow, font=f1)

        bdatelabel = Label(changeaccountdetailswindow, text="Date of Birth", font=f1)
        bdateentry = DateEntry(changeaccountdetailswindow, font=f2, date_pattern='dd-mm-yyyy', setmode='day')

        genderlabel = Label(changeaccountdetailswindow, text="Gender", font=f1)
        m = Radiobutton(changeaccountdetailswindow, text='Male', font=('calibre', 13, 'bold'), variable=v1, value=0)
        f = Radiobutton(changeaccountdetailswindow, text='Female', font=('calibre', 13, 'bold'), variable=v1, value=1)
        o = Radiobutton(changeaccountdetailswindow, text='Other', font=('calibre', 13, 'bold'), variable=v1, value=2)

        nominilabel = Label(changeaccountdetailswindow, text="Nomini", font=f1)
        nominientry = Entry(changeaccountdetailswindow, font=f1)

        submitbutton = Button(changeaccountdetailswindow, font=f1, text='Update', command=submitchangedinfo)

        # Make the Save As dialog modal (disable main window)
        changeaccountdetailswindow.transient(win2)
        changeaccountdetailswindow.grab_set()
        win2.wait_window(changeaccountdetailswindow)  # Wait for the dialog to be closed before continuing
        changeaccountdetailswindow.mainloop()

    @staticmethod
    def show_create_account_window(win2):

        def submitinfo():
            cname = nameentry.get()
            cadd = addentry.get()
            ccity = cityentry.get()
            ccontact = contactentry.get()
            cbdate = bdateentry.get()

            cgender = ""
            if v1.get() == 0:
                cgender = 'Male'
            elif v1.get() == 1:
                cgender = 'Female'
            elif v1.get() == 2:
                cgender = 'Other'

            cnomini = nominientry.get()

            if cname == "" or cadd == "" or ccity == "" or ccontact == "" or cbdate == "" or cgender == "" or cnomini == "":
                messagebox.showerror("Empty Field", "Empty Field Not Allowed")
            else:
                try:
                    ccontact = int(contactentry.get())
                    try:
                        copbal = int(openingbalentry.get())
                        mydb = mysql.connector.connect(host='localhost',
                                                       password='',
                                                       user='root',
                                                       database='bank',
                                                       charset='utf8')
                        mycur = mydb.cursor()
                        q = "insert into applicant (apname, apadd, city, contact, bdate, gender, nomini, balance) values('" + cname + "', '" + cadd + "', '" + ccity + "', '" + str(
                            ccontact) + "', '" + cbdate + "', '" + cgender + "', '" + cnomini + "', '" + str(
                            copbal) + "')"
                        mycur.execute(q)
                        mydb.commit()
                        if mycur.rowcount != 0:
                            mycur.execute("select max(apno) from applicant")
                            result = mycur.fetchone()
                            mycur.execute("select balance from applicant where apno="+str(result[0]))
                            result2 = mycur.fetchone()
                            messagebox.showinfo("Done", "Account Created Successfully\nYour Account No = "+str(result[0])+"\nOpening Balance = "+str(result2[0]))
                            createaccountwindow.destroy()
                        else:
                            messagebox.showerror("Unable to create account", "Something Went Wrong !!!")

                    except ValueError:
                        messagebox.showinfo("Invalid", "Invalid Opening Balance")
                        openingbalentry.delete(0, END)
                except ValueError:
                    messagebox.showinfo("Invalid", "Invalid Contact Number")
                    contactentry.delete(0, END)

        createaccountwindow = Toplevel(win2)
        createaccountwindow.title("Create New Account")
        createaccountwindow.geometry("600x500+475+150")
        createaccountwindow.resizable(False, False)
        v1 = IntVar()

        namelabel = Label(createaccountwindow, text="Account Holder's Name", font=f1)
        namelabel.place(x=50, y=20)
        nameentry = Entry(createaccountwindow, font=f1)
        nameentry.place(x=300, y=20)

        addlabel = Label(createaccountwindow, text="Permanant Address", font=f1)
        addlabel.place(x=85, y=70)
        addentry = Entry(createaccountwindow, font=f1)
        addentry.place(x=300, y=70)

        citylabel = Label(createaccountwindow, text="City", font=f1)
        citylabel.place(x=232, y=120)
        cityentry = Entry(createaccountwindow, font=f1)
        cityentry.place(x=300, y=120)

        contactlabel = Label(createaccountwindow, text="Contact", font=f1)
        contactlabel.place(x=195, y=170)
        contactentry = Entry(createaccountwindow, font=f1)
        contactentry.place(x=300, y=170)

        bdatelabel = Label(createaccountwindow, text="Date of Birth", font=f1)
        bdatelabel.place(x=150, y=220)
        bdateentry = DateEntry(createaccountwindow, font=f2, date_pattern='dd-mm-yyyy', setmode='day')
        bdateentry.place(x=300, y=223)

        genderlabel = Label(createaccountwindow, text="Gender", font=f1)
        genderlabel.place(x=200, y=270)
        m = Radiobutton(createaccountwindow, text='Male', font=('calibre', 13, 'bold'), variable=v1, value=0)
        m.place(x=300, y=270)
        f = Radiobutton(createaccountwindow, text='Female', font=('calibre', 13, 'bold'), variable=v1, value=1)
        f.place(x=375, y=270)
        o = Radiobutton(createaccountwindow, text='Other', font=('calibre', 13, 'bold'), variable=v1, value=2)
        o.place(x=470, y=270)

        nominilabel = Label(createaccountwindow, text="Nomini", font=f1)
        nominilabel.place(x=205, y=320)
        nominientry = Entry(createaccountwindow, font=f1)
        nominientry.place(x=300, y=320)

        openingballabel = Label(createaccountwindow, text="Opening Balance", font=f1)
        openingballabel.place(x=110, y=370)
        openingbalentry = Entry(createaccountwindow, font=f1)
        openingbalentry.place(x=300, y=370)

        submitbutton = Button(createaccountwindow, font=f1, text='Submit', command=submitinfo)
        submitbutton.place(x=250, y=420)

        # Make the Save As dialog modal (disable main window)
        createaccountwindow.transient(win2)
        createaccountwindow.grab_set()
        win2.wait_window(createaccountwindow)  # Wait for the dialog to be closed before continuing
        createaccountwindow.mainloop()

    @staticmethod
    def show_add_new_admin_window(win2):
        def on_click_create():
            uname = ent1.get()
            pwd = ent2.get()
            cpwd = ent3.get()

            if uname == '' or uname == ' ':
                messagebox.showerror("Empty Field", "Please Provide Username")
            elif pwd == '' or pwd == ' ':
                messagebox.showerror('Empty Field', 'Please Provide Password')
            elif cpwd == '' or cpwd == ' ':
                messagebox.showerror('Empty Field', 'Please Confirm the Password')
            elif pwd != cpwd:
                messagebox.showerror('Invalid', "Original and Confirmed Password Do Not Match")
            elif (" " in pwd) or (" " in cpwd) or (" " in uname):
                messagebox.showerror("Invalid", "Blank spaces are not allowed")
            else:
                mydb = mysql.connector.connect(host='localhost',
                                               password='',
                                               user='root',
                                               charset='utf8',
                                               database='bank')

                mycur = mydb.cursor()
                q = "select * from admin where loginid='" + uname + "'"
                mycur.execute(q)
                mycur.fetchall()
                if mycur.rowcount == 0:
                    q = "insert into admin (loginid, password) values('" + uname + "', '" + cpwd + "')"
                    mycur.execute(q)
                    mydb.commit()
                    messagebox.showinfo("Done", "New Admin Account Created Successfully")
                    addnewadminwindow.destroy()
                else:
                    messagebox.showerror("Try Another One", "Login Id Already Exists")

        addnewadminwindow = Toplevel(win2)
        addnewadminwindow.title("Create New Admin Account")
        addnewadminwindow.geometry("650x330+475+150")
        addnewadminwindow.resizable(False, False)

        lab1 = Label(addnewadminwindow, text="Set Username", font=f1)
        lab2 = Label(addnewadminwindow, text="Set Password", font=f1)
        lab3 = Label(addnewadminwindow, text="Comfirm Password", font=f1)
        ent1 = Entry(addnewadminwindow, font=f1)
        ent2 = Entry(addnewadminwindow, font=f1)
        ent3 = Entry(addnewadminwindow, font=f1)

        lab1.place(x=150, y=50)
        ent1.place(x=300, y=50)
        lab2.place(x=150, y=100)
        ent2.place(x=300, y=100)
        lab3.place(x=100, y=150)
        ent3.place(x=300, y=150)

        changebutton = Button(addnewadminwindow, font=f1, text="Create", command=on_click_create)
        changebutton.place(x=290, y=200)

        # Make the Save As dialog modal (disable main window)
        addnewadminwindow.transient(win2)
        addnewadminwindow.grab_set()
        win2.wait_window(addnewadminwindow)  # Wait for the dialog to be closed before continuing
        addnewadminwindow.mainloop()

    @staticmethod
    def show_change_admin_pass_window(win2, loginid):
        def on_click_confirm():
            old = oldpassentry.get()
            new = newpassentry.get()
            confirm = confirmpassentry.get()

            if old == '':
                messagebox.showerror("Empty Field", "Please Provide Old Password")
            elif new == '':
                messagebox.showerror("Empty Field", "Please Provide New Password")
            elif confirm == '':
                messagebox.showerror("Empty Field", "Please Confirm the Password")
            elif confirm != new:
                messagebox.showerror("Invalid", "Confirm Password Do Not Match to New Password")
            else:
                mydb = mysql.connector.connect(host='localhost',
                                               password='',
                                               user='root',
                                               database='bank',
                                               charset='utf8')

                mycur = mydb.cursor()
                query = "select * from admin where password='" + old + "' and loginid='" + loginid + "'"
                mycur.execute(query)
                mycur.fetchone()
                if mycur.rowcount == 0:
                    messagebox.showerror("Invalid", "Invalid old password !!!")
                else:
                    query = "update admin set password='" + confirm + "' where loginid='" + loginid + "' and password='" + old + "'"
                    mycur.execute(query)
                    mydb.commit()
                    if mycur.rowcount == 0:
                        messagebox.showerror("Something went wrong",
                                             "Unable To Change Password, Please Try Another Password")
                    else:
                        messagebox.showinfo("Done", "Password Changed Successfully")
                        changeadminpasswindow.destroy()

        changeadminpasswindow = Toplevel(win2)
        changeadminpasswindow.title("Change Admin Password")
        changeadminpasswindow.geometry("650x330+475+150")
        changeadminpasswindow.resizable(False, False)

        # Create and Place All the Labels
        oldpasslabel = Label(changeadminpasswindow, text="Enter Old Password", font=f1)
        oldpasslabel.place(x=100, y=50)
        newpasslabel = Label(changeadminpasswindow, text="Enter New Password", font=f1)
        newpasslabel.place(x=100, y=120)
        confirmpasslabel = Label(changeadminpasswindow, text="Confirm Password", font=f1)
        confirmpasslabel.place(x=100, y=190)

        # Create and Place All the Entries
        oldpassentry = Entry(changeadminpasswindow, font=f1)
        oldpassentry.place(x=350, y=50)
        newpassentry = Entry(changeadminpasswindow, font=f1)
        newpassentry.place(x=350, y=120)
        confirmpassentry = Entry(changeadminpasswindow, font=f1)
        confirmpassentry.place(x=350, y=190)

        changebutton = Button(changeadminpasswindow, font=f1, text="Confirm", command=on_click_confirm)
        changebutton.place(x=290, y=250)

        # Make the Save As dialog modal (disable main window)
        changeadminpasswindow.transient(win2)
        changeadminpasswindow.grab_set()
        win2.wait_window(changeadminpasswindow)  # Wait for the dialog to be closed before continuing
        changeadminpasswindow.mainloop()

    @staticmethod
    def loginfun(e1, e2, win):
        loginid = e1.get()
        pswd = e2.get()
        if loginid == "":
            messagebox.showerror("Empty Field", "Please provide Login Id")
        elif pswd == "":
            messagebox.showerror("Empty Field", "Please provide Password")
        else:
            mydb = mysql.connector.connect(host='localhost',
                                           password='',
                                           user='root',
                                           database='bank',
                                           charset='utf8')
            mycur = mydb.cursor()
            mycur.execute("select loginid from admin where loginid='" + loginid + "' and password='" + pswd + "'")
            mycur.fetchone()
            if mycur.rowcount != 0:
                messagebox.showinfo("Welcome", "Login Successfully !!!")
                # To Reset the mycur
                mycur.reset()
                # Function call
                win.destroy()
                BankWindows.showloginwindow(loginid)
            else:
                messagebox.showerror("Invalid", "Invalid Login ID or Password")

    @staticmethod
    def showloginwindow(loginid):
        def on_closing():
            if messagebox.askyesnocancel('Confirm Logout', 'Are you sure you want to close and logout of the system?'):
                win2.destroy()
                BankWindows.showmainwindow()

        win2 = Tk()
        win2.title('Logged In successfully')
        win2.geometry("750x500+400+150")
        win2.resizable(False, False)

        mb = Menu(win2)
        menu1 = Menu(mb, tearoff=0)
        menu1.add_command(label='Create New Admin Account', command=lambda: BankWindows.show_add_new_admin_window(win2))
        menu1.add_separator()
        menu1.add_command(label='Change Admin Password',
                          command=lambda: BankWindows.show_change_admin_pass_window(win2, loginid))

        mb.add_cascade(menu=menu1, label="Admin")
        mb.add_command(label='Logout', command=on_closing)

        win2.config(menu=mb)
        original_image1 = Image.open(os.getcwd() + "\\images\\new_acc_img.png")
        resized_image1 = original_image1.resize((150, 150))
        render1 = ImageTk.PhotoImage(resized_image1)
        button1 = Button(win2, image=render1, text="New Account", bd=0, cursor='hand2',
                         command=lambda: BankWindows.show_create_account_window(win2))
        button1.place(x=80, y=60)
        label1 = Label(win2, text="New User Account", font=f2)
        label1.place(x=90, y=220)

        original_image2 = Image.open(os.getcwd() + "\\images\\deposit_img.png")
        resized_image2 = original_image2.resize((150, 150))
        render2 = ImageTk.PhotoImage(resized_image2)
        button2 = Button(win2, image=render2, text="Deposit", bd=0, cursor='hand2',
                         command=lambda: BankWindows.show_deposit_window(win2))
        button2.place(x=300, y=60)
        label2 = Label(win2, text="Deposite", font=f2)
        label2.place(x=350, y=220)

        original_image3 = Image.open(os.getcwd() + "\\images\\withdrawl_img.png")
        resized_image3 = original_image3.resize((150, 150))
        render3 = ImageTk.PhotoImage(resized_image3)
        button3 = Button(win2, image=render3, text="Withdrawl", bd=0, cursor='hand2',
                         command=lambda: BankWindows.show_withdrawl_amount_window(win2))
        button3.place(x=520, y=60)
        label3 = Label(win2, text="Withdrawl", font=f2)
        label3.place(x=580, y=220)

        original_image4 = Image.open(os.getcwd() + "\\images\\change_acc_details_img.png")
        resized_image4 = original_image4.resize((150, 150))
        render4 = ImageTk.PhotoImage(resized_image4)
        button4 = Button(win2, image=render4, text="Change Account Details", bd=0, cursor='hand2',
                         command=lambda: BankWindows.show_change_account_details_window(win2))
        button4.place(x=90, y=280)
        label4 = Label(win2, text="Change Account Details", font=f2)
        label4.place(x=90, y=435)

        original_image6 = Image.open(os.getcwd() + "\\images\\search_img.png")
        resized_image6 = original_image6.resize((150, 150))
        render6 = ImageTk.PhotoImage(resized_image6)
        button6 = Button(win2, image=render6, text="Serach Account", bd=0, cursor='hand2',
                         command=lambda: BankWindows.show_search_account_details_window(win2))
        button6.place(x=300, y=280)
        label6 = Label(win2, text="Search Account Details", font=f2)
        label6.place(x=310, y=435)

        original_image5 = Image.open(os.getcwd() + "\\images\\close_acc_img.png")
        resized_image5 = original_image5.resize((150, 150))
        render5 = ImageTk.PhotoImage(resized_image5)
        button5 = Button(win2, image=render5, text="Close Account", bd=0, cursor='hand2',
                         command=lambda: BankWindows.show_close_account_window(win2))
        button5.place(x=550, y=280)
        label5 = Label(win2, text="Close Account", font=f2)
        label5.place(x=570, y=435)

        win2.protocol('WM_DELETE_WINDOW', on_closing)
        win2.mainloop()

    @staticmethod
    def showmainwindow():
        win = Tk()
        win.title("Login")
        win.geometry("700x350+400+150")
        win.resizable(False, False)

        original_image = Image.open(os.getcwd() + "\\images\\user.png")
        resized_image = original_image.resize((200, 200))
        render = ImageTk.PhotoImage(resized_image)
        img = Label(win, image=render)
        img.place(x=100, y=50)

        l1 = Label(win, text="Login ID", font=f1)
        l1.place(x=400, y=50)
        e1 = Entry(win, font=f1)
        e1.place(x=400, y=90)

        l2 = Label(win, text="Password", font=f1)
        l2.place(x=400, y=140)
        e2 = Entry(win, font=f1, show='*')
        e2.place(x=400, y=180)

        toggle = Button(win, text="Show", font=f2, command=lambda: BankWindows.togglefun(e2,
                                                                                         toggle))  # Lambda is used to disable autocalling of function with passing arguments to it
        toggle.place(x=630, y=180)

        login = Button(win, text="Login", font=f2, command=lambda: BankWindows.loginfun(e1, e2, win))
        login.place(x=500, y=230)

        win.mainloop()

    @staticmethod
    def togglefun(e2, toggle):
        if e2.cget('show') == '':
            e2.config(show='*')
            toggle.config(text='Show')
        else:
            e2.config(show='')
            toggle.config(text='Hide')

