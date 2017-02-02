# -*- coding: utf-8 -*-
"""
Created in 2016-2017

Author : Edouard Cuvelier
Affiliation : Université catholique de Louvain - ICTEAM - UCL Crypto Group
Address : Place du Levant 3, 1348 Louvain-la-Neuve, BELGIUM
email : firstname.lastname@uclouvain.be
"""

from tkinter import filedialog, messagebox
import os
import project_window
import pickle
import mainframe as mf

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


def addfile(tree):
    s =  filedialog.askopenfilename()
    if not s == '' and not s == ():
        i = tree.insert('', 'end',s, text=s)
        size = convertsize(os.path.getsize(s))
        tree.set(i,0,size)
        tree.set(i,1,'not shared')
    
def open_project(nb):
    filename = filedialog.askopenfilename()
    f = open(filename,'rb')
    project = pickle.load(f)
    f.close()
    name, SSSvar, Modvar, nbSLvar, threshold, patternmasking, EP, DEP, LOC, fileList = project
    
    newframe = mf.create_mainframe(nb,project)
    nb.add(newframe, text=name)
    
def save_open_project(root,win,nb,project):
    #print(project)
    name, SSSvar, Modvar, nbSLvar, threshold, patternmasking, EP, DEP, LOC, fileList = project
    epochvar1,epochvar2 = EP
    depochvar1,depochvar2 = DEP
    filename = filedialog.asksaveasfilename(initialfile=name,defaultextension='.closest')
    f = open(filename,'wb')
    pickle.dump(project,f)
    f.close()
    
    newframe = mf.create_mainframe(nb,project)
    nb.add(newframe, text=name)
    win.destroy()
    newframe.focus()

def adddir(tree):
    s =  filedialog.askdirectory()
    if not s == '' and not s == ():
        size = convertsize(get_size(s))
        i= tree.insert('', 'end', text=s)
        tree.set(i,0,size)
        tree.set(i,1,'not shared')
    
def new_project(root,nb):
    project_window.create_project_window(root,nb)
    
def save_project(*args):
    filename = filedialog.asksaveasfilename()
    print(filename)

def quick_save_project(filename):
    print(filename)

def updateb(*args):
    pass

def closetab(notebook,tab):
    r = messagebox.askyesno(message='Are you sure you want to close the project?',icon='question', title='Close Project')
    if r :
        notebook.forget(tab)
        
def cancel_project(root,projectwindow):
    pass
        
def synch_epoch(*args):
    pass

def synch_depoch(*args):
    pass

def synch_pm(*args):
    pass
    
