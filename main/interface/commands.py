# -*- coding: utf-8 -*-
"""
Created in 2016-2017

Author : Edouard Cuvelier
Affiliation : Université catholique de Louvain - ICTEAM - UCL Crypto Group
Address : Place du Levant 3, 1348 Louvain-la-Neuve, BELGIUM
email : firstname.lastname@uclouvain.be
"""
from tkinter import *
from tkinter import filedialog, messagebox
import os
import project_window
import pickle
import mainframe as mf
import time

def getname(s):
    """
    return the substring k of a string s of the form '*/k'
    """
    k = ''
    for i in range(len(s)-1,-1,-1):
        c = s[i]
        if c == '/':
            return k
        else :
            k = c + k
    return k


################### MENU INTERFACE ################################

def new_project(root,nb,currentProjects):
    project_window.create_project_window(root,nb,currentProjects)
    
def save_project(nb,currentProjects):
    
    tabname = nb.select()
    projectDic = currentProjects[tabname]

    filename = filedialog.asksaveasfilename(initialfile=projectDic['name'],defaultextension='.closest')
    if not filename == '' and not filename == ():
        f = open(filename,'wb')
        pickle.dump(projectDic,f)
        f.close()
   
def open_project(nb,currentProjects):
    filename = filedialog.askopenfilename()
    if not filename == '' and not filename == ():
        f = open(filename,'rb')
        projectDic = pickle.load(f)
        f.close()
        print(projectDic)
        newframe = mf.create_mainframe(nb,currentProjects,projectDic)
        #print(newframe)
        currentProjects[str(newframe)] = projectDic
        nb.add(newframe, text=projectDic['name'])
    
def modify_project(*args):
    messagebox.showinfo(message='Not Implemented Yet')
    pass

def about(root):
    print(root.winfo_width(), root.winfo_height())
    messagebox.showinfo(message='Not Implemented Yet')
    pass

def help_func(*args):
    messagebox.showinfo(message='Not Implemented Yet')
    pass


################### MAINFRAME ################################

def quick_save_project(projectDic,console):
    filename = projectDic['filename']
    f = open(filename,'wb')
    pickle.dump(projectDic,f)
    f.close()
    WriteConsole(console,getname(filename)+' saved on '+time.ctime())
    

def closetab(notebook,tab):
    r = messagebox.askyesno(message='Are you sure you want to close the project?',icon='question', title='Close Project')
    if r :
        notebook.forget(tab)
        
        
######### EXPLO FRAME ############

def convertsize(t):
    total_size = t
    if total_size > 10**3 :
        if total_size > 10**6 :
            if total_size > 10**9 :
                t = total_size/(10**8)
                tt = float.__trunc__(t)
                ttt = tt/10
                st = str(ttt)+' GB'
            else :
                t = total_size/(10**5)
                tt = float.__trunc__(t)
                ttt = tt/10
                st = str(ttt)+' MB'
        else :
            t = total_size/(10**2)
            tt = float.__trunc__(t)
            ttt = tt/10
            st = str(ttt)+' KB'
    else:
        st = str(total_size)+' B'
    return st

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def addfile(tree,frameid,currentProjects):
    s =  filedialog.askopenfilename()
    if not s == '' and not s == ():
        fname = getname(s)
        tree.insert('', 'end',s, text=fname)
        size = convertsize(os.path.getsize(s))
        tree.set(s,0,size)
        tree.set(s,1,'not shared')
        tree.set(s,4,s)
        currentProjects[frameid]['fileDic'][s] = {'filename':fname,'size':size,'status':'not shared','shadate':'','expdate':'','planned':False}

def adddir(tree,frameid,currentProjects):
    s =  filedialog.askdirectory()
    if not s == '' and not s == ():
        fname = '/'+getname(s)
        size = convertsize(get_size(s))
        tree.insert('', 'end',s, text=fname)
        tree.set(s,0,size)
        tree.set(s,1,'not shared')
        tree.set(s,4,s)
        currentProjects[frameid]['fileDic'][s] = {'filename':fname,'size':size,'status':'not shared','shadate':'','expdate':'','planned':False}

def share(tree,frameid,currentProjects,console):
    errorList = []
    for item in tree.selection() :
        currentStatus = currentProjects[frameid]['fileDic'][item]['status']
        if currentStatus == 'not shared' or currentStatus == 'to share' :
            currentProjects[frameid]['fileDic'][item]['status']= 'to share'
            tree.set(item,1,'to share')
        else :
            errorList.append((currentProjects[frameid]['fileDic'][item]['filename'],currentStatus))
            
    for error in errorList :
        fname,cstatus = error
        errorMessage = 'ERROR : Status of file '+fname+' not updated to <<to share>> because its current status is :"'+cstatus+'" (only not shared file/dir could be shared)'
        WriteConsole(console,errorMessage)


def recover(tree,frameid,currentProjects,console):
    errorList = []
    for item in tree.selection() :
        currentStatus = currentProjects[frameid]['fileDic'][item]['status']
        if currentStatus == 'shared' or currentStatus == 'to recover' :
            currentProjects[frameid]['fileDic'][item]['status']= 'to recover'
            tree.set(item,1,'to recover')
        else :
            errorList.append((currentProjects[frameid]['fileDic'][item]['filename'],currentStatus))
            
    for error in errorList :
        fname,cstatus = error
        errorMessage = 'ERROR : Status of '+fname+' not updated to "to recover" because its current status is :"'+cstatus+'" (only shared file/dir could be recovered)'
        WriteConsole(console,errorMessage)
        
def restore(tree,frameid,currentProjects,console):
    for item in tree.selection() :
        currentStatus = currentProjects[frameid]['fileDic'][item]['status']
        if currentStatus == 'to share' :
            currentProjects[frameid]['fileDic'][item]['status']= 'not shared'
            tree.set(item,1,'not shared')
        elif currentStatus == 'to delete' or currentStatus == 'to recover' :
            currentProjects[frameid]['fileDic'][item]['status']= 'shared'
            tree.set(item,1,'shared')
        else :
            pass
        
def plan_actions(actiontree,frameid,currentProjects):
    d = currentProjects[frameid]['fileDic']
    for item in d:
        itemStatus = d[item]['status']
        itemPlanned = d[item]['planned']
        if not itemPlanned :
            if itemStatus == 'to share' :
                actiontree.insert('', 'end',item, text='share '+d[item]['filename'])
            elif itemStatus == 'to recover' :
                actiontree.insert('', 'end',item, text='recover '+d[item]['filename'])
            elif itemStatus == 'to remove' :
                actiontree.insert('', 'end',item, text='remove '+d[item]['filename'])
            d[item]['planned'] = True
            
    

def remove(tree,actiontree,frameid,currentProjects,console):
    for item in tree.selection() :
        currentStatus = currentProjects[frameid]['fileDic'][item]['status']
        if currentStatus == 'shared' or currentStatus == 'to recover' or currentStatus == 'to remove':
            currentProjects[frameid]['fileDic'][item]['status']= 'to remove'
            tree.set(item,1,'to remove')
        else :
            fname = currentProjects[frameid]['fileDic'][item]['filename']
            if not actiontree.exists(item):
                currentProjects[frameid]['fileDic'].pop(item)
                tree.delete(item)
                WriteConsole(console,fname+' removed')
            else :
                WriteConsole(console,fname+' not removed (cancel action first)')
        

def updateb(*args):
    messagebox.showinfo(message='Not Implemented Yet')
    pass

######### LOCA FRAME ############

def check(*args):
    messagebox.showinfo(message='Not Implemented Yet')
    pass

def checkall(*args):
    messagebox.showinfo(message='Not Implemented Yet')
    pass

######### TASKS FRAME ############

def cancel_tasks(actiontree,frameid,currentProjects,console):
    for item in actiontree.selection() :
        fname = currentProjects[frameid]['fileDic'][item]['filename']
        currentProjects[frameid]['fileDic'][item]['planned'] = False
        actiontree.delete(item)
        WriteConsole(console,'Action on '+fname+' canceled')


def execute_tasks(*args):
    messagebox.showinfo(message='Not Implemented Yet')
    pass

######### CONSOLE FRAME ###########

def WriteConsole(console,message):
    console.config(state=NORMAL)
    console.insert('end','\n>>> '+message)
    console.config(state=DISABLED)

        
################## PROJECT WINDOW ####################################

def save_open_project(root,win,nb,projectDic,currentProjects):
    print(projectDic)
    filename = filedialog.asksaveasfilename(initialfile=projectDic['name'],defaultextension='.closest')
    projDCopy = projectDic.copy()
    for location in projectDic['locDic']:
        if projectDic['locDic'][location]['sa'] != 'remember pwd':
            projDCopy['locDic'][location]['sa'] = ''
            
    projDCopy['filename'] = filename
        
    f = open(filename,'wb')
    pickle.dump(projDCopy,f)
    f.close()
    
    newframe = mf.create_mainframe(nb,currentProjects,projectDic)
    nb.add(newframe, text=projectDic['name'])
    currentProjects[str(newframe)] = projDCopy
    win.destroy()
    newframe.focus()
    
    root.mainloop()

def open_modify_project(nb):
    messagebox.showinfo(message='Not Implemented Yet')
    pass

def save_edited_project(nb):
    messagebox.showinfo(message='Not Implemented Yet')
    pass
        
def synch_epoch(*args):
    messagebox.showinfo(message='Not Implemented Yet')
    pass

def synch_depoch(*args):
    messagebox.showinfo(message='Not Implemented Yet')
    pass

def synch_pm(*args):
    messagebox.showinfo(message='Not Implemented Yet')
    pass

def cancel_project(root,projectwindow):
    messagebox.showinfo(message='Not Implemented Yet')
    pass
    
