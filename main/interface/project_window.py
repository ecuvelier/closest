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
from interface import commands as com

def create_project_window(root,nb,currentProjects):
    
    projectwindow = Toplevel(root)
    mframe = ttk.Frame(projectwindow, padding=(3,3,12,12))
    mframe.grid(column=10,row=10, sticky=(N,S,E,W))
    
    ################ MENU ########################
    
    menubar = Menu(projectwindow)
    projectwindow['menu'] = menubar
    menu_project = Menu(menubar)
    menu_synch = Menu(menubar)
    
    menubar.add_cascade(menu=menu_project, label='Project')
    menubar.add_cascade(menu=menu_synch, label='Locations')
    
    menu_project.add_command(label='Open Project',command = lambda : com.open_modify_project(nb))
    menu_project.add_command(label='Save Project',command = lambda : com.save_edited_project(nb))
    
    menu_synch.add_command(label='Synchronize Epoch',command = com.synch_epoch)
    menu_synch.add_command(label='Synchronize Delta Epoch',command = com.synch_depoch)
    menu_synch.add_separator()
    checkPMVar = StringVar()
    menu_synch.add_checkbutton(label='Always Use Pattern Masking',command = com.synch_pm, variable=checkPMVar, onvalue=1, offvalue=0)
    
    ################ PARAMETERS FRAME ########################
        
    paramframe = ttk.Labelframe(mframe, text='Parameters')
    paramframe.grid(column=10,row=10, sticky=(N,S,E,W))
    
    namelabel = ttk.Label(paramframe, text='Project Name :')
    namelabel.grid(column=10, row=10, sticky=(W, E))
    nameVar = StringVar()
    name_entry = ttk.Entry(paramframe, width=30, textvariable=nameVar)
    name_entry.grid(column=20, row=10, sticky=(W, E))
    name_entry.insert(0,'Untitled Project')
    
    SSSlabel = ttk.Label(paramframe, text='Secret Sharing Scheme :')
    SSSlabel.grid(column=10, row=20, sticky=(W, E))
    SSSVar = StringVar()
    SSScb = ttk.Combobox(paramframe, textvariable=SSSVar)
    SSScb.grid(column=20, row=20, sticky=(W, E))
    SSScb['values'] = ('Shamir', 'Blakley', 'Other')
    SSScb.configure(state='readonly')
    SSScb.current(0)
    
    Mod = ('512','1024','2048','4096','8192','16384','32768','65536')
    Modlabel = ttk.Label(paramframe, text='Module Size (Shamir) :')
    Modlabel.grid(column=10, row=30, sticky=(W, E))
    ModVar = StringVar()
    Modcb = ttk.Combobox(paramframe, textvariable=ModVar)
    Modcb.grid(column=20, row=30, sticky=(W, E))
    Modcb['values'] = Mod
    Modcb.configure(state='readonly')
    Modcb.current(0)
    
    ################ PLACES FRAME ########################
    locframe = ttk.Labelframe(mframe, text='Storage Locations')
    locframe.grid(column=10,row=20, sticky=(N,S,E,W))
    
    number_of_locations = StringVar()
    number_of_locations.set(0)
    
    locnb = ttk.Notebook(locframe)
    locnb.grid(column=10, row=20,columnspan=90, sticky=(N, S, E, W))
    
    LocationDic = {}
    
    thresholdlabel = ttk.Label(locframe, text='Threshold :')
    thresholdlabel.grid(column=20, row=10)
    thresholdVar = StringVar()
    thresholdcb = ttk.Combobox(locframe, textvariable=thresholdVar)
    thresholdcb.grid(column=30, row=10, sticky=(W, E))
    thresholdcb['values'] = ('2')
    thresholdcb.current(0)
    thresholdcb.configure(state='readonly')
    
    def closeLoctab(notebook,tab):
        #i = number_of_locations.get()
        #number_of_locations.set(int(i)-1)
        T = thresholdcb['values']
        lastv = int(T[-1])
        newT = T[0:len(T)-1]
        thresholdcb['values'] = newT
        if int(thresholdVar.get()) >= lastv :
            thresholdcb.current(len(newT)-1)
        notebook.forget(tab)
    
    def add_location(notebook,removable = True, updateThreshold=True):
        i = number_of_locations.get()
        if updateThreshold :
            T = thresholdcb['values']
            lastv = int(T[-1])
            T = T+(str(lastv+1),)
            thresholdcb['values'] = T
        
        newlocframe = ttk.Frame(notebook, padding=(3,3,12,12))
        
        if removable :
            bcloseLoc = ttk.Button(newlocframe, text="Remove Location",command= lambda : closeLoctab(notebook,newlocframe))
            bcloseLoc.grid(column=10, row=80, sticky=(W))
        
        locnamelabel = ttk.Label(newlocframe, text='Location Name :')
        locnamelabel.grid(column=10, row=10, sticky=(W, E))
        locNameVar = StringVar()
        loc_name_entry = ttk.Entry(newlocframe, width=20, textvariable=locNameVar)
        loc_name_entry.grid(column=20, row=10, sticky=(W, E))
        loc_name_entry.insert(0,'Untitled Location')
        
        locTypelabel = ttk.Label(newlocframe, text='Type :')
        locTypelabel.grid(column=10, row=15, sticky=(W, E))
        locTypeVar = StringVar()
        locTypecb = ttk.Combobox(newlocframe, textvariable=locTypeVar)
        locTypecb.grid(column=20, row=15, sticky=(W, E))
        locTypecb['values'] = ('Local','Cloud', 'FTP', 'Other')
        locTypecb.configure(state='readonly')
        locTypecb.current(1)
        
        accessCommandlabel = ttk.Label(newlocframe, text='Access Command :')
        accessCommandlabel.grid(column=10, row=20, sticky=(W, E))
        accessCommandVar = StringVar()
        accessCommand_entry = ttk.Entry(newlocframe, width=20, textvariable=accessCommandVar)
        accessCommand_entry.grid(column=20, row=20, sticky=(W, E))
        
        passwordCommandlabel = ttk.Label(newlocframe, text='Password :')
        passwordCommandlabel.grid(column=10, row=30, sticky=(W, E))
        passwordCommandVar = StringVar()
        passwordCommand_entry = ttk.Entry(newlocframe, width=20, textvariable=passwordCommandVar)
        passwordCommand_entry.grid(column=20, row=30, sticky=(W, E))
        passwordCommand_entry.configure(show='')

        saveAccess = StringVar()
        saveAccessButton = ttk.Checkbutton(newlocframe, text='Remember Password', variable=saveAccess, onvalue='remember pwd', offvalue='forget pwd')
        saveAccessButton.grid(column=20, row=40, sticky=(W, E))
        
        N = ('1','2','3','4','5','6','7','8','9','10','11')
        M = ('day(s)','week(s)','month(s)','year(s)')
        
        sublocframe = ttk.Frame(newlocframe, padding=(3,3,3,3))
        sublocframe.grid(column=20, row=50, sticky=(W, E))
        
        Epochlabel = ttk.Label(sublocframe, text='Epoch :')
        Epochlabel.grid(column=10, row=10, sticky=(W, E))
        EpochVar1 = StringVar()
        EpochCB1 = ttk.Combobox(sublocframe, textvariable=EpochVar1)
        EpochCB1.grid(column=20, row=10, sticky=(W, E))
        EpochCB1['values'] = N
        EpochCB1.configure(state='readonly')
        EpochCB1.current(2)
        
        EpochVar2 = StringVar()
        EpochCB2 = ttk.Combobox(sublocframe, textvariable=EpochVar2)
        EpochCB2.grid(column=30, row=10, sticky=(W, E))
        EpochCB2['values'] = M
        EpochCB2.configure(state='readonly')
        EpochCB2.current(2)
        
        DEpochlabel = ttk.Label(sublocframe, text='Delta of Epoch :')
        DEpochlabel.grid(column=10, row=20, sticky=(W, E))
        DEpochVar1 = StringVar()
        DEpochCB1 = ttk.Combobox(sublocframe, textvariable=DEpochVar1)
        DEpochCB1.grid(column=20, row=20, sticky=(W, E))
        DEpochCB1['values'] = N
        DEpochCB1.configure(state='readonly')
        DEpochCB1.current(1)
        
        DEpochVar2 = StringVar()
        DEpochCB2 = ttk.Combobox(sublocframe, textvariable=DEpochVar2)
        DEpochCB2.grid(column=30, row=20, sticky=(W, E))
        DEpochCB2['values'] = M
        DEpochCB2.configure(state='readonly')
        DEpochCB2.current(1)
        
        patternMasking = StringVar()
        patternMaskingButton = ttk.Checkbutton(newlocframe, text='Use Pattern Masking', variable=patternMasking, onvalue='Pattern Masking Enabled', offvalue='Pattern Masking Disabled')
        patternMaskingButton.grid(column=10, row=60, sticky=(W, E))
     
        notebook.add(newlocframe, text='Storage Location '+i)
        
        for child in newlocframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
        
        number_of_locations.set(int(i)+1)
        
        location = {'nlf':newlocframe,'name':locNameVar,'type':locTypeVar,'ac':accessCommandVar,'pwd':passwordCommandVar,'sa':saveAccess,'e1':EpochVar1,'e2':EpochVar2,'de1':DEpochVar1,'de2':DEpochVar2,'pm':patternMasking}
        LocationDic[i]=location
    
    
    
    addlocbutton = ttk.Button(locframe, text='Add Location',command=lambda : add_location(locnb))
    addlocbutton.grid(column=10, row=10, sticky=(E, W))
    
    add_location(locnb,False,False)
    add_location(locnb,False,False)
    
    
    ################ Tool FRAME ########################
    
    toolframe = ttk.Frame(mframe)
    toolframe.grid(column=10,row=30, sticky=(N,S,E,W))
    
    def get_project():
        projectDic = {}
        projectDic['name'] = nameVar.get()
        projectDic['SSS'] = SSSVar.get()
        projectDic['Mod'] = ModVar.get()
        projectDic['Nb_of_loc'] = number_of_locations.get()
        projectDic['Threshold'] = thresholdVar.get()
        locDic = {}
        for lockey in LocationDic :
            locDic[lockey] = {'name':LocationDic[lockey]['name'].get(),'type':LocationDic[lockey]['type'].get(),'ac':LocationDic[lockey]['ac'].get(),'pwd':LocationDic[lockey]['pwd'].get(),'sa':LocationDic[lockey]['sa'].get(),'e1':LocationDic[lockey]['e1'].get(),'e2':LocationDic[lockey]['e2'].get(),'de1':LocationDic[lockey]['de1'].get(),'de2':LocationDic[lockey]['de2'].get(),'pm':LocationDic[lockey]['pm'].get()}
        projectDic['locDic'] = locDic
        projectDic['fileDic'] = {}
        
        #print(projectDic)
        return projectDic
        
    
    Save_and_OpenButton = ttk.Button(toolframe, text="Save and Open",command= lambda : com.save_open_project(root,projectwindow,nb,get_project(),currentProjects))
    Save_and_OpenButton.grid(column=10, row=10)
    CancelButton = ttk.Button(toolframe, text="Cancel",command= lambda : com.cancel_project(root,projectwindow))
    CancelButton.grid(column=20, row=10)
    
    
    for frame in (mframe,paramframe,locframe,toolframe):
        for child in frame.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
            
            
    #############################################################
            
    projectwindow.update()
    projectwindow.minsize(projectwindow.winfo_width(), projectwindow.winfo_height())
    
    
    root.mainloop()