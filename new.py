#!python3

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import os
from tkinter import PhotoImage
import sys
import sqlite3
import tkinter.messagebox
import datetime
from tkinter import *
from autocomp import AutocompleteCombobox as combobox
import time

BOLD_FONT = ("Helvetica", 10, "bold")
joblist=[]
current_year = datetime.datetime.now().year

# generic variable object
class VarObj():
    def __init__(self):
        self.val = ''
    def getvalue(self):
        return self.val
    def setvalue(self,value):
        self.val = value

current_job=VarObj()
jobstart_year=VarObj()
jobstart_year.setvalue(current_year)

#The main application
class DbApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("A Pro's Touch Painting, LLC")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (JobMain,):   
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(JobMain)

    def show_frame(self, frm):
        frame = self.frames[frm]
        frame.tkraise()


class DbObject():
    def __init__(self,dbtype):
        self.db=sqlite3.connect(dbtype)
        self.cursor=self.db.cursor()

# Parent window will be referred to as parent and DbApp instance will be referred to as controller 
class JobMain(ttk.Frame):

    def __init__(self,parent,controller):
        ttk.Frame.__init__(self,parent)
        self.controller=controller
        notebook = ttk.Notebook(self)
        tab1=ttk.Frame(notebook)
        tab2=ttk.Frame(notebook)
        tab3=ttk.Frame(notebook)
        tab4=ttk.Frame(notebook)
        tab5=ttk.Frame(notebook)
        tab6=ttk.Frame(notebook)
        tab7=ttk.Frame(notebook)
        notebook.add(tab1,text='load/create job')
        notebook.add(tab2,text='job details')
        notebook.add(tab3,text='view materials')
        notebook.add(tab4,text='add material')
        notebook.add(tab5,text='view labor')
        notebook.add(tab6,text='add labor')
        notebook.pack(fill='both',expand=True)

        # tab1
        t1_f1 = ttk.Frame(tab1)
        t1_f2 = ttk.Frame(tab1)
        lbl = ttk.Label(t1_f1,text='Select a job from the list OR create a new job record.').pack(padx=10,pady=10,anchor='w')
        lbl = ttk.Label(t1_f1,text='Show jobs starting in year:').pack(side='left',padx=10,pady=10)
        x=range(2016,2036)
        z=[]
        for i in x:
            z.append(str(i))
        self.jobstart_year=combobox(t1_f1,width=5,values=(z))
        self.jobstart_year.set(z[0])
        self.jobstart_year.bind("<<ComboboxSelected>>", self.jobstart_year_changed)
        y=[]       
        x=jobs_db.cursor.execute("""SELECT jobname FROM jobs WHERE startyear = ?""", (self.jobstart_year.get(),))
        for i in x:
            y.append(str(i[0]))
        y.sort()
        
        self.jobstart_year.set_completion_list(z)
        self.jobstart_year.pack(side='left',padx=10,pady=10)
        self.job_select=combobox(t1_f1, width=60, values=(y))
        self.job_select.bind("<<ComboboxSelected>>", self.current_job_changed)
        self.job_select.set_completion_list(y)
        self.job_select.focus_set()
        self.job_select.pack(side='left',padx=10,pady=10)
        btn = ttk.Button(t1_f1,text='Load')
        btn.pack(side='left',padx=10,pady=10)
        lbl= ttk.Label(t1_f2,text='Create new job record:').pack(side='left',padx=10,pady=10)
        self.newjob_entry=ttk.Entry(t1_f2,width=60)
        self.newjob_entry.pack(side='left',padx=10,pady=10)
        btn = ttk.Button(t1_f2,text='Create new',command=lambda:create_jobrecord(self.newjob_entry.get(),self.job_select,controller))
        btn.pack(side='left',padx=10,pady=10)
        #t1_f1.pack(anchor='w')
        #t1_f2.pack(anchor='w',pady=60)
        t1_f1.grid(row=1,column=1,sticky='w')
        t1_f2.grid(row=2,column=1,pady=70,sticky='w')

        # tab2
        t2_f1 = ttk.Frame(tab2)
        t2_f2 = ttk.Frame(tab2)
        t2_f3 = ttk.Frame(tab2)
        t2_f4 = ttk.Frame(tab2)
        t2_f5 = ttk.Frame(tab2)
        t2_f6 = ttk.Frame(tab2)
        t2_f7 = ttk.Frame(tab2)
        t2_f8 = ttk.Frame(tab2)
        t2_f9 = ttk.Frame(tab2)
        t2_f10 = ttk.Frame(tab2)
        lbl = ttk.Label(t2_f1, text='Job name:',font=BOLD_FONT).pack(side='left',padx=10,pady=10)
        self.jobname_box=ttk.Entry(t2_f1,width=50)
        self.jobname_box.pack(side='left',padx=5,pady=10)
        lbl = ttk.Label(t2_f1, text='Address:',font=BOLD_FONT).pack(side='left',padx=10,pady=10)
        self.address_box=ttk.Entry(t2_f1,width=60)
        self.address_box.pack(side='left',padx=5,pady=10)
        lbl = ttk.Label(t2_f2, text='Start date:',font=BOLD_FONT).pack(side='left',padx=10,pady=10)
        x=range(1,13)
        y=[]
        for i in x:
            y.append(i)
        self.startmonth_box=ttk.Combobox(t2_f2,width=3,values=(y),state='readonly')
        self.startmonth_box.pack(side='left',padx=2,pady=10)
        lbl=ttk.Label(t2_f2,text='/').pack(side='left')
        x=range(1,32)
        y=[]
        for i in x:
            y.append(i)
        self.startdate_box=ttk.Combobox(t2_f2,width=3,values=(y),state='readonly')
        self.startdate_box.pack(side='left',padx=2,pady=10)
        lbl=ttk.Label(t2_f2,text='/').pack(side='left')
        x=range(2016,2036)
        y=[]
        for i in x:
            y.append(i)
        self.startyear_box=ttk.Combobox(t2_f2,width=5,values=(y),state='readonly')
        self.startyear_box.pack(side='left',padx=2,pady=10)
        lbl = ttk.Label(t2_f2,text='    End date:',font=BOLD_FONT).pack(side='left',padx=10,pady=10)
        x=range(1,13)
        y=[]
        for i in x:
            y.append(i)
        self.endmonth_box=ttk.Combobox(t2_f2,width=3,values=(y),state='readonly')
        self.endmonth_box.pack(side='left',padx=2,pady=10)
        lbl=ttk.Label(t2_f2,text='/').pack(side='left')
        x=range(1,32)
        y=[]
        for i in x:
            y.append(i)
        self.enddate_box=ttk.Combobox(t2_f2,width=3,values=(y),state='readonly')
        self.enddate_box.pack(side='left',padx=2,pady=10)
        lbl=ttk.Label(t2_f2,text='/').pack(side='left')
        x=range(2016,2036)
        y=[]
        for i in x:
            y.append(i)
        self.endyear_box=ttk.Combobox(t2_f2,width=5,values=(y),state='readonly')
        self.endyear_box.pack(side='left',padx=2,pady=10)
        lbl=ttk.Label(t2_f3,text='Contact:',font=BOLD_FONT).pack(side='left',padx=10,pady=10)
        self.contactname_box=ttk.Entry(t2_f3,width=30)
        self.contactname_box.pack(side='left',pady=10)
        lbl = ttk.Label(t2_f3,text='  Email:',font=BOLD_FONT).pack(side='left',padx=10,pady=10)
        self.email_box=ttk.Entry(t2_f3,width=30)
        self.email_box.pack(side='left',pady=10)
        lbl = ttk.Label(t2_f3,text='  Phone:',font=BOLD_FONT).pack(side='left',padx=10,pady=10)
        self.phone_box=ttk.Entry(t2_f3,width=20)
        self.phone_box.pack(side='left',pady=10)
        lbl = ttk.Label(t2_f4,text='Original bid price:',font=BOLD_FONT).pack(side='left',padx=10,pady=10)
        lbl = ttk.Label(t2_f4,text='$').pack(side='left',padx=3,pady=10)
        self.bidprice_box=ttk.Entry(t2_f4,width=13)
        self.bidprice_box.pack(side='left',pady=10)
        lbl =ttk.Label(t2_f4,text=' '*85+'Notes:',font=BOLD_FONT).pack(side='left',anchor='s')
        lbl = ttk.Label(t2_f5,text='Amount in change orders:',font=BOLD_FONT).pack(side='left',padx=10,pady=3)
        lbl = ttk.Label(t2_f5,text='$').pack(side='left',padx=3,pady=3)
        self.coamount_box = ttk.Entry(t2_f5,width=13)
        self.coamount_box.pack(side='left',pady=3)
        self.addco_btn = ttk.Button(t2_f5,text='Edit',command=lambda: notebook.select(tab5))
        self.addco_btn.pack(side='left',padx=10,pady=3)
        self.notes_box = ScrolledText(t2_f8, width=65, height=30, wrap=WORD)
        self.notes_box.pack(side='left',pady=2,anchor='e')
        lbl=ttk.Label(t2_f6,text='Total job worth including change orders :',font=BOLD_FONT).pack(side='left',padx=10,pady=3)
        self.totalworth_label = ttk.Label(t2_f6,text='$')
        self.totalworth_label.pack(side='left')
        lbl = ttk.Label(t2_f7,text='Material cost:',font=BOLD_FONT).pack(side='left',padx=10,pady=3)
        self.materialcost_label = ttk.Label(t2_f7,text='$')
        self.materialcost_label.pack(side='left')
        btn = ttk.Button(t2_f7,text='Edit',command=lambda: notebook.select(tab4)).pack(side='left',padx=15)
        lbl = ttk.Label(t2_f9,text='Labor cost:',font=BOLD_FONT).pack(side='left',padx=10,pady=3)
        self.laborcost_label = ttk.Label(t2_f9,text='$')
        self.laborcost_label.pack(side='left')
        
        #lbl = ttk.Label(t2_f5,text='
        #t2_f1.pack(anchor='w')
        
        t2_f1.grid(row=1,column=1,columnspan=3,sticky='w')
        t2_f2.grid(row=3,column=1,columnspan=2,sticky='w')
        t2_f3.grid(row=2,column=1,columnspan=3,sticky='w')
        t2_f4.grid(row=4,column=1,columnspan=3,sticky='w')
        t2_f5.grid(row=5,column=1,sticky='w')
        t2_f6.grid(row=6,column=1,sticky='w')
        t2_f7.grid(row=7,column=1,sticky='w')
        t2_f8.grid(row=5,column=2,columnspan=2,rowspan=20,sticky='e')
        t2_f9.grid(row=8,column=1,sticky='w')

        '''
        t2_f1.pack(anchor='w')
        t2_f2.pack(anchor='w')
        t2_f3.pack(anchor='w')
        t2_f4.pack(anchor='w')
        t2_f5.pack(anchor='w')
        t2_f6.pack(anchor='w')
        t2_f7.pack(anchor='w')
        '''
        self.grid(row=1,column=1)

    def jobstart_year_changed(self,event):
        jobstart_year.setvalue(self.jobstart_year.get())
        self.job_select.set('')
        update_joblist(self.job_select)

    def current_job_changed(self,event):
        current_job.setvalue(self.job_select.get())
        self.controller.title("A Pro's Touch Painting, LLC  ("+current_job.getvalue()+")")

# create database objects to communicate with
def get_database(dbtype):
    if dbtype == 'jobs':
        return DbObject('jobs.sqlite3')

jobs_db=get_database('jobs')

# update job selection list on load/create tab
def update_joblist(joblist):
    query="""SELECT jobname FROM jobs WHERE startyear = ?"""
    x=read_db('jobs', query)
    y=[]
    for i in x:
        y.append(i[0])
    print(y)
    joblist.configure(values=y)
    joblist.set_completion_list(y)

def write_to_db(dbtype,query,dataset):
    if dbtype == 'jobs':
        jobs_db.cursor.execute(query, dataset)
        jobs_db.db.commit()

def read_db(dbtype,query):
    if dbtype == 'jobs':
        x=jobs_db.cursor.execute(query, (jobstart_year.getvalue(),))
        y=[]
        for i in x:
            y.append(i)
        y.sort
        print(y)
        return y

def check_for_job_duplicate(name):
    x=jobs_db.cursor.execute("""SELECT jobname FROM jobs""")
    for i in x:
        if i[0].lower() == name.lower():
            return True
    return False

def create_jobrecord(name,job,app):
    if len(name)>0:
        if check_for_job_duplicate(name)==True:
            print('duplicate job name')
        else:
            query=""" INSERT INTO jobs(jobname,startyear) VALUES (?,?) """
            dataset=(name,current_year)
            write_to_db('jobs',query,dataset)
            update_joblist(job)
            job.set(name)
            current_job.setvalue(name)
            app.title("A Pro's Touch Painting, LLC  ("+current_job.getvalue()+")")
            
    else:
        print('empty jobname')
            
    
root=DbApp()
root.mainloop()

        
