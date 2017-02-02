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
import commands as com
import mainframe as mf
#import os




root = Tk()
root.option_add('*tearOff', FALSE)

root.title('Closest -- Cloud Secure Storage via Secret Sharing')


nb = ttk.Notebook(root)
nb.grid(column=0, row=0, sticky=(N, S, E, W))
mainf1 = mf.create_mainframe(nb)
nb.add(mainf1, text='Project One')



menubar = Menu(root)
root['menu'] = menubar
menu_project = Menu(menubar)
menu_about = Menu(menubar)
menu_help = Menu(menubar, name='help')

menubar.add_cascade(menu=menu_project, label='Project')
menubar.add_cascade(menu=menu_about, label='About')
menubar.add_cascade(menu=menu_help, label='Help')

menu_project.add_command(label='New Project',command = lambda : com.new_project(root,nb))
menu_project.add_command(label='Open Project',command = lambda : com.open_project(nb))
menu_project.add_command(label='Save Project',command = com.save_project)
#menu_project.add_command(label='Copy Project')
menu_project.add_separator()
menu_project.add_command(label='Modify Project')



root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.update()
#print((root.winfo_width(), root.winfo_height()))
root.minsize(1300, 950)
#nb.forget(mainf1)
root.mainloop()