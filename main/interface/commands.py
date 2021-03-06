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
from binascii import hexlify
import os
from interface import project_window
from interface import proccessing_window as p_w
from interface import mainframe as mf
from secretSharingTools import managefiles
import pickle
#import tools.fingexp as fingexp
from secretSharingTools import secretsharing as ss
#from mathTools import field
import time

def myrandom(a,b):
    """
    return a random number between a and b
    """
    c = b-a
    l = int(((len(bin(c))-2)/8))
    r = int(hexlify(os.urandom(max(l,128))),16)%(c+1)
    assert a+r<=b
    return a+r

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
    

def getEpoch(projDic):
    print(projDic)
    def toSeconds(a1,a2):
        if a2 == 'day(s)':
            return a1*86400
        elif a2 == 'week(s)':
            return a1*604800
        elif a2 == 'month(s)':
            return a1*2678400
        elif a2 == 'year(s)':
            return a1*31536000
            
    epochDic = {}       
            
    for location in projDic['locDic']:
        e1 = projDic['locDic'][location]['e1']
        e2 = projDic['locDic'][location]['e2']
        de1 = projDic['locDic'][location]['de1']
        de2 = projDic['locDic'][location]['de2']
        
        n1 = toSeconds(int(e1),e2)
        n2 = toSeconds(int(de1),de2)
        rn2 = myrandom(0,n2)
        
        epochDic[location] = n1,rn2
        
    return epochDic
    
def builtSSS(projDic):
    SSSType = projDic['SSS']
    SSSThreshold = int(projDic['Threshold'])
    SSS_n = int(projDic['Nb_of_loc'])
    SSS_modsize = projDic['Mod']
    if SSSType == 'Shamir' :
        Fp = getField(SSS_modsize)
        if not Fp == None :
            return ss.ShamirSecretSharing(Fp,SSSThreshold,SSS_n)
        else :
            return None 
    else :
        raise NotImplementedError
        
def getField(modSize):
    #p = field.pDict['p'+modSize]
    #Fp = field.Field(p)
    s = 'F'+modSize
    try :
        f = open('./Fields/'+s,'rb')
    except FileNotFoundError :
        return None
    else :
        Fp = pickle.load(f)
        f.close()
        return Fp


################### MENU INTERFACE ################################

def new_project(root,nb,currentProjects):
    project_window.create_project_window(root,nb,currentProjects)
    
def save_project(nb,currentProjects):
    
    tabname = nb.select()
    try :
        projectDic = currentProjects[tabname]
    except KeyError :
        messagebox.showinfo(message='No project to save...' )
        return
    pDcopy = projectDic.copy()
    pDcopy['builtSSS']  = None #Do not save the SSS used (redundant)

    filename = filedialog.asksaveasfilename(initialfile=projectDic['name'],defaultextension='.closest')
    if not filename == '' and not filename == ():
        f = open(filename,'wb')
        pickle.dump(pDcopy,f)
        f.close()
   
def open_project(nb,currentProjects):
    filename = filedialog.askopenfilename()
    if not filename == '' and not filename == () :
        if not '.closest' in filename:
            messagebox.showinfo(message='Wrong format for '+filename, icon = 'error' )
            return
        f = open(filename,'rb')
        try :
            projectDic = pickle.load(f)
        except pickle.UnpicklingError :
            messagebox.showinfo(message='Unable to exctract the project from '+filename+'\n\n (pickle error)', icon = 'error' )
            return
        f.close()
        if not type(projectDic) == dict :
            messagebox.showinfo(message='Unable to exctract the project from '+filename+'\n\n (dict error)', icon = 'error' )
            return
        #print(projectDic)
        newframe = mf.create_mainframe(nb,currentProjects,projectDic)
        #print(newframe)
        currentProjects[str(newframe)] = projectDic
        bS = builtSSS(projectDic)
        if bS == None :
            messagebox.showinfo(message='Unable to build the secret sharing scheme.', icon = 'error' )
        else :
            currentProjects[str(newframe)]['builtSSS'] = bS
            nb.add(newframe, text=projectDic['name'])
    
def modify_project(*args):
    messagebox.showinfo(message='Not Implemented Yet')
    pass

def print_project_in_console(nb,currentProjects):
    tabname = nb.select()
    messagebox.showinfo(message='Current Project dictionary: '+str(currentProjects[tabname]))

def about(root):
    print(root.winfo_width(), root.winfo_height())
    messagebox.showinfo(message='Not Implemented Yet')
    pass

def help_func(*args):
    messagebox.showinfo(message='Not Implemented Yet')
    pass


################### MAINFRAME ################################

def quick_save_project(projectDic,console):
    try :
        filename = projectDic['filename']
    except KeyError :
        messagebox.showinfo(message='File not saved.\n The original file '+projectDic['name']+' was not found in its original location.\n Try saving via the Menu bar')
    else :
        f = open(filename,'wb')
        pickle.dump(projectDic,f)
        f.close()
        WriteConsole(console,getname(filename)+' saved on '+time.ctime())
    

def closetab(notebook,tab):
    r = messagebox.askyesno(message='Are you sure you want to close the project?',icon='question', title='Close Project')
    if r :
        notebook.forget(tab)
        
def freeze(parent):
    proccesingwindow,progBar = p_w.create_proccessing_window(parent)
    progBar.start()
    return proccesingwindow,progBar

def unfreeze(proccesingwindow,progBar):
    progBar.stop()
    proccesingwindow.destroy()
        
        
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
        currentProjects[frameid]['fileDic'][s] = {'filename':fname,'size':size,'status':'not shared','shadate':'','expdate':'','planned':False,'directory':False}

def adddir(tree,frameid,currentProjects):
    s =  filedialog.askdirectory()
    if not s == '' and not s == ():
        fname = '/'+getname(s)
        size = convertsize(get_size(s))
        tree.insert('', 'end',s, text=fname)
        tree.set(s,0,size)
        tree.set(s,1,'not shared')
        tree.set(s,4,s)
        currentProjects[frameid]['fileDic'][s] = {'filename':fname,'size':size,'status':'not shared','shadate':'','expdate':'','planned':False,'directory':True}

def share(tree,frameid,currentProjects,console):
    errorList = []
    for item in tree.selection() :
        currentStatus = currentProjects[frameid]['fileDic'][item]['status']
        if currentStatus == 'not shared' :
            currentProjects[frameid]['fileDic'][item]['status']= 'to share'
            tree.set(item,1,'to share')
        elif currentStatus == 'shared' :
            currentProjects[frameid]['fileDic'][item]['status']= 'to re-share'
            tree.set(item,1,'to re-share')
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
        if currentStatus == 'shared' or currentStatus == 'to recover' or currentStatus == 'to re-share':
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
            currentProjects[frameid]['fileDic'][item]['planned']= False
            tree.set(item,1,'not shared')
        elif currentStatus == 'to remove' or currentStatus == 'to recover' or currentStatus == 'to re-share':
            currentProjects[frameid]['fileDic'][item]['status']= 'shared'
            currentProjects[frameid]['fileDic'][item]['planned']= False
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
                d[item]['planned'] = True
            elif itemStatus == 'to re-share' :
                actiontree.insert('', 'end',item, text='re-share '+d[item]['filename'])
                d[item]['planned'] = True
            elif itemStatus == 'to recover' :
                actiontree.insert('', 'end',item, text='recover '+d[item]['filename'])
                d[item]['planned'] = True
            elif itemStatus == 'to remove' :
                actiontree.insert('', 'end',item, text='remove '+d[item]['filename'])
                d[item]['planned'] = True
            
            
    

def remove(tree,actiontree,frameid,currentProjects,console):
    for item in tree.selection() :
        currentStatus = currentProjects[frameid]['fileDic'][item]['status']
        if currentStatus == 'shared' or currentStatus == 'to recover' or currentStatus == 'to remove' or currentStatus == 'to re-share':
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
    #progBar.configure(value = 0)
    for item in actiontree.selection() :
        fname = currentProjects[frameid]['fileDic'][item]['filename']
        currentProjects[frameid]['fileDic'][item]['planned'] = False
        actiontree.delete(item)
        WriteConsole(console,'Action on '+fname+' canceled')


def execute_tasks(tree,actiontree,frameid,currentProjects,console,parent):
    
    p_win, pBar = freeze(parent)
    try :
        os.mkdir('./recovered files/')
    except :
        pass #the directory already exists
    #progBarValue.set(0)
    #progBar.step(50)
    #progBar.start()
    cd = currentProjects[frameid]['fileDic']
    nbofActions = 0
    for item in cd:
        if cd[item]['planned'] == True :
            nbofActions +=  1
            
    #st1 = 100/nbofActions
    for item in cd:
        if cd[item]['planned'] == True :
            fname = cd[item]['filename']
            itemStatus = cd[item]['status']
            
            if itemStatus == 'to share' or itemStatus == 'to re-share':
                SecSharSchem =  currentProjects[frameid]['builtSSS']
                dN = []
                for lockey in currentProjects[frameid]['locDic']:
                    locDir = lockey+'_'+currentProjects[frameid]['locDic'][lockey]['name']
                    dN.append(locDir)
                dN.sort()
                
                if itemStatus == 'to share' :
                    WriteConsole(console,'Sharing '+fname)
                    compressedfilename = managefiles.compress(fname,item,cd[item]['directory'])
                    sharedfile = managefiles.Mysharedfile(compressedfilename, SSS = SecSharSchem )
                    sharedfile.sharefile() #Build the list of share
                else : # itemStatus == 'to-re-share'
                    WriteConsole(console,'Re-sharing '+fname)
                    sharedfile = cd[item]['pointer']
                    sharedfile.SSS = SecSharSchem
                    if cd[item]['directory'] :
                        sharedfile.filename = cd[item]['filename'][1:]+'.tar.xz'
                    else :
                        sharedfile.filename = cd[item]['filename']+'.tar.xz'
                    Ldict = {}
                    sL = sharedfile.recover_List_of_Filename_of_Shares()
                        
                    for lockey in currentProjects[frameid]['locDic']:
                        locDir = lockey+'_'+currentProjects[frameid]['locDic'][lockey]['name']
                        j = int(lockey)
                        Ldict[j] = (locDir,sL[j])
                        
                    ErrorList = sharedfile.rebuilt_listofsharesmessages(Ldict)
                    for error in ErrorList :
                        WriteConsole(console,'share stored at '+error+' of '+fname+' not found and thus not re-shared' )
                        
                    new_LOSM = SecSharSchem.resharelist(sharedfile.listofsharesofmessages)
                    sharedfile.listofsharesofmessages = new_LOSM
                    
                    ErrorList = sharedfile.erase_listofsharesmessages(Ldict)
                    for error in ErrorList :
                        WriteConsole(console,'share stored at '+error+' of '+fname+' not found and thus not removed' )
                    
                    #sharedfile.filename = cd[item]['filename']
                
                sharedfile.saveShares(directorynames = dN) #TODO : Save the shares in the correct locations and not in directories
                      
                tree.set(item,1,'shared')
                ct = time.ctime()
                tree.set(item,2,ct)
                epochDic = getEpoch(currentProjects[frameid])
                e1,de1 = min(epochDic.values())
                ect = time.ctime(time.time()+e1+de1)
                tree.set(item,3,ect)
                cd[item]['planned'] = False
                cd[item]['shadate'] = ct
                cd[item]['expdate'] = ect
                cd[item]['status'] = 'shared'
                actiontree.delete(item)
                
                sharedfile.SSS = None  # Erase SSS
                sharedfile.listofsharesofmessages = [] # Erase lsm
                cd[item]['pointer'] = sharedfile
                
                
                if itemStatus == 'to share' :
                    os.remove(compressedfilename)
                    WriteConsole(console,fname+' shared' )
                else : # itemStatus == 'to-re-share'
                    WriteConsole(console,fname+' re-shared' )
                
                #quick_save_project(currentProjects[frameid],console)
                
            elif itemStatus == 'to recover' or itemStatus == 'to remove':
                if itemStatus == 'to remove' :
                    WriteConsole(console,'removing '+ fname )
                else : #itemStatus == 'to recover'
                    WriteConsole(console,'recovering '+ fname )
                    
                SecSharSchem =  currentProjects[frameid]['builtSSS']
                
                sharedfile = cd[item]['pointer']
                if cd[item]['directory'] :
                    sharedfile.filename = cd[item]['filename'][1:]+'.tar.xz'
                else :
                    sharedfile.filename = cd[item]['filename']+'.tar.xz'
                sharedfile.SSS = SecSharSchem
                Ldict = {}
                sL = sharedfile.recover_List_of_Filename_of_Shares()
                #dN = []
                for lockey in currentProjects[frameid]['locDic']:
                    locDir = lockey+'_'+currentProjects[frameid]['locDic'][lockey]['name']
                    #dN.append(locDir)
                    j = int(lockey)
                    Ldict[j] = (locDir,sL[j])
                #dN.sort()
                
                if itemStatus == 'to remove' :
                    ErrorList = sharedfile.erase_listofsharesmessages(Ldict)
                    for error in ErrorList :
                        WriteConsole(console,'share stored at '+error+' of '+fname+' not found and thus not deleted' )
                    actiontree.delete(item)
                    tree.delete(item)
                    cd[item] = 'deleted'
                    WriteConsole(console,fname+' removed (modulo errors)')
                else : #itemStatus == 'to recover'
                    ErrorList = sharedfile.rebuilt_listofsharesmessages(Ldict)
                    for error in ErrorList :
                        WriteConsole(console,'share stored at '+error+' of '+fname+' not found' )
                    
                    filepath = './recovered files/'+cd[item]['filename']+'.tar.xz'
                    sharedfile.filename = './recovered files/'+cd[item]['filename']+'.tar.xz'
                    try :
                        sharedfile.rebuildfile()
                    except AssertionError :
                        WriteConsole(console,'Not enough shares to reconstruct '+fname )
                    else :
                        sharedfile.filename = cd[item]['filename']
                        managefiles.uncompress(sharedfile.filename+'.tar.xz',filepath,cd[item]['directory'])
                        os.remove('./recovered files/'+cd[item]['filename']+'.tar.xz')
                        tree.set(item,1,'shared')
                        cd[item]['planned'] = False
                        cd[item]['status'] = 'shared'
                        actiontree.delete(item)
                        WriteConsole(console,fname+' recovered' )
                    
                
                
    #progBar.stop()
    for k in list(cd) :
        if cd[k] == 'deleted':
            cd.pop(k)
    unfreeze(p_win, pBar)
    quick_save_project(currentProjects[frameid],console)
    

######### CONSOLE FRAME ###########

def WriteConsole(console,message):
    console.config(state=NORMAL)
    console.insert('end','\n>>> '+message)
    console.config(state=DISABLED)
    console.see('end')

        
################## PROJECT WINDOW ####################################

def save_open_project(root,win,nb,projectDic,currentProjects):
    print(projectDic)
    filename = filedialog.asksaveasfilename(initialfile=projectDic['name'],defaultextension='.closest')
    if not filename == '' and not filename == ():
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
        currentProjects[str(newframe)]['builtSSS'] = builtSSS(projectDic)
        win.destroy()
        newframe.focus()
    
    root.mainloop()

def open_modify_project(root,projectwindow):
    r = messagebox.askyesno(message='Opening a new project will close the current project.\n Are you sure?',icon='question', title='Opening Project')
    if r :
        projectwindow.destroy()
        messagebox.showinfo(message='Not Implemented Yet')

def save_edited_project(nb):
    messagebox.showinfo(message='Not Implemented Yet')
    pass

def synch_epoch(parent,LocationDic,dB = False):
    epochwindow = Toplevel(parent)
    if not dB :
        epochwindow.title('Synchronized epoch')
    else :
        epochwindow.title('Synchronized delta of epoch')
    
    mframe = ttk.Frame(epochwindow, padding=(3,3,12,12))
    mframe.grid(column=10,row=10, sticky=(N,S,E,W))
    
    Nv = ('1','2','3','4','5','6','7','8','9','10','11')
    Mv = ('day(s)','week(s)','month(s)','year(s)')
        
    Epochlabel = ttk.Label(mframe, text='Epoch :')
    Epochlabel.grid(column=10, row=10, sticky=(W, E))
    EpochVar1 = StringVar()
    EpochCB1 = ttk.Combobox(mframe, textvariable=EpochVar1)
    EpochCB1.grid(column=20, row=10, sticky=(W, E))
    EpochCB1['values'] = Nv
    EpochCB1.configure(state='readonly')
    EpochCB1.current(2)
        
    EpochVar2 = StringVar()
    EpochCB2 = ttk.Combobox(mframe, textvariable=EpochVar2)
    EpochCB2.grid(column=30, row=10, sticky=(W, E))
    EpochCB2['values'] = Mv
    EpochCB2.configure(state='readonly')
    EpochCB2.current(2)
    
    def Ok():
        newe1 = EpochVar1.get()
        newe2 = EpochVar2.get()
        for key in LocationDic:
            location = LocationDic[key]
            if not dB :
                location['e1'].set(newe1)
                location['e2'].set(newe2)
            else :
                location['de1'].set(newe1)
                location['de2'].set(newe2)
        epochwindow.destroy()

    
    OKButton = ttk.Button(mframe, text="OK",command= lambda : Ok())
    OKButton.grid(column=10, row=20)
    CancelButton = ttk.Button(mframe, text="Cancel",command= lambda : epochwindow.destroy())
    CancelButton.grid(column=20, row=20)
    
    for child in mframe.winfo_children():
        child.grid_configure(padx=5, pady=5)


def synch_pm(LocationDic,checkPMVar):
    for key in LocationDic:
        location = LocationDic[key]
        if checkPMVar.get() == '1' :
            location['pm'].set('Pattern Masking Enabled')
        else :
            location['pm'].set('Pattern Masking Disabled')
    #messagebox.showinfo(message='Not Implemented Yet')
    #pass

def cancel_project(root,projectwindow):
    projectwindow.destroy()
    root.mainloop()
    
