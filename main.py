#!python3

import tkinter as tk
from tkinter import ttk
import os
from tkinter import PhotoImage
import sys
import sqlite3
import tkinter.messagebox
import datetime
from tkinter import *
# So far this is a crappy attempt to draw a window to look how I want it to and interact with it


TITLE_FONT = ("Helvetica", 18, "bold")

joblist=[]

#The main application loop
class DbApp(tk.Tk):

    # Defines the __init__ constructor for the container window
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        
        self.frames = {}
        for F in (MainMenu, TimecardAdd, TimecardRead, JobDetailAdd, JobDetailModify, JobDetailRead, MaterialManagerAdd):   
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, c):
        frame = self.frames[c]
        frame.tkraise()
    









class MainMenu(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        controller.title("Contractors Assistant by Brian")
        
        self.button1 = ttk.Button(self, text = "Add to timecard database", width=45, command=lambda: controller.show_frame(TimecardAdd))
        self.button2 = ttk.Button(self, text = "Read from the timecard database", width=45, command=lambda: controller.show_frame(TimecardRead))
        self.button3 = ttk.Button(self, text = "Create a new job record", width=45, command=lambda: controller.show_frame(JobDetailAdd))
        self.button4 = ttk.Button(self, text = "Read from the job detail database", width=45, command=lambda: controller.show_frame(JobDetailRead))
        self.button5 = ttk.Button(self, text = "Modify/Update an existing job record", width=45, command=lambda:controller.show_frame(JobDetailModify))
        self.button6 = ttk.Button(self, text = "Add items to the Material Manager", width=45, command=lambda:controller.show_frame(MaterialManagerAdd))
    
        
        self.image = PhotoImage(file='image.gif', width=660, height=688)
        self.myimage = ttk.Label(self, image = self.image)

        self.button1.grid(column=1, row=1, rowspan=1, padx=20, pady=15, sticky="n")
        self.button2.grid(column=1, row=1, rowspan=1, padx=20, pady=15)
        self.button5.grid(column=1, row=3, padx=20, pady=15, sticky="n")
        self.button4.grid(column=1, row=3, padx=20, pady=15)
        self.button3.grid(column=1, row=2, padx=20, pady=15, sticky="s")
        self.button6.grid(column=1, row=3, sticky="s")
        frame = ttk.Frame(self, borderwidth=3, relief="sunken", width=660, height=688)
        #frame.grid(column=2, row=1, columnspan=3, rowspan=3)
        self.myimage.grid(column=2, row=1, columnspan=3, rowspan=3)
        #self.text = ttk.Label(self, text="  Welcome to the Main Menu\n  Eventually I will put a picture here. ", font = TITLE_FONT)
        #self.text.grid(column=3, row=2)

    

        
    






# Each new foreground window will be defined by a class. This class defines the window for
# adding data to the timecard. It contains all the methods needed to draw the window, collect
# all of the user input values and write them to the database
class TimecardAdd(tk.Frame):

    


    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        
        
        
        self.usedate = tk.BooleanVar()

        # I'm attempting to populate a list dynamically with .sqlite3 files that exist in the working directory. This list will be used to populate the user name combobox
        users = []

        for filename in sorted(os.listdir()):
            if filename.endswith(('.sqlite3')):
                print(filename)
                dbfiles = filename[:-8]
                users.append(dbfiles)
            





        # Define widgets
        self.namelabel = ttk.Label(self, text = "Select a user name:")
        self.jobloclbl = ttk.Label(self, text = "Enter job locations:")
        self.hourslabel = ttk.Label(self, text = "Enter hours worked:")
        self.noteslabel = ttk.Label(self, text = "Enter general notes:",)
        self.datelabel = ttk.Label(self, text = "Select the date:")
        self.daylabel = ttk.Label(self, text = "Select the day:")
        self.day = ttk.Combobox(self, values= ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"), state='disabled')
        self.name = ttk.Combobox(self, values = (users), width=30, state='readonly')
        self.jobloc = ttk.Entry(self, width=50)
        self.hours = ttk.Entry(self)
        self.notes = ttk.Entry(self, width=110)
        self.month = ttk.Combobox(self, values= (1,2,3,4,5,6,7,8,9,10,11,12), width=2, state='disabled')
        self.submit = ttk.Button(self, text="Submit", command=self.submit_clicked)
        self.date = ttk.Combobox(self, values = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31),width=2, state='disabled')
        self.year = ttk.Combobox(self, values = (2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030), width=4, state='disabled')
        self.use_os_date = ttk.Checkbutton(self, text="Check this box to use the date\nprovided by your OS", variable=self.usedate, onvalue=True, command=lambda: self.usedate_check(self.usedate, self.month, self.date, self.year, self.day))
        self.image = PhotoImage(file='image2.gif', width=975, height=525)
        self.myimage = ttk.Label(self, image = self.image)
        #self.placeholder = ttk.Frame(self, borderwidth=3, relief="sunken", width=975, height=525)
        
        #self.text = ttk.Label(self, text = " This is the Add to Timecard page where you put info\nthat you will be writing to the database.\nEventually I will put some kind of picture here. ", font = TITLE_FONT)
        self.backbutton = ttk.Button(self, text="Go Back", command=lambda: controller.show_frame(MainMenu))
        

        self.usedate.set(True)
        self.year.set(int(datetime.date.today().strftime("%Y")))

        
            
  








        #Define widget geometry
    
        #self.placeholder.grid(column=0, row=3, columnspan=6, rowspan=5, sticky="w,e", padx=2)
        self.namelabel.grid(column=0, row=0, columnspan=1, rowspan=1, sticky="w", pady=15, padx=15)
        self.jobloclbl.grid(column=0, row=1, columnspan=1, rowspan=1, sticky="w", pady=15, padx=15)
        self.noteslabel.grid(column=0, row=2, columnspan=1, rowspan=1, sticky="w", pady=15, padx=15)
        self.name.grid(column=1, row=0, columnspan=1, rowspan=1, sticky="w", pady=15, padx=15)
        self.jobloc.grid(column=1, row=1, columnspan=1, rowspan=1, sticky="w", pady=15, padx=15)
        self.notes.grid(column=1, row=2, columnspan=4, sticky="w", pady=15, padx=15)
        self.submit.grid(column=4, row=2, pady=15, sticky="e", padx=15)
        self.datelabel.grid(column=2, row=0, columnspan=1, rowspan=1, sticky="n", pady=9, padx=3)
        self.month.grid(column=3, row=0, rowspan=1, sticky="n,w", padx=19, pady=9)
        self.hourslabel.grid(column=2, row=1, columnspan=1, rowspan=1, pady=4, padx=4)
        self.hours.grid(column=3, row=1, columnspan=1, rowspan=1, pady=4, padx=4)
        self.date.grid(column=3, row=0, rowspan=1, sticky="n", padx=4, pady=9)
        self.year.grid(column=3, row=0, rowspan=1, pady=9, padx=7, sticky="n,e")
        self.daylabel.grid(column=2, row=0, columnspan=1, sticky="s")
        self.day.grid(column=3, row=0, columnspan=1, sticky="s")
        self.use_os_date.grid(column=4, row=0, columnspan=1, rowspan=1, sticky="w", pady=10, padx=10)
        #self.text.grid(column=1, row=4, columnspan=3, rowspan=2, stick="w")
        self.myimage.grid(column=0, row=3, columnspan=6, rowspan=5, sticky="w,e", padx=2)
        self.backbutton.grid(column=0, row=7, columnspan=1, rowspan=1, padx=15, pady=15, sticky="s,w")
        






    def usedate_check(self, var1, cb1, cb2, cb3, cb4):
        if (var1.get() == 1):
            cb1.configure(state="disabled")
            cb2.configure(state="disabled")
            cb3.configure(state="disabled")
            cb4.configure(state="disabled")
        else:
            cb1.configure(state="readonly")
            cb2.configure(state="readonly")
            cb3.configure(state="readonly")
            cb4.configure(state="readonly")
                                           
                                           
                                           

    # This method defines what happens when the submit button is clicked in the Add to Timecard section of the program
    def submit_clicked(self):
        usedate = self.usedate.get()

        if (usedate == 1):
            try:
                print ("use date is True")
                hours = float(self.hours.get())
                name = str.capitalize(self.name.get())
                job_location = self.jobloc.get()
                notes = self.notes.get()

                month = int(datetime.date.today().strftime("%m"))
                date = int(datetime.date.today().strftime("%d"))
                day = (datetime.date.today().strftime("%A"))
                year = int(datetime.date.today().strftime("%Y"))
                                    




                #month = int(self.month.get())
                if (self.file_exists(name) == True):
                    print ('good')
                    self.add_to_database(name, month, date, year, day, hours, job_location, notes) 
                else:
                    print ('bad')
                    tk.messagebox.showerror("No such database", " No database was found for the entered user name.\n Please enter a valid user name. ")
                       
        
            except ValueError:
                tk.messagebox.showerror("Error", " You did not enter a valid number for hours worked.")

                
        
        else:
            try:
                
                hours = float(self.hours.get())
                name = str.capitalize(self.name.get())
                job_location = self.jobloc.get()
                date = int(self.date.get())
                year = int(self.year.get())
                day = (self.day.get())
                print (usedate)

    

            #print (self.hours.get())
                notes = self.notes.get()
                month = int(self.month.get())
                if (self.file_exists(name) == True):
                    print ('good')
                    self.add_to_database(name, month, date, year, day , hours, job_location, notes) 
                else:
                    print ('bad')
                    tk.messagebox.showerror("No such database", " No database was found for the entered user name.\n Please enter a valid user name. ")
                    
        
            except ValueError:
                tk.messagebox.showerror("Error", " You did not enter a valid choice for either hours worked or month,date,year")
            

    #This method checks to see if a given database filename exists
    def file_exists(self, filename):
        dbname = filename + ".sqlite3"
        
        try:
            if os.path.isfile(dbname):
                return True
        except IOError:
            return False

    def add_to_database(self, name, month, date, year, day, hours, job_location, notes):
        db_name = name + ".sqlite3"
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        cursor.execute("""INSERT INTO timecard (month, date, year, day, hours, location, notes) VALUES (?, ?, ?, ?, ?, ?, ?)""", (month, date, year, day, str(hours), job_location, notes))
        db.commit()
        db.close()
        print("\n\n\n")
        print(" SUCCESS ")
        messagebox.showinfo(message='Time card entry was saved successfully')

    




# This class defines the window that will be used to gather information and read data from the timecard database
class TimecardRead(tk.Frame):
    

    def __init__(self, parent, controller):
        
                        
                                 
        ttk.Frame.__init__(self, parent)

        users = []

        for filename in sorted(os.listdir()):
            if filename.endswith(('sqlite3')):
                dbfiles = filename[:-8]
                users.append(dbfiles)
        
        self.namelabel = ttk.Label(self, text="Select the user name to search: ")
        self.name = ttk.Combobox(self, height = 20, values = (users), state='readonly')
        self.namelabel.grid(column=0, row=1, columnspan=1, rowspan=1, sticky="w", padx=10, pady=10)
        self.name.grid(column=1, row=1, columnspan=1, rowspan=1, sticky="w", padx=10, pady=10)
        self.startmonth = ttk.Combobox(self, values=(1,2,3,4,5,6,7,8,9,10,11,12), width=2, state='readonly')
        self.startdate = ttk.Combobox(self, values=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31), width=2, state='readonly')
        self.enddate = ttk.Combobox(self, values=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31), width=2, state='readonly')
        self.year = ttk.Combobox(self, values=(2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030), width=4, state='readonly')
        self.monthlabel = ttk.Label(self, text="Select the month to search: ")
        self.startdatelabel = ttk.Label(self, text="Select the start date to search: ")
        self.enddatelabel = ttk.Label(self, text="Select the end date to search: ")
        self.yearlabel = ttk.Label(self, text="Select the year to search: ")
        self.placeholder = tk.Text(self, width=75, height=42, state='disabled')
        self.backbutton = ttk.Button(self, text="Go Back", command=lambda: controller.show_frame(MainMenu))
        #self.submitbutton = ttk.Button(self, text="Submit", command=self.read_database())
        self.submitbutton = ttk.Button(self, text="Submit", command=lambda: self.submit_clicked())
        self.scroll = ttk.Scrollbar(self, command=self.placeholder.yview)
        self.placeholder.config(yscrollcommand=self.scroll.set)
        self.totalhourslabel = ttk.Label(self, text="Total hours for all days in the search:")
        self.totalhoursbox = tk.Text(self, width=6, height=1, state='disabled')

        #self.scroll.config(command=self.placeholder.yview)
        #self.placeholder.config(yscrollcommand=self.scroll.set)
        
        self.monthlabel.grid(column=0, row=2, columnspan=1, rowspan=1, sticky="n,w", padx=10)
        self.startmonth.grid(column=1, row=2, columnspan=1, rowspan=1, sticky="n,w", padx=10)
        self.startdatelabel.grid(column=0, row=3, columnspan=1, rowspan=1, sticky="n,w", padx=10)
        self.startdate.grid(column=1, row=3, columnspan=2, rowspan=1, sticky="n,w", padx=10)
        self.enddatelabel.grid(column=0, row=4, columnspan=1, rowspan=1, sticky="n,w", padx=10)
        self.enddate.grid(column=1, row=4, columnspan=1, rowspan=1, sticky="n,w", padx=10)
        self.yearlabel.grid(column=0, row=5, columnspan=1, rowspan=1, sticky="n,w", padx=10)
        self.year.grid(column=1, row=5, columnspan=1, rowspan=1, sticky="n,w", padx=10)
        self.placeholder.grid(column=3, row=1, columnspan=4, rowspan=18, sticky="w", padx=2, pady=5)
        self.backbutton.grid(column=0, row=18, columnspan=1, rowspan=1, padx=10, pady=10, sticky="s,w")
        self.submitbutton.grid(column=1, row=18, columnspan=1, rowspan=1, padx=10, pady=10, sticky="s,e")
        self.scroll.grid(column=7, row=1, rowspan=18, stick="ns")
        self.totalhourslabel.grid(column=0, row=11, columnspan=2, sticky="s,w", padx=10)
        self.year.set(datetime.date.today().strftime("%Y"))
        self.totalhoursbox.grid(column=1, row=11, sticky="s", padx=10)
       # scrl = Scrollbar(root, command=text.yview)
       # text.config(yscrollcommand=scrl.set)
                               
                    


    def file_exists(self, filename):
        
        dbname = filename + ".sqlite3"
        
        try:
            if os.path.isfile(dbname):
                return True
        except IOError:
            return False



    def submit_clicked(self):

        # This is how I'm checking if any of the input fields are blank before continuing. There has to be a better way but it works

        self.blank = 0
        try:
            checkforblank = [self.name.get(), self.startmonth.get(), self.startdate.get(), self.enddate.get(), self.year.get()]
            for check in checkforblank:
                
                if (check == ""):
                    print("there are blank entries")
                    self.blank += 1
        
        except ValueError:
            print("too bad")
            
        if (self.blank == 0):
            name = checkforblank[0]
            if (self.file_exists(name) == True):
                print ('good')
                
                month = checkforblank[1]
                startdate = checkforblank[2]
                enddate = checkforblank[3]
                year = checkforblank[4]
                query = "SELECT * FROM timecard WHERE year == " + year + " AND month == " + month + " AND date BETWEEN " + startdate + " AND " + enddate + " ORDER BY date ASC"
                print(name)
                print(month)
                print(startdate)
                print(enddate)
                print(self.blank)
            
                self.read_database(name, query)
            else:
                print("no database")
        else:
            print("show an error")
            
                    
                
                    
            

            
        
        
        

    def read_database(self, name, query):
        db_name = name + ".sqlite3"
        


        
        #query_range = "SELECT * FROM timecard WHERE month ==" + month_range + " and date >=" + date_range + " and date <=" + date_range2 + " order by date"
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        results_format = " \n Date: {}/{}/{}\n Day: {}\n Hours: {}\n Location: {}\n Notes: {}\n\n\n\n\n"
    

        #sql = query_range
        self.placeholder.configure(state='normal')
        self.placeholder.delete('0.0',tk.END)
        self.totalhours = []
        cursor.execute(query)
        
        print("\n\n\n\n\n############################ RESULTS START HERE ############################\n\n\n\n")
        
        for record in cursor:
            x = results_format.format( record[1], record [2], record[3], record[4], record[5], record[6], record[7] )
            print (x)
            self.placeholder.insert('end', x)
            self.totalhours.append(record[5])
        print("\n\n\n############################ RESULTS END HERE ############################")
        self.placeholder.configure(state='disabled')
        self.totalhoursbox.configure(state='normal')
        self.totalhoursbox.delete('0.0',tk.END)
        self.totalhoursbox.insert('end', sum(self.totalhours))
        self.totalhoursbox.configure(state='disabled')
        print("\n\n\n")
        print(self.totalhours)
        print (sum(self.totalhours))
        db.close()
        



               

class JobDetailAdd(tk.Frame):
    name = ""
    
    


    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        #self.updatevalue= tk.BooleanVar()
        self.joblist = []
        #db = sqlite3.connect("jobs.sqlite3")
        #cursor = db.cursor()
        #cursor.execute("SELECT * FROM jobs")


        self.namelabel = ttk.Label(self, text = "Job name:")
        self.hiredbylabel = ttk.Label(self, text = "Hired by:")
        self.startlabel = ttk.Label(self, text = "Start date:")
        self.endlabel = ttk.Label(self, text = "End date:")
        self.laborlabel = ttk.Label(self, text = "Labor cost:")
        self.materiallabel = ttk.Label(self, text = "Material cost:")
        self.noteslabel = ttk.Label(self, text = "General notes:")
        self.submit = ttk.Button(self, text ="Create", textvariable=self.name, command= self.submit_clicked)
        self.notesbox = tk.Text(self, width=40, height=20)
        self.startmonth = ttk.Combobox(self, width=2, values=(1,2,3,4,5,6,7,8,9,10,11,12), state='readonly')
        self.startday = ttk.Combobox(self, width=2, values=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31), state='readonly')
        self.startyear = ttk.Combobox(self, width=4, values=(2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030), state='readonly')
        self.endmonth = ttk.Combobox(self, width=2, values=(1,2,3,4,5,6,7,8,9,10,11,12), state='readonly')
        self.endday = ttk.Combobox(self, width=2, values=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31), state='readonly')
        self.endyear = ttk.Combobox(self, width=4, values=(2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030), state='readonly')
        self.labor = ttk.Entry(self)
        self.material = ttk.Entry(self)
        #self.name = ttk.Entry(self, width=43)
        self.hired = ttk.Entry(self, width=43)
        #self.update = ttk.Button(self, text="Update")
        #self.updatecb = ttk.Checkbutton(self, variable=self.updatevalue, onvalue=True, command=lambda: self.update_check(self.updatevalue),text=" Check this box if you want\nto update an existing database entry.")
        self.pricelabel = ttk.Label(self, text = "Bid price:")
        self.bidprice = ttk.Entry(self)
        self.ds1= ttk.Label(self, text="$")
        self.ds2= ttk.Label(self, text="$")
        self.ds3= ttk.Label(self, text="$")
        
        self.f1= ttk.Frame(self, borderwidth=3, width=100, height=120)
        self.backbutton= ttk.Button(self.f1, text="Go back", command=lambda: controller.show_frame(MainMenu))
        self.namebox= ttk.Entry(self, width=43)
        


        self.namelabel.grid(column=1, row=1, columnspan=1, padx=20, pady=20)
        self.namebox.grid(column=2, row=1, columnspan=3, padx=20, pady=20, sticky='w')
        self.hiredbylabel.grid(column=5, row=1, columnspan=1, padx=20, sticky='w')
        self.hired.grid(column=6, row=1, columnspan=3, padx=2, pady=20, sticky='w')
        self.startlabel.grid(column=1, columnspan=1, row=2, padx=20, pady=20)
        self.startmonth.grid(column=2, row=2, sticky="w", padx=22, pady=9)
        self.startday.grid(column=2, row=2, pady=9)
        self.startyear.grid(column=2, row=2, padx=11, pady=9, sticky='e')
        self.endlabel.grid(column=1, row=3, pady=20, padx=20)
        self.endmonth.grid(column=2, row=3, pady=20, padx=22, sticky='w')
        self.endday.grid(column=2, row=3, pady=9)
        self.endyear.grid(column=2, row=3, padx=11, sticky='e')
        self.laborlabel.grid(column=5, columnspan=1, row=4, padx=20, pady=20, sticky='w')
        self.labor.grid(column=6, row=4, columnspan=1, padx=3, sticky='w')
        self.materiallabel.grid(column=5, row=3, columnspan=1, padx=20, pady=20, sticky='w')
        self.material.grid(column=6, row=3,padx=3, columnspan=1, sticky='w')
        self.noteslabel.grid(column=1, row=4, columnspan=1, pady=10, padx=40, sticky='se')
        self.notesbox.grid(column=1, row=5, columnspan=3, rowspan=2, padx=22, sticky='e')
        #self.submit.grid(column=5, row=6, sticky='n')
        
        self.bidprice.grid(column=6, row=2,padx=3, columnspan=1, sticky='w')
        self.pricelabel.grid(column=5, row=2, padx=20, columnspan=1, sticky='w')
        self.ds1.grid(column=5, row=2, sticky='e')
        self.ds2.grid(column=5, row=3, sticky='e')
        self.ds3.grid(column=5, row=4, sticky='e')
        self.f1.grid(column=1, row=7, rowspan=3)
        self.backbutton.place(in_=self.f1, relx=.05, rely=.7)
        self.submit.place(in_=self.f1, relx=1.3, rely=.7)

       
  


    
            




    def gather_info(self, bidprice, materialcost, laborcost):
        #db = sqlite3.connect("jobs.sqlite3")
        #cursor = db.cursor()



        if len(bidprice) > 0:
            
                
            try:
                bidprice = float(bidprice)
                #cursor.execute("""INSERT INTO jobs(bidprice) VALUES (?)""", (bidprice,))
                #db.commit()
                
            except ValueError:
                print("bid price is not an integer")
                tk.messagebox.showerror("Error", "Bid price must be a valid number and contain no commas or spaces.")
                self.invalid_entry += 1

        else:
            pass

        if len(materialcost) > 0:
            
            
                
            try:
                materialcost = float(materialcost)
                #cursor.execute("""INSERT INTO jobs(materialcost) VALUES (?)""", (materialcost,))
                #db.commit()
            except ValueError:
                print("material cost is not an integer")
                tk.messagebox.showerror("Error", "Materialcost must be a valid number and contain no commas or spaces.")
                self.invalid_entry += 1
        else:  
            pass
        if len(laborcost) > 0:
            



            
            
                
            try:
                laborcost = float(laborcost)
                #cursor.execute("""INSERT INTO jobs(laborcost) VALUES (?)""", (laborcost,))
                #db.commit()
            except ValueError:
                print("labor cost is not an integer")
                tk.messagebox.showerror("Error", "Labor cost must be a valid number and contain no commas or spaces.")
                self.invalid_entry += 1
        else:
            pass



        

        
           
            
            
            











        

    def submit_clicked(self):
        self.invalid_entry = 0
        self.duplicatejob = 0

        #check = [self.hired.get(), self.startmonth.get(), self.startday.get(), self.startyear.get(), self.endmonth.get(), self.endday.get(), self.endyear.get(), self.bidprice.get(), self.material.get(), self.labor.get(), self.notesbox.get]
        #notblank=[]
        #db = sqlite3.connect("jobs.sqlite3")
        #cursor = db.cursor()
        
        
        name = self.namebox.get()
        hiredby = self.hired.get()
        startmonth = self.startmonth.get()
        startday = self.startday.get()
        startyear = self.startyear.get()
        endmonth = self.endmonth.get()
        endday = self.endday.get()
        endyear = self.endyear.get()
        laborcost = self.labor.get()
        materialcost = self.material.get()
        notes = self.notesbox.get("0.0", tk.END)
        notes = str.strip(notes)

        bidprice = self.bidprice.get()
        self.gather_info(bidprice, materialcost, laborcost)

        print(self.invalid_entry)
        if (self.invalid_entry == 0):
            

            print(name)
            if len(name) > 0:
                db = sqlite3.connect("jobs.sqlite3")
                cursor = db.cursor()
                cursor.execute(""" SELECT * FROM jobs """)
                for i in cursor:
                    if i[1].lower() == name.lower():
                        print("duplicate name")
                        
                        self.duplicatejob +=1
                    else:
                        pass

                if (self.duplicatejob == 0):
                    
                    cursor.execute(""" INSERT INTO jobs(jobname) VALUES (?) """, (name,))
                
                   
                    if len(hiredby) > 0:
                        cursor.execute(""" UPDATE jobs SET hiredby = ? WHERE jobname = ? """, (hiredby, name))
                    
                    else:
                        pass

                    if len(startmonth) > 0:
                        cursor.execute(""" UPDATE jobs SET startmonth = ? WHERE jobname = ? """, (startmonth, name))
                    
                    else:
                        pass

                    if len(startday) > 0:
                        cursor.execute(""" UPDATE jobs SET startday = ? WHERE jobname = ? """, (startday, name))
                    
                    else:
                        pass

                    if len(startyear) > 0:
                        cursor.execute(""" UPDATE jobs SET startyear = ? WHERE jobname = ? """, (startyear, name))
                    
                    else:
                        pass

                    if len(endmonth) > 0:
                        cursor.execute(""" UPDATE jobs SET endmonth = ? WHERE jobname = ? """, (endmonth, name))
                    
                    else:
                        pass
    
                    if len(endday) > 0:
                        cursor.execute(""" UPDATE jobs SET endday = ? WHERE jobname = ? """, (endday, name))
                    
                    else:
                        print("end day is empty")

                    if len(endyear) > 0:
                        cursor.execute(""" UPDATE jobs SET endyear = ? WHERE jobname = ? """, (endyear, name))
                    
                    else:
                        pass

                    if len(notes) > 0:
                        cursor.execute(""" UPDATE jobs SET notes = ? WHERE jobname = ? """, (notes, name))
                    
                    else:
                        print("notes is empty")
            
                    if len(bidprice) > 0:
                        cursor.execute(""" UPDATE jobs SET bidprice = ? WHERE jobname = ? """, (bidprice, name))
                    
                    else:
                        pass

                    if len(materialcost) > 0:
                        cursor.execute(""" UPDATE jobs SET materialcost = ? WHERE jobname = ? """, (materialcost, name))
                    
                    else:
                        pass
                
                    if len (laborcost) > 0:
                        cursor.execute(""" UPDATE jobs SET laborcost = ? WHERE jobname = ? """, (laborcost, name))
                    
                    else:
                        pass
                    db.commit()
                    db.close()

                    tk.messagebox.showinfo(message="The job record was created successfully")
                else:
                    tk.messagebox.showerror("Error", "A job record with that job name already exists and there can not be duplicate job names.")
                    
            
            else:
                print("name box is empty")
                tk.messagebox.showerror("Error", "You must enter a job name to create a new job record")







        


class JobDetailModify(tk.Frame):
    
    name=""
    #app=DbApp()

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.joblist = []
        self.qtylist = []
        self.qtylist.extend(range(0, 31))
        

        
        self.combo()

        self.updatevalue = tk.BooleanVar()
        self.namelabel = ttk.Label(self, text = "Job name:")
        self.hiredbylabel = ttk.Label(self, text = "Hired by:")
        self.startlabel = ttk.Label(self, text = "Start date:")
        self.endlabel = ttk.Label(self, text = "End date:")
        self.laborlabel = ttk.Label(self, text = "Labor cost:")
        self.materiallabel = ttk.Label(self, text = "Material cost:")
        self.noteslabel = ttk.Label(self, text = "General notes:")
        self.pricelabel = ttk.Label(self, text = "Bid price:")
        self.ds1= ttk.Label(self, text="$")
        self.ds2= ttk.Label(self, text="$")
        self.ds3= ttk.Label(self, text="$")
        self.hired = ttk.Entry(self, width=43)       
        self.startmonth = ttk.Combobox(self, width=2, values=(1,2,3,4,5,6,7,8,9,10,11,12), state='readonly')
        self.startday = ttk.Combobox(self, width=2, values=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31), state='readonly')
        self.startyear = ttk.Combobox(self, width=4, values=(2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030), state='readonly')
        self.endmonth = ttk.Combobox(self, width=2, values=(1,2,3,4,5,6,7,8,9,10,11,12), state='readonly')
        self.endday = ttk.Combobox(self, width=2, values=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31), state='readonly')
        self.endyear = ttk.Combobox(self, width=4, values=(2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030), state='readonly')
        self.bidprice = ttk.Entry(self)
        self.material = ttk.Entry(self)
        self.usematerial=ttk.Button(self, text="add materials", command=lambda: self.add_material())
        self.labor_button = ttk.Button(self, text="add labor cost", command=lambda: self.add_labor())
        self.labor = ttk.Entry(self)
        self.notesbox = tk.Text(self, width=44, height=20, wrap=WORD)
        self.submit = ttk.Button(self, text ="Update", textvariable=self.name, command= self.submit_clicked)
        self.button= ttk.Button(self, text="refresh list", command= lambda: self.destroy())
        self.f1= ttk.Frame(self, borderwidth=3, width=100, height=120)
        self.backbutton= ttk.Button(self.f1, text="Go back", command=lambda: controller.show_frame(MainMenu))
        
        
        self.notesbox_scroll = ttk.Scrollbar(self, command=self.notesbox.yview)
        






        self.namelabel.grid(column=1, row=1, columnspan=1, padx=2, pady=20)
        self.hiredbylabel.grid(column=5, row=1, columnspan=1, padx=20, sticky='w')
        self.startlabel.grid(column=1, columnspan=1, row=2, padx=20, pady=20)
        self.endlabel.grid(column=1, row=3, pady=20, padx=20)
        self.laborlabel.grid(column=5, columnspan=1, row=4, padx=20, pady=20, sticky='w')
        self.materiallabel.grid(column=5, row=3, columnspan=1, padx=20, pady=20, sticky='w')
        self.noteslabel.grid(column=1, row=4, columnspan=1, pady=10, padx=40, sticky='se')
        self.pricelabel.grid(column=5, row=2, padx=20, columnspan=1, sticky='w')
        


        self.hired.grid(column=6, row=1, columnspan=3, padx=2, pady=20, sticky='w')
        self.startmonth.grid(column=2, row=2, sticky="w", padx=12, pady=9)
        self.startday.grid(column=2, row=2, pady=9)
        self.startyear.grid(column=2, row=2, padx=1, pady=9, sticky='e')
        self.endmonth.grid(column=2, row=3, pady=20, padx=12, sticky='w')
        self.endday.grid(column=2, row=3, pady=9)
        self.endyear.grid(column=2, row=3, padx=1, sticky='e')
        self.bidprice.grid(column=6, row=2,padx=3, columnspan=1, sticky='w')
        self.material.grid(column=6, row=3,padx=3, columnspan=1, sticky='w')
        self.labor.grid(column=6, row=4, columnspan=1, padx=3, sticky='w')
        self.notesbox.grid(column=1, row=5, columnspan=3, rowspan=2, padx=18, sticky='e')
        self.f1.grid(column=1, row=7, rowspan=3)
        self.backbutton.place(in_=self.f1, relx=.05, rely=.7)
    
        self.submit.place(in_=self.f1, relx=1.3, rely=.7)
        self.button.grid(column=4, row=2, sticky="n")
        self.usematerial.grid(column=7, row=3)
        self.labor_button.grid(column=7, row=4)
        
        self.ds1.grid(column=5, row=2, sticky='e')
        self.ds2.grid(column=5, row=3, sticky='e')
        self.ds3.grid(column=5, row=4, sticky='e')
        
        self.notesbox_scroll.grid(column=3, row=5, rowspan=2, sticky="nse")


        self.notesbox.config(yscrollcommand=self.notesbox_scroll.set)

        
################### ADD TO MATERIAL LOG SECTION ########################################
############################################################################################
###########################################################################################################    

    

            
    def material_widgets(self):
        bold_font = ("Helvetica", 10, 'bold')
        t = self.t
        n = ttk.Notebook(t)
        tab1 = ttk.Frame(n)
        tab2 = ttk.Frame(n)
        n.add(tab1, text = "Show Add Materials")
        n.add(tab2, text = "Show All Logged Materials")
        n.pack(fill="both", expand=True)
        suplist=[]
        
        
        db = sqlite3.connect("materials.sqlite3")
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM materials""")

        for i in cursor:
            if i[1]:
                if i[1] not in suplist:
                    suplist.append(str(i[1]))
        db.close()


        def listbox_selected(event):
            
            current = self.listbox.curselection()
            current = current[0]
            current = int(current)
            activate_current = self.listbox.activate(current)
            #w = self.listbox.get(ACTIVE)
            db = sqlite3.connect("jobs.sqlite3")
            cursor = db.cursor()
            #z = self.testlist[y]
            
            #get_selection = current[0][0]
            #print(y)

            get_qty = self.testlist[current][0]
            get_item = self.testlist[current][1]
            get_supplier = self.testlist[current][2]
            get_category = self.testlist[current][3]
            get_subcategory = self.testlist[current][4]
            get_unitcost = self.testlist[current][5]
            int_unit_cost = float(get_unitcost)
            get_totalcost = int_unit_cost * get_qty
        
            self.prelabel = str(get_item) + "\nQuantity: " + str(get_qty) + "\n\n\nUnit price: $" + str("%0.2f" % get_unitcost) + "\nTotal item cost: $" + str("%0.2f" % get_totalcost) + "\n\n\nSupplier: "+ str(get_supplier) + "\nCategory: " + get_category + "\nSubcategory: " + get_subcategory
            list_font = ("Helvetica", 10)
            small_font = ("Helvetica", 9)
            self.itemdetails.configure(text=self.prelabel,font=list_font, justify='left')
            
            
            
            

            
                
        def show_material_log():
            bold_font = ("Helvetica", 10, 'bold')
            list_font = ("Helvetica", 10)
            logresults = []
            getjob = self.namebox.get()
            db = sqlite3.connect("jobs.sqlite3")
            cursor = db.cursor()

            blanklabel=ttk.Label(tab2,text='\t\t\t')
            blanklabel.grid(column=5,row=1)
            #show_logged_materials = tk.Text(tab2, height = 36, width = 75#show_logged_materials.pack(side="right")
            self.listbox = tk.Listbox(tab2, height=35,width=77,font=list_font)
            self.listbox.grid(column=6, row=1, columnspan=4, rowspan=13,sticky='e')
            self.listbox.bind("<<ListboxSelect>>", listbox_selected)
            self.modifyqtylabel = ttk.Label(tab2, font=bold_font, text="Use the box below to modify the quantity\n of the selected item. To delete an item completely\n from this job log, set the quantity to 0.")
            self.modifyqtylabel.grid(column=1, row=1, columnspan=3, padx=5, pady=5)
            newqtylabel = ttk.Label(tab2, font=list_font, text="Enter new quantity: \nSet to 0 to delete.")
            newqtylabel.grid(column=1, row=2, padx=5, pady=10)
            self.modify_qty = ttk.Entry(tab2, width=6)
            self.modify_qty.grid(column=2,row=2,padx=5, pady=10)
            self.updateqty_button = ttk.Button(tab2,text="Update qty")
            self.updateqty_button.grid(column=3,sticky='w',row=2, padx=5,pady=5)
            self.itemdetails = ttk.Label(tab2, text="")
            self.itemdetails.grid(column=0,row=5, rowspan=5, columnspan=6, padx=3, sticky='w')
            self.detailslabel = ttk.Label(tab2, font=bold_font, text="Details about selected item in the log:")
            self.detailslabel.grid(column=1, row=4, columnspan=2, sticky='w',padx=10)
            
            self.testlist = []
            #show_logged_materials.configure(state='disabled')
            cursor.execute("""SELECT * FROM jobmaterials WHERE jobname = ?""", (getjob,))
            results= "    {} / {}\n\n"
            for i in cursor:
                x = results.format(i[5], i[2])
                y = (i[6], i[5], i[2], i[3], i[4], i[7])
                print(x)
                self.testlist.append(y)
                print("\n\n\nthe test list:\n")
                #print(testlist)
                logresults.append(x)
                #show_logged_materials.insert("end", x)
                #self.listbox.insert("end","")
                self.listbox.insert("end", x)
            
            db.close()
                
        show_material_log()



        def supplier_chosen(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            catlist = []
            self.supplier1 = self.sup1.get()
            cursor.execute("""SELECT * FROM materials WHERE supplier = ?""", (self.supplier1,))
            for i in cursor:
                if i[2]:
                    if i[2] not in catlist:
                        catlist.append(str(i[2]))
            print (catlist)
           
            refresh1(catlist)
            #refresh2()

            db.close()
        def supplier_chosen2(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            catlist = []
            self.supplier2 = self.sup2.get()
            cursor.execute("""SELECT * FROM materials WHERE supplier = ?""", (self.supplier2,))
            for i in cursor:
                if i[2]:
                    if i[2] not in catlist:
                        catlist.append(str(i[2]))
            print (catlist)
           
            refresh2(catlist)
            #refresh2()

            db.close()
        def supplier_chosen3(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            catlist = []
            self.supplier3 = self.sup3.get()
            cursor.execute("""SELECT * FROM materials WHERE supplier = ?""", (self.supplier3,))
            for i in cursor:
                if i[2]:
                    if i[2] not in catlist:
                        catlist.append(str(i[2]))
            print (catlist)
           
            refresh3(catlist)
            #refresh2()

            db.close()
        def supplier_chosen4(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            catlist = []
            self.supplier4 = self.sup4.get()
            cursor.execute("""SELECT * FROM materials WHERE supplier = ?""", (self.supplier4,))
            for i in cursor:
                if i[2]:
                    if i[2] not in catlist:
                        catlist.append(str(i[2]))
            print (catlist)
           
            refresh4(catlist)
            #refresh2()

            db.close()
        def supplier_chosen5(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            catlist = []
            self.supplier5 = self.sup5.get()
            cursor.execute("""SELECT * FROM materials WHERE supplier = ?""", (self.supplier5,))
            for i in cursor:
                if i[2]:
                    if i[2] not in catlist:
                        catlist.append(str(i[2]))
            print (catlist)
           
            refresh5(catlist)
            #refresh2()

            db.close()       

        def refresh1(cat1list):
            
            self.cat1.set("")
            self.cat1.configure(values=())
            self.cat1.configure(values=(cat1list))
            self.item1.configure(values=())
            self.scat1.configure(values=())
            self.cat1.bind("<<ComboboxSelected>>", cat_refresh)
            self.scat1.set("")
            self.item1.set("")
        def refresh2(cat1list):
            
            self.cat2.set("")
            self.cat2.configure(values=())
            self.cat2.configure(values=(cat1list))
            self.item2.configure(values=())
            self.scat2.configure(values=())
            self.cat2.bind("<<ComboboxSelected>>", cat_refresh2)
            self.scat2.set("")
            self.item2.set("")
        def refresh3(cat1list):
            
            self.cat3.set("")
            self.cat3.configure(values=())
            self.cat3.configure(values=(cat1list))
            self.item3.configure(values=())
            self.scat3.configure(values=())
            self.cat3.bind("<<ComboboxSelected>>", cat_refresh3)
            self.scat3.set("")
            self.item3.set("")
        def refresh4(cat1list):
            
            self.cat4.set("")
            self.cat4.configure(values=())
            self.cat4.configure(values=(cat1list))
            self.item4.configure(values=())
            self.scat4.configure(values=())
            self.cat4.bind("<<ComboboxSelected>>", cat_refresh4)
            self.scat4.set("")
            self.item4.set("")
        def refresh5(cat1list):
            
            self.cat5.set("")
            self.cat5.configure(values=())
            self.cat5.configure(values=(cat1list))
            self.item5.configure(values=())
            self.scat5.configure(values=())
            self.cat5.bind("<<ComboboxSelected>>", cat_refresh5)
            self.scat5.set("")
            self.item5.set("")
            
        def cat_refresh(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            subcat1list = []
            self.category1 = self.cat1.get()
            print(self.category1)
            cursor.execute("""SELECT * FROM materials WHERE supplier = ? AND cat1 = ?""", (self.supplier1, self.category1,))
            for i in cursor:
                if i[3]:
                    if i[3] not in subcat1list:
                        subcat1list.append(str(i[3]))
            self.scat1.configure(values=())
            self.item1.configure(values=()) 
            self.scat1.configure(values=(subcat1list))
            self.scat1.bind("<<ComboboxSelected>>", scat_chosen)
            self.item1.set("")
            self.scat1.set("")
            db.close()
            #self.scat1 = ttk.Combobox(t, values=(subcat1list), width=25)
            #self.scat1.grid(column=4, row=1, padx=5, pady=10)

        def cat_refresh2(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            subcat2list = []
            self.category2 = self.cat2.get()
            print(self.category2)
            cursor.execute("""SELECT * FROM materials WHERE supplier = ? AND cat1 = ?""", (self.supplier2, self.category2,))
            for i in cursor:
                if i[3]:
                    if i[3] not in subcat2list:
                        subcat2list.append(str(i[3]))
            self.scat2.configure(values=())
            self.item2.configure(values=())
            self.scat2.set("")
            self.scat2.configure(values =(subcat2list))
            self.scat2.bind("<<ComboboxSelected>>", scat_chosen2)
            self.item2.set("")
            
            db.close()
            #self.scat1 = ttk.Combobox(t, values=(subcat1list), width=25)
            #self.scat1.grid(column=4, row=1, padx=5, pady=10)
        def cat_refresh3(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            subcat1list = []
            self.category3 = self.cat3.get()
            print(self.category3)
            cursor.execute("""SELECT * FROM materials WHERE supplier = ? AND cat1 = ?""", (self.supplier3, self.category3,))
            for i in cursor:
                if i[3]:
                    if i[3] not in subcat1list:
                        subcat1list.append(str(i[3]))
            self.scat3.configure(values=())
            self.item3.configure(values=()) 
            self.scat3.configure(values=(subcat1list))
            self.scat3.bind("<<ComboboxSelected>>", scat_chosen3)
            self.item3.set("")
            self.scat3.set("")
            db.close()
            #self.scat1 = ttk.Combobox(t, values=(subcat1list), width=25)
            #self.scat1.grid(column=4, row=1, padx=5, pady=10)
        def cat_refresh4(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            subcat1list = []
            self.category4 = self.cat4.get()
            print(self.category4)
            cursor.execute("""SELECT * FROM materials WHERE supplier = ? AND cat1 = ?""", (self.supplier4, self.category4,))
            for i in cursor:
                if i[3]:
                    if i[3] not in subcat1list:
                        subcat1list.append(str(i[3]))
            self.scat4.configure(values=())
            self.item4.configure(values=()) 
            self.scat4.configure(values=(subcat1list))
            self.scat4.bind("<<ComboboxSelected>>", scat_chosen4)
            self.item4.set("")
            self.scat4.set("")
            db.close()
            #self.scat1 = ttk.Combobox(t, values=(subcat1list), width=25)
            #self.scat1.grid(column=4, row=1, padx=5, pady=10)
        def cat_refresh5(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            subcat1list = []
            self.category5 = self.cat5.get()
            print(self.category5)
            cursor.execute("""SELECT * FROM materials WHERE supplier = ? AND cat1 = ?""", (self.supplier5, self.category5,))
            for i in cursor:
                if i[3]:
                    if i[3] not in subcat1list:
                        subcat1list.append(str(i[3]))
            self.scat5.configure(values=())
            self.item5.configure(values=()) 
            self.scat5.configure(values=(subcat1list))
            self.scat5.bind("<<ComboboxSelected>>", scat_chosen5)
            self.item5.set("")
            self.scat5.set("")
            db.close()
            #self.scat1 = ttk.Combobox(t, values=(subcat1list), width=25)
            #self.scat1.grid(column=4, row=1, padx=5, pady=10)
        def scat_chosen(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            items1list = []
            self.subcategory1 = self.scat1.get()
            cursor.execute("""SELECT * FROM materials WHERE supplier = ? AND cat1 = ? AND cat2 = ?""", (self.supplier1, self.category1, self.subcategory1,))
            for i in cursor:
                if i[4]:
                    if i[4] not in items1list:
                        items1list.append(str(i[4]))
            self.item1.configure(values=(items1list))
            db.close()
        def scat_chosen2(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            items1list = []
            self.subcategory2 = self.scat2.get()
            cursor.execute("""SELECT * FROM materials WHERE supplier = ? AND cat1 = ? AND cat2 = ?""", (self.supplier2, self.category2, self.subcategory2,))
            for i in cursor:
                if i[4]:
                    if i[4] not in items1list:
                        items1list.append(str(i[4]))
            self.item2.configure(values=(items1list))
            db.close()
        def scat_chosen3(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            items1list = []
            self.subcategory3 = self.scat3.get()
            cursor.execute("""SELECT * FROM materials WHERE supplier = ? AND cat1 = ? AND cat2 = ?""", (self.supplier3, self.category3, self.subcategory3,))
            for i in cursor:
                if i[4]:
                    if i[4] not in items1list:
                        items1list.append(str(i[4]))
            self.item3.configure(values=(items1list))
            db.close()
        def scat_chosen4(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            items1list = []
            self.subcategory4 = self.scat4.get()
            cursor.execute("""SELECT * FROM materials WHERE supplier = ? AND cat1 = ? AND cat2 = ?""", (self.supplier4, self.category4, self.subcategory4,))
            for i in cursor:
                if i[4]:
                    if i[4] not in items1list:
                        items1list.append(str(i[4]))
            self.item4.configure(values=(items1list))
            db.close()
        def scat_chosen5(event):
            db = sqlite3.connect("materials.sqlite3")
            cursor = db.cursor()
            items1list = []
            self.subcategory5 = self.scat5.get()
            cursor.execute("""SELECT * FROM materials WHERE supplier = ? AND cat1 = ? AND cat2 = ?""", (self.supplier5, self.category5, self.subcategory5,))
            for i in cursor:
                if i[4]:
                    if i[4] not in items1list:
                        items1list.append(str(i[4]))
            self.item5.configure(values=(items1list))
            db.close()



########################################################## THIS IS WHERE I LOG THE MATERIALS INTO THE DATABASE#####################################################################################
                            


        def log_material_info(checkitem1,checkitem2,checkitem3,checkitem4,checkitem5,checkqty1,checkqty2,checkqty3,checkqty4,checkqty5):

            useCustom1 = self.customprice1.get()
            useCustom2 = self.customprice2.get()
            useCustom3 = self.customprice3.get()
            useCustom4 = self.customprice4.get()
            useCustom5 = self.customprice5.get()

            useCustom1 = str.strip(useCustom1)
            useCustom2 = str.strip(useCustom2)
            useCustom3 = str.strip(useCustom3)
            useCustom4 = str.strip(useCustom4)
            useCustom5 = str.strip(useCustom5)
            self.isCustom = []

            
            def verify_custom(ver1,ver2,ver3,ver4,ver5):

                self.customVerify1 = ""
                self.customVerify2 = ""
                self.customVerify3 = ""
                self.customVerify4 = ""
                self.customVerify5 = ""
                
                throwError = 0
                if len(ver1) > 0:
                    try:
                        strip1 = str.strip(ver1)
                        
                        self.customVerify1 = float(strip1)
                        self.isCustom.append(1)
                        
                        print("good custom price1")
                    except ValueError:
                        throwError += 1
                        print("bad custom price 1")

                if len(ver2) > 0:
                    try:
                        strip2 = str.strip(ver2)
                        self.customVerify2 = float(strip2)
                        self.isCustom.append(2)
                        print("good custom price2")
                    except ValueError:
                        throwError += 1
                        print("bad custom price 2")

                if len(ver3) > 0:
                    try:
                        strip3 = str.strip(ver3)
                        
                        self.customVerify3 = float(strip3)
                        self.isCustom.append(3)
                        print("good custom price3")
                    except ValueError:
                        throwError += 1
                        print("bad custom price 3")

                if len(ver4) > 0:
                    try:
                        strip4 = str.strip(ver4)
                        self.customVerify4 = float(strip4)
                        self.isCustom.append(4)
                        print("good custom price4")
                    except ValueError:
                        throwError += 1
                        print("bad custom price 4 ")

                if len(ver5) > 0:
                    try:
                        strip5 = str.strip(ver5)
                        self.customVerify5 = float(strip5)
                        self.isCustom.append(5)
                        print("good custom price 5")
                    except ValueError:
                        throwError += 1
                        print("bad custom price 5 ")
                if throwError > 0:
                    return True
                else:
                    return False

            if verify_custom(useCustom1,useCustom2,useCustom3,useCustom4,useCustom5) == True:
                tk.messagebox.showerror("Error"," You have entered a custom price for one or more items that is not a valid number.")
            else:
                log_material_info2(checkitem1,checkitem2,checkitem3,checkitem4,checkitem5,checkqty1,checkqty2,checkqty3,checkqty4,checkqty5)

        def log_material_info2(checkitem1,checkitem2,checkitem3,checkitem4,checkitem5,checkqty1,checkqty2,checkqty3,checkqty4,checkqty5):
            
            
                        


            name = self.namebox.get()
           
            totalcost=[]
          
            print(name)
            if (len(checkitem1) > 0):

                
              
                if (checkqty1 > 0):
                    items = []
                    jobs = []
                    qty = []
                    qty.append(checkqty1)
                    supplier1 = self.sup1.get()
                    category1 = self.cat1.get()
                    subcategory1 = self.scat1.get()
                    item1 = checkitem1
                    
                    if 1 in self.isCustom:
                        itemcost1 = checkqty1 * self.customVerify1
                        unitcost1 = self.customVerify1
                    else:
                        
                        db = sqlite3.connect("materials.sqlite3")
                        cursor = db.cursor()
                        cursor.execute(""" SELECT cost FROM materials WHERE supplier = ? AND cat1 = ? AND cat2 =? AND item = ? """, (supplier1, category1, subcategory1, item1)) 
                    
                        for i in cursor:
                            itemcost1 = checkqty1 * i[0]
                            unitcost1 = i[0]
                        db.close()

                    totalcost.append(itemcost1)
                    item1 = checkitem1 + " @ $" + "%0.2f" % unitcost1
                    

                


                
                    db = sqlite3.connect("jobs.sqlite3")
                    cursor = db.cursor()
                    cursor.execute(""" SELECT item FROM jobmaterials WHERE jobname = ? AND supplier = ? AND category = ? AND subcategory = ? """, (name, supplier1, category1, subcategory1))

                    for i in cursor:
                        items.append(i[0])

                    if item1 in items:
                        cursor.execute(""" SELECT quantity FROM jobmaterials WHERE jobname = ? AND supplier = ? AND category = ? AND subcategory = ? AND item = ? AND unitcost = ? """, (name, supplier1, category1, subcategory1, item1, unitcost1))
                        for i in cursor:
                            qty = i
                        qty = sum(qty, checkqty1)
                        
                        cursor.execute(""" UPDATE jobmaterials SET quantity = ? WHERE jobname = ? AND supplier = ? AND category = ? AND  subcategory = ? AND item = ? AND unitcost = ? """, (qty, name, supplier1, category1, subcategory1, item1, unitcost1))
                        print("found item in log already and updated quantity")
                        print(qty)
                    else:
                        qty = checkqty1
                        cursor.execute(""" INSERT INTO jobmaterials(jobname, supplier, category, subcategory, item, quantity, unitcost) VALUES(?,?,?,?,?,?,?)""", (name, supplier1, category1, subcategory1, item1, qty, unitcost1))
                        print("did not find item in log, it was created")
                    
                    db.commit()
                    db.close()
                else:
                    pass


            if (len(checkitem2) > 0):
                
                
                
                
                if (checkqty2 > 0):
                    items = []
                    jobs = []
                    qty = []
                    qty.append(checkqty2)
                    supplier2 = self.sup2.get()
                    category2 = self.cat2.get()
                    subcategory2 = self.scat2.get()
                    item2 = checkitem2

                    if 2 in self.isCustom:
                        itemcost2 = checkqty2 * self.customVerify2
                        unitcost2 = self.customVerify2
                    else:
                        db = sqlite3.connect("materials.sqlite3")
                        cursor = db.cursor()
                 
                        cursor.execute(""" SELECT cost FROM materials WHERE supplier = ? AND cat1 = ? AND cat2 =? AND item = ? """, (supplier2, category2, subcategory2, item2)) 
                        for i in cursor:
                            itemcost2 = checkqty2 * i[0]
                            unitcost2 = i[0]
                            
                        db.close()

                    totalcost.append(itemcost2)
                    item2 = checkitem2 + " @ $" + "%0.2f" % unitcost2
                    
                    db = sqlite3.connect("jobs.sqlite3")
                    cursor = db.cursor()
                    cursor.execute(""" SELECT item FROM jobmaterials WHERE jobname = ? AND supplier = ? AND category = ? AND subcategory = ? """, (name, supplier2, category2, subcategory2))
                    for i in cursor:
                        items.append(i[0])
                        
                    print("Items list: ")
                    print(items)
                    if item2 in items:
                        cursor.execute(""" SELECT quantity FROM jobmaterials WHERE jobname = ? AND supplier = ? AND category = ? AND subcategory = ? AND item = ? AND unitcost = ? """, (name, supplier1, category1, subcategory1, item1, unitcost2))
                        for i in cursor:
                            qty = i
                        qty = sum(qty, checkqty2)
                        
                        cursor.execute(""" UPDATE jobmaterials SET quantity = ? WHERE jobname = ? AND supplier = ? AND category = ? AND  subcategory = ? AND item = ? AND unitcost = ? """, (name, supplier1, category1, subcategory1, item1, unitcost2))
                        print("found item in log already and updated quantity")
                        print(qty)
                    else:
                        qty = checkqty2
                        cursor.execute(""" INSERT INTO jobmaterials(jobname, supplier, category, subcategory, item, quantity, unitcost) VALUES(?,?,?,?,?,?,?)""", (name, supplier2, category2, subcategory2, item2, qty, unitcost2))
                        print("did not find item in log, it was created")
                    
                    db.commit()
                    db.close()
                else:
                    pass


            if (len(checkitem3) > 0):
                db = sqlite3.connect("materials.sqlite3")
                cursor = db.cursor()
                
                
                    
                #quantity1 = int(self.qty1.get())
                if (checkqty3 > 0):
                
                    
                    items = []
                    jobs = []
                    qty = []
                    qty.append(checkqty3)
                    
                    supplier3 = self.sup3.get()
                    category3 = self.cat3.get()
                    subcategory3 = self.scat3.get()
                    item3 = checkitem3
                    if 3 in self.isCustom:
                        itemcost3 = checkqty3 * self.customVerify3
                        unitcost3 = self.customVerify3
                    else:
                        
                        db = sqlite3.connect("materials.sqlite3")
                        cursor = db.cursor()
                        cursor.execute(""" SELECT cost FROM materials WHERE supplier = ? AND cat1 = ? AND cat2 =? AND item = ? """, (supplier3, category3, subcategory3, item3)) 
                    
                        for i in cursor:
                            itemcost3 = checkqty3 * i[0]
                            unitcost3 = i[0]
                        db.close()

                    totalcost.append(itemcost3)
                    item3 = checkitem3 + " @ $" + "%0.2f" % unitcost3
                    db = sqlite3.connect("jobs.sqlite3")
                    cursor = db.cursor()
                    cursor.execute(""" SELECT item FROM jobmaterials WHERE jobname = ? AND supplier = ? AND category = ? AND subcategory = ? """, (name, supplier3, category3, subcategory3))
                    for i in cursor:
                        items.append(i[0])
                    print("Items list: ")
                    print(items)
                    if item3 in items:
                        cursor.execute(""" SELECT quantity FROM jobmaterials WHERE jobname = ? AND supplier = ? AND category = ? AND subcategory = ? AND item = ? AND unitcost = ? """, (name, supplier3, category3, subcategory3, item3, unitcost3))
                        for i in cursor:
                            qty = i
                        qty = sum(qty, checkqty3)
                        
                        cursor.execute(""" UPDATE jobmaterials SET quantity = ? WHERE jobname = ? AND supplier = ? AND category = ? AND  subcategory = ? AND item = ? AND unitcost = ? """, (qty, name, supplier3, category3, subcategory3, item3, unitcost3))
                        print("found item in log already and updated quantity")
                        print(qty)
                    else:
                        qty = checkqty3
                        cursor.execute(""" INSERT INTO jobmaterials(jobname, supplier, category, subcategory, item, quantity, unitcost) VALUES(?,?,?,?,?,?,?)""", (name, supplier3, category3, subcategory3, item3, qty, unitcost3))
                        print("did not find item in log, it was created")
                    
                    db.commit()
                    db.close()
                else:
                    pass


            if (len(checkitem4) > 0):
                db = sqlite3.connect("materials.sqlite3")
                cursor = db.cursor()
                
                
                    
                #quantity1 = int(self.qty1.get())
                if (checkqty4 > 0):
                
                    
                    items = []
                    jobs = []
                    qty = []
                    qty.append(checkqty4)
                    
                    supplier4 = self.sup4.get()
                    category4 = self.cat4.get()
                    subcategory4 = self.scat4.get()
                    item4 = checkitem4
                    if 4 in self.isCustom:
                        itemcost4 = checkqty4 * self.customVerify4
                        unitcost4 = self.customVerify4
                    else:
                        
                        db = sqlite3.connect("materials.sqlite3")
                        cursor = db.cursor()
                        cursor.execute(""" SELECT cost FROM materials WHERE supplier = ? AND cat1 = ? AND cat2 =? AND item = ? """, (supplier4, category4, subcategory4, item4)) 
                    
                        for i in cursor:
                            itemcost4 = checkqty4 * i[0]
                            unitcost4 = i[0]
                        db.close()

                    totalcost.append(itemcost4)
                    item4 = checkitem4 + " @ $" + "%0.2f" % unitcost4
                    db = sqlite3.connect("jobs.sqlite3")
                    cursor = db.cursor()
                    cursor.execute(""" SELECT item FROM jobmaterials WHERE jobname = ? AND supplier = ? AND category = ? AND subcategory = ? """, (name, supplier4, category4, subcategory4))
                    for i in cursor:
                        items.append(i[0])
                    print("Items list: ")
                    print(items)
                    if item4 in items:
                        cursor.execute(""" SELECT quantity FROM jobmaterials WHERE jobname = ? AND supplier = ? AND category = ? AND subcategory = ? AND item = ? AND unitcost = ? """, (name, supplier4, category4, subcategory4, item4, unitcost4))
                        for i in cursor:
                            qty = i
                        qty = sum(qty, checkqty4)
                        
                        cursor.execute(""" UPDATE jobmaterials SET quantity = ? WHERE jobname = ? AND supplier = ? AND category = ? AND  subcategory = ? AND item = ? AND unitcost = ? """, (qty, name, supplier4, category4, subcategory4, item4, unitcost4))
                        print("found item in log already and updated quantity")
                        print(qty)
                    else:
                        qty = checkqty4
                        cursor.execute(""" INSERT INTO jobmaterials(jobname, supplier, category, subcategory, item, quantity, unitcost) VALUES(?,?,?,?,?,?,?)""", (name, supplier4, category4, subcategory4, item4, qty, unitcost4))
                        print("did not find item in log, it was created")
                    
                    db.commit()
                    db.close()
                else:
                    pass


            if (len(checkitem5) > 0):
                db = sqlite3.connect("materials.sqlite3")
                cursor = db.cursor()
                
                
                    
                #quantity1 = int(self.qty1.get())
                if (checkqty5 > 0):
                
                    
                    items = []
                    jobs = []
                    qty = []
                    qty.append(checkqty5)
                    
                    supplier5 = self.sup5.get()
                    category5 = self.cat5.get()
                    subcategory5 = self.scat5.get()
                    item5 = checkitem5
                    if 5 in self.isCustom:
                        itemcost5 = checkqty5 * self.customVerify5
                        unitcost5 = self.customVerify5
                    else:
                        
                        db = sqlite3.connect("materials.sqlite3")
                        cursor = db.cursor()
                        cursor.execute(""" SELECT cost FROM materials WHERE supplier = ? AND cat1 = ? AND cat2 =? AND item = ? """, (supplier5, category5, subcategory5, item5)) 
                    
                        for i in cursor:
                            itemcost5 = checkqty5 * i[0]
                            unitcost5 = i[0]
                        db.close()

                    totalcost.append(itemcost5)
                    item5 = checkitem5 + " @ $" + "%0.2f" % unitcost5
                    db = sqlite3.connect("jobs.sqlite3")
                    cursor = db.cursor()
                    cursor.execute(""" SELECT item FROM jobmaterials WHERE jobname = ? AND supplier = ? AND category = ? AND subcategory = ? """, (name, supplier5, category5, subcategory5))
                    for i in cursor:
                        items.append(i[0])
                    print("Items list: ")
                    print(items)
                    if item5 in items:
                        cursor.execute(""" SELECT quantity FROM jobmaterials WHERE jobname = ? AND supplier = ? AND category = ? AND subcategory = ? AND item = ? AND unitcost = ? """, (name, supplier5, category5, subcategory5, item5, unitcost5))
                        for i in cursor:
                            qty = i
                        qty = sum(qty, checkqty5)
                        
                        cursor.execute(""" UPDATE jobmaterials SET quantity = ? WHERE jobname = ? AND supplier = ? AND category = ? AND  subcategory = ? AND item = ? AND unitcost = ? """, (qty, name, supplier5, category5, subcategory5, item5, unitcost5))
                        print("found item in log already and updated quantity")
                        print(qty)
                    else:
                        qty = checkqty5
                        cursor.execute(""" INSERT INTO jobmaterials(jobname, supplier, category, subcategory, item, quantity, unitcost) VALUES(?,?,?,?,?,?,?)""", (name, supplier5, category5, subcategory5, item5, qty, unitcost5))
                        print("did not find item in log, it was created")
                    
                    db.commit()
                    db.close()
                else:
                    pass
            total = sum(totalcost)
            update_material_cost(total)
            tk.messagebox.showinfo(message="Adding items to the job materials log was succesfull")
            print(total)
                



        



        def update_material_cost(total):
            name = self.namebox.get()
            db=sqlite3.connect("jobs.sqlite3")
            cursor=db.cursor()
            cursor.execute(""" SELECT materialcost FROM jobs WHERE jobname = ? """, (name,))
            for i in cursor:
                if i[0]:
                    
                    existingmaterialcost = i[0]
                else:
                    existingmaterialcost = ""
                print(existingmaterialcost)
        
            #existingmaterialcost = self.material.get()
            print("existing material cost: ")
            print(existingmaterialcost)
            
            if (existingmaterialcost != ""):
                existingmaterialcost = float(existingmaterialcost)
                
                
                grandtotal = total + existingmaterialcost
                print(grandtotal)
            else:
                grandtotal = total
                print(grandtotal)
            self.material.delete(0, tk.END)
            
            self.material.insert(0, "%0.2f" % grandtotal)
            
            
            


        def verify_log_material():

            checkitem1 = self.item1.get()
            checkitem2 = self.item2.get()
            checkitem3 = self.item3.get()
            checkitem4 = self.item4.get()
            checkitem5 = self.item5.get()
            checkqty1 = int(self.qty1.get())
            checkqty2 = int(self.qty2.get())
            checkqty3 = int(self.qty3.get())
            checkqty4 = int(self.qty4.get())
            checkqty5 = int(self.qty5.get())
            verify = 0


             ### THIS IS HOW I DECIDED TO CHECK IF AN ENTRY HAS AN ITEM SELECTED BUT NO QUANTITY. IF ANY ENTRIES DO IT WILL ADD 1 TO verify. I WILL CHECK verify LATER AND IF ITS GREATER
            ### THAN 0 I WILL ASK THE USER IF THEY WANT TO CONTINUE WITH NO QUANTITY OR CHANGE IT.
            
            if (len(checkitem1) > 0):
                if (checkqty1 == 0):
                    verify += 1
            if (len(checkitem2) > 0):
                if (checkqty2 == 0):
                    verify += 1
            if (len(checkitem3) > 0):
                if (checkqty3 == 0):
                    verify += 1
            if (len(checkitem4) > 0):
                if (checkqty4 == 0):
                    verify += 1
            if (len(checkitem5) > 0):
                if (checkqty5 == 0):
                    verify += 1
           
            
            if (verify != 0):
                

                if (tk.messagebox.askyesno("Proceed?", "There are entries that have an item selected but the quantity is set to 0.\nWould you like to proceed as it is? Items with a quantity set to 0\nwill simply be ignored.") == True):
                    print("you chose yes")
                    log_material_info(checkitem1,checkitem2,checkitem3,checkitem4,checkitem5,checkqty1,checkqty2,checkqty3,checkqty4,checkqty5)
                    #tk.messagebox.showinfo(message="Adding items to the job materials log was succesfull")
                else:
                    print("chose to not proceed")
            else:
                log_material_info(checkitem1,checkitem2,checkitem3,checkitem4,checkitem5,checkqty1,checkqty2,checkqty3,checkqty4,checkqty5)
                #tk.messagebox.showinfo(message="Adding items to the job materials log was succesfull")

                
        
        

            






        

            
            
            
                


        
        
        #t.wm_title("Add materials")
        qtylabel = ttk.Label(tab1, text="Qty:")
        suplabel = ttk.Label(tab1, text="Supplier:")
        catlabel = ttk.Label(tab1, text="Category:")
        scatlabel = ttk.Label(tab1, text="Subcategory")
        itemnamelabel = ttk.Label(tab1, text="Item name:")


        qtylabel.grid(column=1, row=0, pady=13)
        suplabel.grid(column=2, row=0, pady=13)
        catlabel.grid(column=3, row=0, pady=13)
        scatlabel.grid(column=4, row=0, pady=13)
        itemnamelabel.grid(column=5, row=0, pady=13)

        item1 = ttk.Label(tab1, text="Entry 1:")
        item2 = ttk.Label(tab1, text="Entry 2:")
        item3 = ttk.Label(tab1, text="Entry 3:")
        item4 = ttk.Label(tab1, text="Entry 4:")
        item5 = ttk.Label(tab1, text="Entry 5:")
        #item6 = ttk.Label(t, text="Item 6:")
        #item7 = ttk.Label(t, text="Item 7:")
        #item8 = ttk.Label(t, text="Item 8:")
        #item9 = ttk.Label(t, text="Item 9:")
        #item10 = ttk.Label(t, text="Item 10:")

        item1.grid(column=0, row=1, padx=10)
        item2.grid(column=0, row=2, padx=10)
        item3.grid(column=0, row=3, padx=10)
        item4.grid(column=0, row=4, padx=10)
        item5.grid(column=0, row=5, padx=10)
        #item6.grid(column=0, row=6)
        #item7.grid(column=0, row=7)
        #item8.grid(column=0, row=8)
        #item9.grid(column=0, row=9)
        #item10.grid(column=0, row=10)
        

        self.qty1 = ttk.Combobox(tab1, values=(self.qtylist), width=5)
        self.sup1 = ttk.Combobox(tab1, values=(suplist), width=25)
        self.cat1 = ttk.Combobox(tab1, width=25)
        self.scat1 = ttk.Combobox(tab1, width=25)
        self.item1 = ttk.Combobox(tab1, width=40)
        self.qty2 = ttk.Combobox(tab1, values=(self.qtylist), width=5)
        self.sup2 = ttk.Combobox(tab1, values=(suplist), width=25)
        self.cat2 = ttk.Combobox(tab1, width=25)
        self.scat2 = ttk.Combobox(tab1, width=25)
        self.item2 = ttk.Combobox(tab1, width=40)
        self.qty3 = ttk.Combobox(tab1, values=(self.qtylist), width=5)
        self.sup3 = ttk.Combobox(tab1, values=(suplist),width=25)
        self.cat3 = ttk.Combobox(tab1, width=25)
        self.scat3 = ttk.Combobox(tab1, width=25)
        self.item3 = ttk.Combobox(tab1, width=40)
        self.qty4 = ttk.Combobox(tab1, values=(self.qtylist), width=5)
        self.sup4 = ttk.Combobox(tab1, values=(suplist), width=25)
        self.cat4 = ttk.Combobox(tab1, width=25)
        self.scat4 = ttk.Combobox(tab1, width=25)
        self.item4 = ttk.Combobox(tab1, width=40)
        self.qty5 = ttk.Combobox(tab1, values=(self.qtylist), width=5)
        self.sup5 = ttk.Combobox(tab1, values=(suplist), width=25)
        self.cat5 = ttk.Combobox(tab1, width=25)
        self.scat5 = ttk.Combobox(tab1, width=25)
        self.item5 = ttk.Combobox(tab1, width=40)
        self.customprice1 = ttk.Entry(tab1, width=10)
        self.customprice2 = ttk.Entry(tab1, width=10)
        self.customprice3 = ttk.Entry(tab1, width=10)
        self.customprice4 = ttk.Entry(tab1, width=10)
        self.customprice5 = ttk.Entry(tab1, width=10)
        self.usemanualitems = ttk.Checkbutton(tab1)
        self.usemanualitemslabel = ttk.Label(tab1, font=bold_font, text="You may also use the boxes below to log items\nthat are not saved in the Materials Database.\nThis is useful to log items that are rarely or\ninfrequently purchased or for other reasons are ")
        #self.custompricelabel1 = ttk.Label(tab1, text="Custom price for Entry 1:  $\t")
        self.custompricelabel1 = ttk.Label(tab1, text="")
        self.manualqty1 = ttk.Combobox(tab1, values=(self.qtylist), width=5)
        self.manualitem1 = ttk.Entry(tab1, width=37)
        self.manualcost1 = ttk.Entry(tab1, width=8)
        self.manualqty2 = ttk.Combobox(tab1, values=(self.qtylist), width=5)
        self.manualitem2 = ttk.Entry(tab1, width=37)
        self.manualcost2 = ttk.Entry(tab1, width=8)
        self.manualqty3 = ttk.Combobox(tab1, values=(self.qtylist), width=5)
        self.manualitem3 = ttk.Entry(tab1, width=37)
        self.manualcost3 = ttk.Entry(tab1, width=8)
        self.manualqtylabel = ttk.Label(tab1,text="Qty:")
        self.manualitemlabel = ttk.Label(tab1, text="Custom item name:")
        self.manualcostlabel = ttk.Label(tab1, text="Cost:")
        
        self.custompricelabel2 = ttk.Label(tab1, text="")
        self.custompricelabel3 = ttk.Label(tab1, text="")
        self.custompricelabel4 = ttk.Label(tab1, text="")
        self.custompricelabel5 = ttk.Label(tab1, text="")


        self.usecstmcheckvar = tk.BooleanVar()

        
        self.cancel = ttk.Button(tab1, text="Cancel", command= tab2)
        #self.submit = ttk.Button(tab1, text="Submit", command = lambda: n.select(tab2))
        self.submit = ttk.Button(tab1, text="Submit", command = lambda: verify_log_material())
        self.usecstmprice = ttk.Label(tab1, font=bold_font, text="Check here if you want to enter a custom price for any of the\nitems chosen above, use the boxes below. Do this only if you\nwant to override the price saved in the Materials Database.\n ie: if the item is on sale.")
        self.usecstmcheck = ttk.Checkbutton(tab1, variable=self.usecstmcheckvar, onvalue=True, command = lambda: self.use_custom_price_check())
        self.qty1.grid(column=1, row=1, padx=5, pady=10)
        self.sup1.grid(column=2, row=1, padx=5, pady=10)
        self.cat1.grid(column=3, row=1, padx=5, pady=10)
        self.scat1.grid(column=4, row=1, padx=5, pady=10)
        self.item1.grid(column=5, row=1, padx=5, pady=10)
        self.qty2.grid(column=1, row=2, padx=5, pady=10)
        self.sup2.grid(column=2, row=2, padx=5, pady=10)
        self.cat2.grid(column=3, row=2, padx=5, pady=10)
        self.scat2.grid(column=4, row=2, padx=5, pady=10)
        self.item2.grid(column=5, row=2, padx=5, pady=10)
        self.qty3.grid(column=1, row=3, padx=5, pady=10)
        self.sup3.grid(column=2, row=3, padx=5, pady=10)
        self.cat3.grid(column=3, row=3, padx=5, pady=10)
        self.scat3.grid(column=4, row=3, padx=5, pady=10)
        self.item3.grid(column=5, row=3, padx=5, pady=10)
        self.qty4.grid(column=1, row=4, padx=5, pady=10)
        self.sup4.grid(column=2, row=4, padx=5, pady=10)
        self.cat4.grid(column=3, row=4, padx=5, pady=10)
        self.scat4.grid(column=4, row=4, padx=5, pady=10)
        self.item4.grid(column=5, row=4, padx=5, pady=10)
        self.qty5.grid(column=1, row=5, padx=5, pady=10)
        self.sup5.grid(column=2, row=5, padx=5, pady=10)
        self.cat5.grid(column=3, row=5, padx=5, pady=10)
        self.scat5.grid(column=4, row=5, padx=5, pady=10)
        self.item5.grid(column=5, row=5, padx=5, pady=10)
        #self.cancel.grid(column=0, row=7, padx=5, pady=20, sticky="w")
        self.submit.grid(column=0, row=15, padx=5, pady=20)
        self.usecstmprice.grid(column=4, columnspan=3, row=7, rowspan=3, padx=5,pady=5)
        self.custompricelabel1.grid(column=5,row=10,pady=10,sticky='w')
        self.custompricelabel2.grid(column=5,row=11,pady=10,sticky='w')
        self.custompricelabel3.grid(column=5,row=12,pady=10,sticky='w')
        self.custompricelabel4.grid(column=5,row=13,pady=10,sticky='w')
        self.custompricelabel5.grid(column=5,row=14,pady=10,sticky='w')
        self.customprice1.grid(column=5, row=10, padx=50, pady=10, sticky='e')
        self.customprice2.grid(column=5, row=11, padx=50, pady=10, sticky='e')
        self.customprice3.grid(column=5, row=12, padx=50, pady=10, sticky='e')
        self.customprice4.grid(column=5, row=13, padx=50, pady=10, sticky='e')
        self.customprice5.grid(column=5, row=14, padx=50, pady=10, sticky='e')
        #self.usemanualitems.grid(column=0, row=8,padx=5,pady=5)
        self.usemanualitemslabel.grid(column=0, row=8, columnspan=3,rowspan=2,padx=5,pady=5)
        self.manualqty1.grid(column=0, row=11,padx=7)
        self.manualitem1.grid(column=1, columnspan=2, row=11,sticky='w')
        self.manualcost1.grid(column=3, row=11,sticky='w')

        self.manualqty2.grid(column=0, row=12,padx=7)
        self.manualitem2.grid(column=1, columnspan=2, row=12,sticky='w')
        self.manualcost2.grid(column=3, row=12,sticky='w')

        self.manualqty3.grid(column=0, row=13,padx=7)
        self.manualitem3.grid(column=1, columnspan=2, row=13,sticky='w')
        self.manualcost3.grid(column=3, row=13,sticky='w')

        self.usecstmcheck.grid(column=4,row=8,sticky="w")
        
        self.manualqtylabel.grid(column=0, row=10)
        self.manualitemlabel.grid(column=1,row=10,columnspan=2)
        self.manualcostlabel.grid(column=3, row=10,sticky='w',padx=10)
        
        
        self.sup1.bind("<<ComboboxSelected>>", supplier_chosen)
        self.sup2.bind("<<ComboboxSelected>>", supplier_chosen2)
        self.sup3.bind("<<ComboboxSelected>>", supplier_chosen3)
        self.sup4.bind("<<ComboboxSelected>>", supplier_chosen4)
        self.sup5.bind("<<ComboboxSelected>>", supplier_chosen5)
        self.qty1.set(0)
        self.qty2.set(0)
        self.qty3.set(0)
        self.qty4.set(0)
        self.qty5.set(0)


        # Set the custom price entry boxes state to disabled by default.

        self.customprice1.configure(state='disabled')
        self.customprice2.configure(state='disabled')
        self.customprice3.configure(state='disabled')
        self.customprice4.configure(state='disabled')
        self.customprice5.configure(state='disabled')

    def use_custom_price_check(self):
        if self.usecstmcheckvar.get() == True:
            print("true")
            self.custompricelabel1.configure(text="Custom price for Entry 1:  $\t")

            self.custompricelabel2.configure(text="Custom price for Entry 2:  $\t")
            self.custompricelabel3.configure(text="Custom price for Entry 3:  $\t")
            self.custompricelabel4.configure(text="Custom price for Entry 4:  $\t")
            self.custompricelabel5.configure(text="Custom price for Entry 5:  $\t")
            
            self.customprice1.configure(state='enabled')
            self.customprice2.configure(state='enabled')
            self.customprice3.configure(state='enabled')
            self.customprice4.configure(state='enabled')
            self.customprice5.configure(state='enabled')
            

            '''

            self.customprice1.grid_remove()
            self.customprice2.grid_remove()
            self.customprice3.grid_remove()
            self.customprice4.grid_remove()
            self.customprice5.grid_remove()
            self.custompricelabel1.grid_remove()
            self.custompricelabel2.grid_remove()
            self.custompricelabel3.grid_remove()
            self.custompricelabel4.grid_remove()
            self.custompricelabel5.grid_remove()

            '''

            
            
        elif self.usecstmcheckvar.get() == False:
            print("false")

            self.custompricelabel1.configure(text="")
            self.custompricelabel2.configure(text="")
            self.custompricelabel3.configure(text="")
            self.custompricelabel4.configure(text="")
            self.custompricelabel5.configure(text="")
            self.customprice1.delete('0',tk.END)
            self.customprice2.delete('0',tk.END)
            self.customprice3.delete('0',tk.END)
            self.customprice4.delete('0',tk.END)
            self.customprice5.delete('0',tk.END)
            self.customprice1.configure(state='disabled')
            self.customprice2.configure(state='disabled')
            self.customprice3.configure(state='disabled')
            self.customprice4.configure(state='disabled')
            self.customprice5.configure(state='disabled')
            '''

            self.customprice1.grid()
            self.customprice2.grid()
            self.customprice3.grid()
            self.customprice4.grid()
            self.customprice5.grid()
            self.custompricelabel1.grid()
            self.custompricelabel2.grid()
            self.custompricelabel3.grid()
            self.custompricelabel4.grid()
            self.custompricelabel5.grid()
        else:
            print("error")


            '''

            
        
    def add_material(self):
        print("add material")
        #def create_window(self):
        #self.counter += 1
        self.t = tk.Toplevel(self)
    
        self.material_widgets()

    def add_labor(self):
        self.l = tk.Toplevel(self)
        self.labor_widgets()
        
        
        
                                    
    def clearallselections(self):
        self.hired.delete(0, tk.END)
        self.startmonth.set("")
        self.startday.set("")
        self.startyear.set("")
        self.endmonth.set("")
        self.endday.set("")
        self.endyear.set("")
        self.bidprice.delete(0, tk.END)
        self.material.delete(0, tk.END)
        self.labor.delete(0, tk.END)
        self.notesbox.delete("0.0", tk.END)

    def newselection(self, event):
        #self.preset_info = []
        self.clearallselections()
        self.value_of_combo = self.namebox.get()
        checkifblank = str.strip(self.value_of_combo)
        
        
        
        print(self.value_of_combo)
        
        if not(len(checkifblank) > 0):
            print("job is blank")
            self.usematerial.configure(state="disabled")
        else:
            self.usematerial.configure(state="normal")
               
               
        db=sqlite3.connect("jobs.sqlite3")
        cursor=db.cursor()
        cursor.execute("SELECT * FROM jobs WHERE jobname = ?", (self.value_of_combo,))
        for record in cursor:
            #self.preset_info.append(record[2])
            if record[2]:
                self.hired.insert(0, record[2])
            else:
                pass
            if record[3]:
                self.startmonth.set(record[3])
            else:
                pass
            if record[4]:
                self.startday.set(record[4])
            else:
                pass
            if record[5]:
                self.startyear.set(record[5])
            else:
                pass
            if record[6]:
                self.endyear.set(record[6])
            else:
                pass
            if record[7]:
                self.endmonth.set(record[7])
            else:
                pass
            if record[8]:
                self.endday.set(record[8])
            else:
                pass
            if record[9]:
                self.bidprice.insert(0, "%0.2f" % record[9])
            else:
                pass
            if record[10]:
                self.material.insert(0, "%0.2f" % record[10])
            else:
                pass
            if record[11]:
                self.labor.insert(0, "%0.2f" % record[11])
            else:
                pass
            if record[12]:
                self.notesbox.insert('end', record[12])
            else:
                pass
        db.close()

    def destroy(self):
        
        self.joblist = []
        db = sqlite3.connect("jobs.sqlite3")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM jobs")
        for record in cursor:
            self.joblist.append(str(record[1]))
        self.namebox.set("")
        self.namebox.configure(values=(self.joblist))
        #self.combo()
        self.clearallselections()
            

    def combo(self):
        self.joblist = [""]
        db = sqlite3.connect("jobs.sqlite3")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM jobs")
        for record in cursor:
            self.joblist.append(str(record[1]))
        
        self.box_value = StringVar()
        #self.namebox = ttk.Combobox(self, height=40, width=46, values=(self.joblist), state='read only')
        #self.namebox.destroy()
        self.namebox = ttk.Combobox(self, height=40, width=46, values=(self.joblist), state='read only')
        self.namebox.grid(column=2, row=1, columnspan=3, padx=2, pady=20, sticky='w')
        #self.box = ttk.Combobox(self.parent, textvariable=self.box_value)
        self.namebox.bind("<<ComboboxSelected>>", self.newselection)
    
        db.close()

    def gather_info(self, bidprice, materialcost, laborcost):
        db = sqlite3.connect("jobs.sqlite3")
        cursor = db.cursor()



        if len(bidprice) > 0:
            
            try:
                bidprice = float(bidprice)
            except ValueError:
                tk.messagebox.showerror("Error", "Bid price must be a valid number and contain no commas or spaces.")
                self.invalid_entry += 1
        else:
            pass

        if len(materialcost) > 0:
        
            try:
                materialcost = float(materialcost)
                
            except ValueError:
                tk.messagebox.showerror("Error", "Materialcost must be a valid number and contain no commas or spaces.")
                self.invalid_entry += 1
        else:  
            pass
        
        if len(laborcost) > 0:

            try:
                laborcost = float(laborcost)
                
            except ValueError:
                tk.messagebox.showerror("Error", "Labor cost must be a valid number and contain no commas or spaces.")
                self.invalid_entry += 1
        else:
            pass
        db.close()



    def submit_clicked(self):
        self.invalid_entry = 0

        check = [self.hired.get(), self.startmonth.get(), self.startday.get(), self.startyear.get(), self.endmonth.get(), self.endday.get(), self.endyear.get(), self.bidprice.get(), self.material.get(), self.labor.get(), self.notesbox.get]
        notblank=[]
        db = sqlite3.connect("jobs.sqlite3")
        cursor = db.cursor()
        
        
        name = self.namebox.get()
        hiredby = self.hired.get()
        startmonth = self.startmonth.get()
        startday = self.startday.get()
        startyear = self.startyear.get()
        endmonth = self.endmonth.get()
        endday = self.endday.get()
        endyear = self.endyear.get()
        laborcost = self.labor.get()
        materialcost = self.material.get()
        notes = self.notesbox.get("0.0", tk.END)
        notes = str.strip(notes)

        bidprice = self.bidprice.get()
        self.gather_info(bidprice, materialcost, laborcost)

        print(self.invalid_entry)

        if (self.invalid_entry == 0):
            if len(name) > 0:
                if len(hiredby) > 0:
                    cursor.execute("""UPDATE jobs SET hiredby = ? WHERE jobname = ?""", (hiredby, name))
                    #db.commit()
                else:
                    pass

                if len(startmonth) > 0:
                    cursor.execute("""UPDATE jobs SET startmonth = ? WHERE jobname = ?""", (startmonth, name))
                    #db.commit()
                else:
                    pass

                if len(startday) > 0:
                    cursor.execute("""UPDATE jobs SET startday = ? WHERE jobname =?""", (startday, name))
                    #db.commit()
                else:
                    pass

                if len(startyear) > 0:
                    cursor.execute("""UPDATE jobs SET startyear = ? WHERE jobname = ?""", (startyear, name))
                    #db.commit()
                else:
                    pass

                if len(endmonth) > 0:
                    cursor.execute("""UPDATE jobs SET endmonth = ? WHERE jobname = ?""", (endmonth, name))
                    #db.commit()
                else:
                    pass
    
                if len(endday) > 0:
                    cursor.execute("""UPDATE jobs SET endday = ? WHERE jobname = ?""", (endday,name))
                    #db.commit()
                else:
                    pass

                if len(endyear) > 0:
                    cursor.execute("""UPDATE jobs SET endyear = ? WHERE jobname = ?""", (endyear, name))
                    #db.commit()
                else:
                    pass

                if len(notes) > 0:
                    cursor.execute("""UPDATE jobs SET notes = ? WHERE jobname = ?""", (notes, name))
                    #db.commit()
                else:
                    pass
            
                if len(bidprice) > 0:
                    cursor.execute("""UPDATE jobs SET bidprice = ? WHERE jobname = ?""", (bidprice, name))
                    #db.commit()
                else:
                    pass

                if len(materialcost) > 0:
                    cursor.execute("""UPDATE jobs SET materialcost = ? WHERE jobname = ?""", (materialcost, name))
                    #db.commit()
                else:
                    pass
                
                if len (laborcost) > 0:
                    cursor.execute("""UPDATE jobs SET laborcost = ? WHERE jobname = ?""", (laborcost, name))
                    #db.commit()
                else:
                    pass

                db.commit()
                db.close()
                tk.messagebox.showinfo(message="The job record was updated successfully")

                    
            
            else:
                print("name box is empty")
                tk.messagebox.showerror("Error", "You must choose a job name from the dropdown list to modify a job record")

    def labor_widgets(self):
        n = ttk.Notebook(self.l)
        tab1 = ttk.Frame(n)
        tab2 = ttk.Frame(n)
        n.add(tab1, text = "Add Labor Cost")
        n.add(tab2, text = "Tab2")
        n.pack(fill="both", expand=True)
        self.labor_nameLabel = ttk.Label(tab1, text="Employee name:")
        self.labor_qtyLabel= ttk.Label(tab1,text="Qty:")
        self.labor_employee1 = ttk.Combobox(tab1)
        self.labor_qty1 = ttk.Combobox(tab1, width=3)

        #self.labor_qtyLabel.grid(column=0, row=0)
        self.labor_employee1.grid(column=0,row=1, padx=5, pady=7)
        self.labor_nameLabel.grid(column=0,row=0, padx=5, pady=7)
        self.labor_qtyLabel.grid(column=1, row=0, padx=5, pady=7)
        self.labor_qty1.grid(column=1, row=1, padx=5, pady=7)

class JobDetailRead(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)



        self.searchby = ttk.Checkbutton(self, text="Show by job name.")
        self.searchbydate = ttk.Checkbutton(self, text="Search date range.")
        self.startlabel = ttk.Label(self, text="start date:")
        #self.startdate= ttk.Entry(self)

        #self.startlabel.grid(column=1, row=2, padx=20, pady=10)
        #self.startdate.grid(column=2, columnspan=1, row=1, padx=20, pady=10)

        self.placeholder = tk.Text(self, width=77, height=42, state='disabled')
        self.scroll = ttk.Scrollbar(self, command=self.placeholder.yview)
        self.placeholder.config(yscrollcommand=self.scroll.set)
        self.submit = ttk.Button(self, text="Submit", command=lambda: self.read_database())
        self.backbutton = ttk.Button(self, text="Go back", command=lambda: controller.show_frame(MainMenu))   
        self.startmonth = ttk.Combobox(self, width=2, values=(1,2,3,4,5,6,7,8,9,10,11,12))
        self.startday = ttk.Combobox(self, width=2, values=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31))
        self.startyear = ttk.Combobox(self, width=4, values=(2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030))
        self.jobname = ttk.Combobox(self, width=48) 





        self.jobname.grid(column=1,columnspan=3, row=2, padx=10, sticky="n")
        self.placeholder.grid(column=4, row=1, columnspan=4, rowspan=18, sticky="w", padx=2, pady=5)
        self.scroll.grid(column=8, row=1, rowspan=18, sticky="ns")
        self.searchby.grid(column=1, row=1)
        self.submit.grid(column=1, row=6)
        self.backbutton.grid(column=2, row=9)
        self.startmonth.grid(column=1, row=3, padx=29, sticky="w")
        self.startday.grid(column=1, row=3)
        self.startyear.grid(column=1,row=3, padx=17, sticky="e")
        self.searchbydate.grid(column=1, row=2, padx=10, pady=20, sticky='s')
                                       
    def read_database(self):
        db_name = "jobs.sqlite3"
        


        
        #query_range = "SELECT * FROM timecard WHERE month ==" + month_range + " and date >=" + date_range + " and date <=" + date_range2 + " order by date"
        db = sqlite3.connect(db_name)
        cursor = db.cursor()
        results_format = " \n Job name: {}\n Hired by: {}\n Start date: {}/{}/{}\n End date: {}/{}/{}\n Bid price: {}\n Material cost: {}\n Labor cost: {}\n Notes: {}\n\n\n\n\n"
    

        #sql = query_range
        self.placeholder.configure(state='normal')
        self.placeholder.delete('0.0',tk.END)
        #self.totalhours = []
        cursor.execute("SELECT * FROM jobs")
        
        print("\n\n\n\n\n############################ RESULTS START HERE ############################\n\n\n\n")
        
        for record in cursor:
            x = results_format.format( record[1], record [2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11], record[12] )
            print (x)
            self.placeholder.insert('end', x)
            #self.totalhours.append(record[5])
        print("\n\n\n############################ RESULTS END HERE ############################")
        self.placeholder.configure(state='disabled')
        #self.totalhoursbox.configure(state='normal')
        db.close()
        #self.totalhoursbox.delete('0.0',tk.END)
        #self.totalhoursbox.insert('end', sum(self.totalhours))
        #self.totalhoursbox.configure(state='disabled')
        print("\n\n\n")
        

        

            
            

            
            
            
class MaterialManagerAdd(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        
        self.blank = ttk.Label(self, text="")
        
        
        self.suplabel = ttk.Label(self, text="Supplier:")
        self.catlabel = ttk.Label(self, text="Category:")
        self.subcatlabel = ttk.Label(self, text="Sub category:")
        self.itemlabel = ttk.Label(self, text="Item name:")
        self.costlabel = ttk.Label(self, text="Item cost:")
        self.desclabel = ttk.Label(self, text="Item description:")
        self.noteslabel = ttk.Label(self, text="Notes:")
        self.backbutton = ttk.Button(self, text="Go back", command=lambda: controller.show_frame(MainMenu))
        self.submitbutton = ttk.Button(self, text="Submit", command=lambda: self.submit_clicked())
        self.refreshbutton = ttk.Button(self, text="refresh lists", command=lambda: self.refresh_all())
        self.blank.grid(column=1,row=0)
        self.suplabel.grid(column=1, row=1, padx=40, pady=15, sticky="w")
        
        self.catlabel.grid(column=1, row=2, padx=40, pady=15, sticky="w") 
        
        self.subcatlabel.grid(column=1, row=3, padx=40, pady=15, sticky="w")
        
        self.itemlabel.grid(column=1, row=4, padx=40, pady=15, sticky="w")
        
        self.costlabel.grid(column=1, row=5, padx=40, pady=15, sticky="w")
        
        self.desclabel.grid(column=1, row=6, padx=40, pady=15, sticky="w")
        
        self.noteslabel.grid(column=1, row=10, padx=40, pady=15, sticky="w")
        

        self.backbutton.grid(column=1, row=17, padx=35, pady=17, sticky="sw")
        self.submitbutton.grid(column=2, row=17,padx=0, pady=17, sticky="sw")
        self.refreshbutton.grid(column=5, row=2)
        self.widgets()


    def widgets(self):
        self.suplist=[]
        self.catlist=[]
        self.subcatlist=[]

        db = sqlite3.connect("materials.sqlite3")
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM materials""")
        for i in cursor:
            if i[1]:
                if i[1] not in self.suplist:
                    self.suplist.append(str(i[1]))
           
            if i[2]:
                
                if i[2] not in self.catlist:
                    self.catlist.append(str(i[2]))
            if i[3]:
                if i[3] not in self.subcatlist:
                    self.subcatlist.append(str(i[3]))
        db.close()
        
            
        self.sup1 = ttk.Combobox(self, width=40, values=(self.suplist))
        self.cat1 = ttk.Combobox(self, width=40, values=(self.catlist))
        self.subcat1 = ttk.Combobox(self, width=40, values=(self.subcatlist))
        self.item1 = ttk.Entry(self, width=43)
        self.cost1 = ttk.Entry(self)
        self.desc1 = tk.Text(self, width=40, height=9)
        self.notes1 = tk.Text(self, width=40, height=9)
        self.sup1.grid(column=2, columnspan=3, row=1, padx=17, pady=15, sticky="w")
        self.cat1.grid(column=2, columnspan=3, row=2, padx=17, pady=15, sticky="w")
        self.subcat1.grid(column=2, columnspan=3, row=3, padx=17, pady=15, sticky="w")
        self.item1.grid(column=2, columnspan=3, row=4, padx=17, pady=15, sticky="w")
        self.cost1.grid(column=2, row=5, padx=17, pady=15, sticky="w")
        self.desc1.grid(column=2, row=6, columnspan=3, rowspan=4, padx=17, pady=15, sticky="w")
        self.notes1.grid(column=2, columnspan=3, row=10, rowspan=4, padx=17, pady=15)

# I NEED TO REWORK THIS SO IT DOESN'T JUST DESTROY AND REFRESH BECAUSE IT MESSES UP THE TABBING ORDER

    def refresh_all(self):
        self.sup1.destroy()
        self.cat1.destroy()
        self.subcat1.destroy()
        self.item1.destroy()
        self.cost1.destroy()
        self.desc1.destroy()
        self.notes1.destroy()
        self.widgets()
        
    def submit_clicked(self):
        self.invalidentry = 0
        supplier = self.sup1.get()
        category = self.cat1.get()
        subcategory = self.subcat1.get()
        item = self.item1.get()
        cost = self.cost1.get()
        description = self.desc1.get("0.0", tk.END)
        description = str.strip(description)
        notes = self.notes1.get("0.0", tk.END)
        notes = str.strip(notes)

        mylist=[supplier, category, item, cost, subcategory, description, notes]
        required=mylist[0:4]
        for i in required:
            if len(i) < 1:
                print("empty values")
                self.invalidentry += 1
            else:
                pass
        if self.invalidentry > 0:
            tk.messagebox.showerror("Error", "Supplier, Category, Item name and Item cost are all required fields")
        else:
            
            try:
                if (len(cost) > 0):
                    cost= float(cost)
                    self.add_to_database(supplier, category, subcategory, item, cost, description, notes)
                else:
                    pass
            except ValueError:
                tk.messagebox.showerror("Error", "Item cost must be a number and contain no commas or space.")
                    
 
        

    
        
        
    def add_to_database(self, supplier, category, subcategory, itemname, cost, description, notes):
        print("add to database")
        duplicate_entry = 0
        item = str.strip(itemname)
        db=sqlite3.connect("materials.sqlite3")
        cursor=db.cursor()
        cursor.execute("""SELECT item FROM materials WHERE supplier = ? AND cat1 = ? AND cat2 = ?""", (supplier, category, subcategory))
        for i in cursor:
            if i[0].lower() == item.lower():
                duplicate_entry += 1

        if (duplicate_entry < 1):
            
            cursor.execute("""INSERT INTO materials(supplier, cat1, item, cost) VALUES(?,?,?,?)""", (supplier, category, item, cost))
            if (len(subcategory) > 0):
                cursor.execute("""UPDATE materials SET cat2 = ? WHERE supplier = ? AND cat1 = ? AND item = ? AND cost = ?""", (subcategory, supplier, category, item, cost))
            else:
                pass
            if (len(description) > 0):
                cursor.execute("""UPDATE materials SET description = ? WHERE supplier = ? AND cat1 = ? AND item = ? AND cost = ?""", (description, supplier, category, item, cost)) 
    
            else:
                pass
            if (len(notes) > 0):
                cursor.execute("""UPDATE materials SET notes = ? WHERE supplier = ? AND cat1 = ? AND item = ? AND cost = ?""", (notes, supplier, category, item, cost))
            else:
                pass
            db.commit()
        
            tk.messagebox.showinfo(message="Item has been added to the Materials database succesfully")
        else:
            tk.messagebox.showerror("Error", "The item you are trying to add already exists in the materials database!\nThere can not be duplicate entries.")
        db.close()
        
            

        
        
                     
window = DbApp()
                                 
        
        
    

        
        
if __name__ == "__main__":
    
    window.resizable(width=False, height=False)
    window.mainloop()
