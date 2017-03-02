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


def create_mainframe(parent,currentProjects,projectDic={}):
    if projectDic == {} :
        projectDic['SSS'] = ''
        projectDic['Threshold'] = ''
        projectDic['Nb_of_loc'] = ''
        projectDic['locDic'] = {}
        projectDic['fileDic'] = {}

        
    mainframe = ttk.Frame(parent, padding=(3,3,12,12))
    mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
    
    mainframe.columnconfigure(5,weight=1)
    mainframe.columnconfigure(35,weight=1)
    
    mainframe.rowconfigure(5,weight=1)
    mainframe.rowconfigure(15,weight=1)
    mainframe.rowconfigure(25,weight=1)
    mainframe.rowconfigure(35,weight=1)
    
    
    mainframe.rowconfigure(20,weight=3)
    mainframe.columnconfigure(10,weight=3)
    mainframe.columnconfigure(20,weight=3)
    mainframe.columnconfigure(30,weight=3)
    
    mainframe.rowconfigure(30,weight=3)
    
    ################ PARAMETERS FRAME ########################
        
    paramframe = ttk.Labelframe(mainframe, text='Parameters')
    paramframe.grid(column=10,row=10, sticky=(N,S,E,W))
    
    #parameters = StringVar()
    splus = ''
    if projectDic['SSS'] == 'Shamir' :
        splus = ' with '+projectDic['Mod']+'-bit Module'
        
    sparam = projectDic['Threshold']+'-out-of-'+projectDic['Nb_of_loc']+' '+projectDic['SSS']+' Secret Sharing Scheme'+splus
    paramlabel = ttk.Label(paramframe, text=sparam)
    paramlabel.grid(column=2, row=2, sticky=(W, E))
    #parameters.set(sparam)
    
    for child in paramframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    
    ################ Tool FRAME ########################
    
    toolframe = ttk.Frame(mainframe)
    toolframe.grid(column=30,row=10, sticky=(E))
    
    bclose = ttk.Button(toolframe, text="Close ❌",command= lambda : com.closetab(parent,mainframe))
    bclose.grid(column=3, row=0)
    #bopen = ttk.Button(toolframe, text="",command = lambda : com.open_project(parent))
    #bopen.grid(column=1, row=0)
    bsave = ttk.Button(toolframe, text="Quick Save ", command = lambda : com.quick_save_project(projectDic,console))
    bsave.grid(column=2, row=0)
    
    
    for child in toolframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
        
    ################ CONSOLE FRAME ########################

    consoleframe = ttk.Labelframe(mainframe, text='Console')
    consoleframe.grid(column=30,row=30, sticky=(N,S,E,W))
    
    console = Text(consoleframe, width=50, height=20)
    console.grid(column=5,row=5,sticky = (N,S,E,W))
    #console.config(state=DISABLED)
    
    sc3 = ttk.Scrollbar(consoleframe, orient=VERTICAL, command=console.yview)
    console.configure(yscrollcommand=sc3.set)
    sc3.grid(column = 6,row = 5, sticky = (N,S))
    
    consoleframe.columnconfigure(5,weight=1)
    consoleframe.rowconfigure(5,weight=1)
    
    console.insert('1.0','>>> Welcome to Closest')
    console.config(state=DISABLED)
    
    
    for child in consoleframe.winfo_children():
        child.grid_configure(padx=5, pady=5)
    
    ################ EXPLO FRAME ########################
    
    exploframe = ttk.Labelframe(mainframe, text='Virtual Repository')
    exploframe.grid(column=10,row=20, columnspan = 21, sticky=(N,S,E,W))
    
    addrepo = ttk.Button(exploframe, text="Add a Directory ", command= lambda : com.adddir(tree,str(mainframe),currentProjects))
    addrepo.grid(column=3, row=1,sticky=W)
    
    addfile = ttk.Button(exploframe, text="Add a File ", command=lambda : com.addfile(tree,str(mainframe),currentProjects))
    addfile.grid(column=3, row=2,sticky=W)
    
    reshare = ttk.Button(exploframe, text="(Re-)Share   ", command=lambda : com.share(tree,str(mainframe),currentProjects,console))
    reshare.grid(column=3, row=3,sticky=W)
    
    recover = ttk.Button(exploframe, text="Recover   ", command=lambda : com.recover(tree,str(mainframe),currentProjects,console))
    recover.grid(column=3, row=4,sticky=W)
    
    restore = ttk.Button(exploframe, text="Restore ", command=lambda : com.restore(tree,str(mainframe),currentProjects,console))
    restore.grid(column=3, row=5,sticky=W)
    
    planactions = ttk.Button(exploframe, text="Plan Actions ", command=lambda : com.plan_actions(actiontree,str(mainframe),currentProjects))
    planactions.grid(column=5, row=8,sticky=(E,W))
    
    remove = ttk.Button(exploframe, text="Remove ", command=lambda : com.remove(tree,actiontree,str(mainframe),currentProjects,console))
    remove.grid(column=3, row=6,sticky=W)
    
    tree = ttk.Treeview(exploframe, columns = ['size','status','shared on','exp date','path'])
    tree.grid(column=5, row=1, rowspan=6, sticky=(N, W, E, S))
    
    #update = ttk.Button(exploframe, text="Reload Project File/ ",command =com.updateb)
    #update.grid(column=5, row=8,sticky=(E,W))
    
    tree.heading('#0',text = 'name')
    tree.column('#0',anchor = W,minwidth = 100, stretch = True, width = 200)
    tree.heading(0,text = 'size')
    tree.column(0,anchor = E, minwidth = 100, stretch = True, width = 100)
    tree.heading(1,text = 'status')
    tree.column(1,anchor = E,minwidth = 100, stretch = True, width = 100)
    tree.heading(2,text = 'shared on')
    tree.column(2,anchor = E,minwidth = 100, stretch = True, width = 150)
    tree.heading(3,text = 'expiration date')
    tree.column(3,anchor = E,minwidth = 120, stretch = True, width = 150)
    tree.heading(4,text = 'path')
    tree.column(4,anchor = W,minwidth = 400, stretch = True, width = 400)
    
    # Inserted at the root, program chooses id:
    d = projectDic['fileDic']
    for fileKey in d:
        fileName = d[fileKey]['filename']
        fileSize = d[fileKey]['size']
        fileStatus = d[fileKey]['status']
        fileSharedDate = d[fileKey]['shadate']
        fileExpdDate = d[fileKey]['expdate']
        
        tree.insert('', 'end',fileKey, text=fileName)
        tree.set(fileKey,0,fileSize)
        tree.set(fileKey,1,fileStatus)
        tree.set(fileKey,2,fileSharedDate)
        tree.set(fileKey,3,fileExpdDate)
        tree.set(fileKey,4,fileKey)
    
    sc1 = ttk.Scrollbar(exploframe, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=sc1.set)
    sc1.grid(column = 6,row = 1, rowspan=6, sticky = (N,S))
    sc1x = ttk.Scrollbar(exploframe, orient=HORIZONTAL, command=tree.xview)
    tree.configure(xscrollcommand=sc1x.set)
    sc1x.grid(column = 5,row = 7, sticky = (W,E))
    
    exploframe.columnconfigure(5,weight=1)
    exploframe.rowconfigure(1,weight=1)
    
    for child in exploframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
        
        
    ################ PLACES FRAME ########################,progBar
    emplaframe = ttk.Labelframe(mainframe, text='Storage Locations')
    emplaframe.grid(column=10,row=30, sticky=(N,S,E,W))
    
    emplanb = ttk.Notebook(emplaframe)
    emplanb.grid(column=15, row=10, sticky=(N, S, E, W))
    
    def add_location(loc):
        
        newlocframe = ttk.Frame(emplanb, padding=(3,3,12,12))
        
        locTypelabel = ttk.Label(newlocframe, text='Type: '+loc['type'])
        locTypelabel.grid(column=10, row=10, sticky=(W, E))
        
        passwordCommandlabel = ttk.Label(newlocframe, text='Password: ')
        passwordCommandlabel.grid(column=10, row=20, sticky=(W, E))
        passwordCommandVar = StringVar()
        passwordCommand_entry = ttk.Entry(newlocframe, width=20, textvariable=passwordCommandVar)
        passwordCommand_entry.grid(column=20, row=20, sticky=(W, E))
        passwordCommand_entry.configure(show='')
        passwordCommand_entry.insert(0,loc['pwd'])
        
        Epochlabel = ttk.Label(newlocframe, text='Epoch: '+loc['e1']+' '+loc['e2'])
        Epochlabel.grid(column=10, row=30, sticky=(W, E))
        
        DEpochlabel = ttk.Label(newlocframe, text='Delta of Epoch: '+loc['de1']+' '+loc['de2'])
        DEpochlabel.grid(column=10, row=40, sticky=(W, E))
        
        PMlabel = ttk.Label(newlocframe, text = loc['pm'])
        PMlabel.grid(column=10, row=50, sticky=(W, E))
        
        checkstatus = ttk.Button(newlocframe, text="Check", command = lambda : com.check(loc))
        checkstatus.grid(column=10, row=60)
     
        emplanb.add(newlocframe, text=loc['name'])
        
        for child in newlocframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
    
    for loc in projectDic['locDic']:
        add_location(projectDic['locDic'][loc])
   
    checkplaces = ttk.Button(emplaframe, text="Check All",command=lambda: com.checkall())
    checkplaces.grid(column=10, row=20)
    
    for child in emplaframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
        
    ################ ACTIONS FRAME ########################

    actionframe = ttk.Labelframe(mainframe, text='Planned Tasks')
    actionframe.grid(column=20,row=30, sticky=(N,S,E,W))
    
    actiontree = ttk.Treeview(actionframe)
    actiontree.grid(column=5, row=3, columnspan = 2, sticky=(N, W, E, S))
    
    actiontree.heading('#0',text = 'Actions pending')
    
    d = projectDic['fileDic']
    for item in d:
        if d[item]['planned'] :
            itemStatus = d[item]['status']
            if itemStatus == 'to share' :
                actiontree.insert('', 'end',item, text='share '+d[item]['filename'])
            elif itemStatus == 'to recover' :
                actiontree.insert('', 'end',item, text='recover '+d[item]['filename'])
            elif itemStatus == 'to remove' :
                actiontree.insert('', 'end',item, text='remove '+d[item]['filename'])
    
    sc2 = ttk.Scrollbar(actionframe, orient=VERTICAL, command=actiontree.yview)
    actiontree.configure(yscrollcommand=sc2.set)
    sc2.grid(column = 7,row = 3, sticky = (N,S))
    
    #progBarValue = StringVar()
    #progBar = ttk.Progressbar(actionframe, orient=HORIZONTAL, mode='indeterminate')
    #progBar.grid(column=5, columnspan = 2, row=11,sticky=(W,E))
    #progBar.step(100)
    
    delactions = ttk.Button(actionframe, text="Cancel Tasks",command=lambda: com.cancel_tasks(actiontree,str(mainframe),currentProjects,console))
    delactions.grid(column=5, row=10,sticky=(W,E))
    
    launchactions = ttk.Button(actionframe, text=" Execute Tasks",command=lambda: com.execute_tasks(tree,actiontree,str(mainframe),currentProjects,console,mainframe))
    #TODO: add a functionality to stop the execution of the tasks (modify the appearance of button)
    launchactions.grid(column=6, row=10,sticky=(W,E))
    
    
    
    actionframe.columnconfigure(5,weight=1)
    actionframe.rowconfigure(3,weight=1)
    
    for child in actionframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
        
        
    #######################################################
        
    for child in mainframe.winfo_children():
        if child != toolframe :
            child.grid_configure(padx=20, pady=20)
        
    return mainframe