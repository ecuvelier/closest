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
#from tkinter import filedialog
import interface.commands as com
#import interface.mainframe as mf
#import os




root = Tk()
root.option_add('*tearOff', FALSE)

root.title('Closest -- Cloud Secure Storage via Secret Sharing')


nb = ttk.Notebook(root)
nb.grid(column=0, row=0, sticky=(N, S, E, W))
#mainf1 = mf.create_mainframe(nb)
#nb.add(mainf1, text='Project One')

currentProjects = {} # Dictionary saving the project opened for the session #TODO: save and open project of last sessions


menubar = Menu(root)
root['menu'] = menubar
menu_project = Menu(menubar)
menu_about = Menu(menubar)
menu_help = Menu(menubar, name='help')

menubar.add_cascade(menu=menu_project, label='Project')
menubar.add_cascade(menu=menu_about, label='?')

menu_about.add_command(label='Help',command = lambda : com.help_func())
menu_about.add_command(label='About',command = lambda : com.about(root))

menu_project.add_command(label='New Project',command = lambda : com.new_project(root,nb,currentProjects))
menu_project.add_command(label='Open Project',command = lambda : com.open_project(nb,currentProjects))
menu_project.add_command(label='Save Project',command = lambda : com.save_project(nb,currentProjects))
#menu_project.add_command(label='Copy Project')
menu_project.add_separator()
menu_project.add_command(label='Modify Project',command = lambda : com.modify_project(nb,currentProjects))



root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.update()
#root.minsize(root.winfo_width(), root.winfo_height())
#print(root.winfo_width(), root.winfo_height())
root.minsize(1400, 950)
#nb.forget(mainf1)
root.mainloop()