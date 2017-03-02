# -*- coding: utf-8 -*-
"""
Created in 2016-2017

Author : Edouard Cuvelier
Affiliation : Université catholique de Louvain - ICTEAM - UCL Crypto Group
Address : Place du Levant 3, 1348 Louvain-la-Neuve, BELGIUM
email : firstname.lastname@uclouvain.be
"""

from tkinter import *
from tkinter import ttk

def create_proccessing_window(parent):
    proccesingwindow = Toplevel(parent)
    proccesingwindow.title('Executing pending tasks')
    
    mframe = ttk.Frame(proccesingwindow, padding=(3,3,12,12))
    mframe.grid(column=10,row=10, sticky=(N,S,E,W))
    
    progBar = ttk.Progressbar(mframe, orient=HORIZONTAL, length = 400, mode='indeterminate')
    progBar.grid(column=10, row=10,sticky=(W,E))
    progBar.start()
    
    proccesingwindow.update()
    proccesingwindow.minsize(proccesingwindow.winfo_width(), proccesingwindow.winfo_height())
    proccesingwindow.resizable(FALSE,FALSE)
    
    return proccesingwindow,progBar