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
import commands as com


def create_mainframe(parent,projectDic={}):
    if projectDic == {} :
        projectDic['SSS'] = ''
        projectDic['Threshold'] = ''
        projectDic['Nb_of_loc'] = ''
        projectDic['locDic'] = {}
        
    mainframe = ttk.Frame(parent, padding=(3,3,12,12))
    mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
    
    mainframe.columnconfigure(5,weight=1)
    mainframe.columnconfigure(20,weight=1)
    mainframe.rowconfigure(0,weight=1)
    mainframe.rowconfigure(3,weight=1)
    mainframe.rowconfigure(4,weight=1)
    mainframe.rowconfigure(20,weight=1)
    mainframe.columnconfigure(1,weight=3)
    mainframe.columnconfigure(10,weight=3)
    mainframe.rowconfigure(1,weight=3)
    mainframe.rowconfigure(14,weight=3)
    
    ################ Tool FRAME ########################
    
    toolframe = ttk.Frame(mainframe)
    toolframe.grid(column=1,row=2, columnspan = 10, sticky=(E))
    
    bclose = ttk.Button(toolframe, text="Close ❌",command= lambda : com.closetab(parent,mainframe))
    bclose.grid(column=3, row=0)
    #bopen = ttk.Button(toolframe, text="",command = lambda : com.open_project(parent))
    #bopen.grid(column=1, row=0)
    bsave = ttk.Button(toolframe, text="Save ", command = lambda : com.quick_save_project(projname))
    bsave.grid(column=2, row=0)
    
    
    for child in toolframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
    
    ################ EXPLO FRAME ########################
    
    exploframe = ttk.Labelframe(mainframe, text='Virtual Repository')
    exploframe.grid(column=1,row=3, rowspan = 10, sticky=(N,S,E,W))
    
    addrepo = ttk.Button(exploframe, text="Add a Directory", command= lambda : com.adddir(tree))
    addrepo.grid(column=3, row=1,sticky=W)
    
    addfile = ttk.Button(exploframe, text="Add a File", command=lambda : com.addfile(tree))
    addfile.grid(column=3, row=2,sticky=W)
    
    reshare = ttk.Button(exploframe, text="(Re-)Share   ")
    reshare.grid(column=3, row=3,sticky=W)
    
    recover = ttk.Button(exploframe, text="Recover   ")
    recover.grid(column=3, row=4,sticky=W)
    
    planactions = ttk.Button(exploframe, text="Plan Actions")
    planactions.grid(column=3, row=5,sticky=W)
    
    delete = ttk.Button(exploframe, text="Delete")
    delete.grid(column=3, row=6,sticky=W)
    
    tree = ttk.Treeview(exploframe, columns = ['size','status','shared on','exp date'])
    tree.grid(column=5, row=1, rowspan=6, sticky=(N, W, E, S))
    
    update = ttk.Button(exploframe, text="Reload Project File/ ",command =com.updateb)
    update.grid(column=5, row=8,sticky=(E,W))
    
    tree.heading('#0',text = 'path')
    tree.column('#0',anchor = W,minwidth = 100, stretch = True, width = 200)
    tree.heading(0,text = 'size')
    tree.column(0,anchor = E, minwidth = 100, stretch = True, width = 100)
    tree.heading(1,text = 'status')
    tree.column(1,anchor = E,minwidth = 100, stretch = True, width = 100)
    tree.heading(2,text = 'shared on')
    tree.column(2,anchor = E,minwidth = 100, stretch = True, width = 100)
    tree.heading(3,text = 'expiration date')
    tree.column(3,anchor = E,minwidth = 100, stretch = True, width = 100)
    
    # Inserted at the root, program chooses id:
    tree.insert('', 'end', 'doc', text='./example.txt')
    tree.set('doc',0,'14KB')
    tree.set('doc',1,'shared')
    tree.set('doc',2,'16 Jan. 2017')
    tree.set('doc',3,'31 Apr. 2017')
    
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
        
        
    ################ PARAMETERS FRAME ########################
        
    paramframe = ttk.Labelframe(mainframe, text='Parameters')
    paramframe.grid(column=10,row=3, sticky=(N,S,E,W))
    
    parameters = StringVar()
    splus = ''
    if projectDic['SSS'] == 'Shamir' :
        splus = ' with '+projectDic['Mod']+'-bit Module'
        
    sparam = projectDic['Threshold']+'-out-of-'+projectDic['Nb_of_loc']+' '+projectDic['SSS']+' Secret Sharing Scheme'+splus
    paramlabel = ttk.Label(paramframe, text=sparam)
    paramlabel.grid(column=2, row=2, sticky=(W, E))
    parameters.set(sparam)
    
    for child in paramframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
        
    ################ PLACES FRAME ########################
    emplaframe = ttk.Labelframe(mainframe, text='Storage Locations')
    emplaframe.grid(column=10,row=5, sticky=(N,S,E,W))
    
    emplanb = ttk.Notebook(emplaframe)
    emplanb.grid(column=10, row=10, sticky=(N, S, E, W))
    
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
        
        checkstatus = ttk.Button(newlocframe, text="Check")
        checkstatus.grid(column=10, row=60)
     
        emplanb.add(newlocframe, text=loc['name'])
        
        for child in newlocframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    """
    #emplacement1 = StringVar()
    ttk.Label(emplaframe, text='').grid(column=4, row=2, sticky=(W, E))
    ttk.Label(emplaframe, text="Storage Location 1 :").grid(column=2, row=2, sticky=W)
    ttk.Label(emplaframe, text=" Status :").grid(column=5, row=3, sticky=(W,E))
    checkstatus1 = ttk.Button(emplaframe, text="Check")
    checkstatus1.grid(column=2, row=3,sticky=(W,E))
    #emplacement1.set(LOC[0][1])
   
    #emplacement2 = StringVar()
    ttk.Label(emplaframe, text='').grid(column=4, row=5, sticky=(W, E))
    ttk.Label(emplaframe, text="Storage Location 2 :").grid(column=2, row=5, sticky=W)
    ttk.Label(emplaframe, text=" Status :").grid(column=5, row=6, sticky=(W,E))
    checkstatus2 = ttk.Button(emplaframe, text="Check")
    checkstatus2.grid(column=2, row=6,sticky=(W,E))
    #emplacement2.set(LOC[1][1])
   
    #emplacement3 = StringVar()
    emp3Lab = ttk.Label(emplaframe)
    emp3Lab.grid(column=4, row=8, sticky=(W, E))
    ttk.Label(emplaframe, text="Storage Location 3 :").grid(column=2, row=8, sticky=W)
    ttk.Label(emplaframe, text=" Status :").grid(column=5, row=9, sticky=(W,E))
    checkstatus3 = ttk.Button(emplaframe, text="Check" )
    checkstatus3.grid(column=2, row=9,sticky=(W,E))
    
    if int(nbSLvar) >= 3:
        emp3Lab['text'] = LOC[2][1]
    else :
        emp3Lab['text'] = 'disabled'
        checkstatus3.configure(state='disabled')
    
   
    #emplacement4 = StringVar()
    emp4Lab = ttk.Label(emplaframe)
    emp4Lab.grid(column=4, row=11, sticky=(W, E))
    ttk.Label(emplaframe, text="Storage Location 4 :").grid(column=2, row=11, sticky=W)
    ttk.Label(emplaframe, text=" Status :").grid(column=5, row=12, sticky=(W,E))
    checkstatus4 = ttk.Button(emplaframe, text="Check")
    checkstatus4.grid(column=2, row=12,sticky=(W,E))
    
    if int(nbSLvar) >= 4:
        emp4Lab['text']=LOC[3][1]
    else :
        emp4Lab['text']='disabled'
        checkstatus4.configure(state='disabled')
    
   
    #emplacement5 = StringVar()
    emp5Lab =ttk.Label(emplaframe)
    emp5Lab.grid(column=4, row=14, sticky=(W, E))
    ttk.Label(emplaframe, text="Storage Location 5 :").grid(column=2, row=14, sticky=W)
    ttk.Label(emplaframe, text=" Status :").grid(column=5, row=15, sticky=(W,E))
    checkstatus5 = ttk.Button(emplaframe, text="Check")
    checkstatus5.grid(column=2, row=15,sticky=(W,E))
    
    if int(nbSLvar) == 5:
        emp5Lab['text']=LOC[4][1]
    else :
        emp5Lab['text']='disabled'
        checkstatus5.configure(state='disabled')
    """
    
    for loc in projectDic['locDic']:
        add_location(projectDic['locDic'][loc])
   
    checkplaces = ttk.Button(emplaframe, text="Check All",command=lambda:mainframe.update())
    checkplaces.grid(column=10, row=20)
    
    for child in emplaframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
        
    ################ ACTIONS FRAME ########################

    actionframe = ttk.Labelframe(mainframe, text='Planned Tasks')
    actionframe.grid(column=1,row=15, sticky=(N,S,E,W))
    
    actiontree = ttk.Treeview(actionframe)
    actiontree.grid(column=5, row=3, columnspan = 2, sticky=(N, W, E, S))
    
    actiontree.heading('#0',text = 'Actions pending')

    actiontree.insert('', 0, 'gallery', text='Share example.txt')

    
    sc2 = ttk.Scrollbar(actionframe, orient=VERTICAL, command=actiontree.yview)
    actiontree.configure(yscrollcommand=sc2.set)
    sc2.grid(column = 7,row = 3, sticky = (N,S))
    
    delactions = ttk.Button(actionframe, text="Delete Tasks")
    delactions.grid(column=5, row=10,sticky=(W,E))
    
    launchactions = ttk.Button(actionframe, text=" Execute Tasks")
    launchactions.grid(column=6, row=10,sticky=(W,E))
    
    actionframe.columnconfigure(5,weight=1)
    actionframe.rowconfigure(3,weight=1)
    
    for child in actionframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
        
    ################ CONSOLE FRAME ########################

    consoleframe = ttk.Labelframe(mainframe, text='Console')
    consoleframe.grid(column=10,row=15, sticky=(N,S,E,W))
    
    console = Text(consoleframe, width=50, height=20)
    console.grid(column=5,row=5,sticky = (N,S,E,W))
    console.config(state=DISABLED)
    
    sc3 = ttk.Scrollbar(consoleframe, orient=VERTICAL, command=console.yview)
    console.configure(yscrollcommand=sc3.set)
    sc3.grid(column = 6,row = 5, sticky = (N,S))
    
    consoleframe.columnconfigure(5,weight=1)
    consoleframe.rowconfigure(5,weight=1)
    
    
    for child in consoleframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)
        
    #######################################################
        
    for child in mainframe.winfo_children():
        if child != toolframe :
            child.grid_configure(padx=20, pady=20)
        
    return mainframe