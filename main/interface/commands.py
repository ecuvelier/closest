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
from interface import mainframe as mf
import managefiles
import pickle
#import tools.fingexp as fingexp
from secretSharingTools import secretsharing as ss
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
        return ss.ShamirSecretSharing(Fp,SSSThreshold,SSS_n)
    else :
        raise NotImplementedError
        
def getField(modSize):
    s = 'F'+modSize
    f = open('./secretSharingTools/'+s,'rb')
    Fp = pickle.load(f)
    f.close()
    return Fp


################### MENU INTERFACE ################################

def new_project(root,nb,currentProjects):
    project_window.create_project_window(root,nb,currentProjects)
    
def save_project(nb,currentProjects):
    
    tabname = nb.select()
    projectDic = currentProjects[tabname]
    pDcopy = projectDic.copy()
    pDcopy['builtSSS']  = None #Do not save the SSS used (redundant)

    filename = filedialog.asksaveasfilename(initialfile=projectDic['name'],defaultextension='.closest')
    if not filename == '' and not filename == ():
        f = open(filename,'wb')
        pickle.dump(pDcopy,f)
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
        currentProjects[str(newframe)]['builtSSS'] = builtSSS(projectDic)
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
        
def freeze(frameid):
    pass

def unfreeze(frameid):
    pass
        
        
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
            currentProjects[frameid]['fileDic'][item]['planned']= False
            tree.set(item,1,'not shared')
        elif currentStatus == 'to delete' or currentStatus == 'to recover' :
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
            elif itemStatus == 'to recover' :
                actiontree.insert('', 'end',item, text='recover '+d[item]['filename'])
                d[item]['planned'] = True
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

def cancel_tasks(actiontree,frameid,currentProjects,console,progBar):
    progBar.configure(value = 0)
    for item in actiontree.selection() :
        fname = currentProjects[frameid]['fileDic'][item]['filename']
        currentProjects[frameid]['fileDic'][item]['planned'] = False
        actiontree.delete(item)
        WriteConsole(console,'Action on '+fname+' canceled')


def execute_tasks(tree,actiontree,frameid,currentProjects,console,progBar):
    
    freeze(frameid)
    try :
        os.mkdir('/recovered files/')
    except :
        pass #the directory already exists
    progBar.configure(value = 0)
    #progBar.step(50)
    cd = currentProjects[frameid]['fileDic']
    nbofActions = 0
    for item in cd:
        if cd[item]['planned'] == True :
            nbofActions +=  1
            
    st1 = 100/nbofActions
    for item in cd:
        if cd[item]['planned'] == True :
            fname = cd[item]['filename']
            itemStatus = cd[item]['status']
            
            if itemStatus == 'to share':
                WriteConsole(console,'Sharing '+fname)
                
                compressedfilename = managefiles.compress(item)
                
                SecSharSchem =  currentProjects[frameid]['builtSSS']
                
                sharedfile = managefiles.Mysharedfile(compressedfilename, SSS = SecSharSchem )
                sharedfile.sharefile() #Build the list of shares
                k = (sharedfile.numberofmessages)*(SecSharSchem.n)
                #print(sharedfile.numberofmessages)
                #print(SecSharSchem.n)
                st2 = st1/k
                dN = []
                for lockey in currentProjects[frameid]['locDic']:
                    locDir = lockey+'_'+currentProjects[frameid]['locDic'][lockey]['name']
                    dN.append(locDir)
                dN.sort()
                sharedfile.saveShares(directorynames = dN, pBar = progBar, progStep = st2) #TODO : Save the shares in the correct locations and not in directories
                      
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
                
                os.remove(compressedfilename)
                
                WriteConsole(console,fname+' shared' )
                quick_save_project(currentProjects[frameid],console)
                
            elif itemStatus == 'to recover' or itemStatus == 'to remove':
                if itemStatus == 'to remove' :
                    WriteConsole(console,'removing '+ fname )
                else : #itemStatus == 'to recover'
                    WriteConsole(console,'recovering '+ fname )
                    
                SecSharSchem =  currentProjects[frameid]['builtSSS']
                
                sharedfile = cd[item]['pointer']
                sharedfile.SSS = SecSharSchem
                sL = sharedfile.recover_List_of_Filename_of_Shares()
                dN = []
                for lockey in currentProjects[frameid]['locDic']:
                    locDir = lockey+'_'+currentProjects[frameid]['locDic'][lockey]['name']
                    dN.append(locDir)
                dN.sort()
                
                if itemStatus == 'to remove' :
                    sharedfile.erase_listofsharesmessages(sL,dN)
                    actiontree.delete(item)
                    tree.delete(item)
                    WriteConsole(console,fname+' removed' )
                else : #itemStatus == 'to recover'
                    sharedfile.rebuilt_listofsharesmessages(sL,dN)
                    sharedfile.filename = '/recovered files/'+cd[item]['filename']
                    sharedfile.rebuildfile()
                    managefiles.uncompress(sharedfile.filename)
                    os.remove(sharedfile.filename)
                    
                    tree.set(item,1,'not shared')
                    tree.set(item,2,'')
                    tree.set(item,3,'')
                    cd[item]['planned'] = False
                    cd[item]['shadate'] = ''
                    cd[item]['expdate'] = ''
                    cd[item]['status'] = 'not shared'
                    actiontree.delete(item)
                
                    WriteConsole(console,fname+' recovered' )
                    
                quick_save_project(currentProjects[frameid],console)
            
    unfreeze(frameid)
    

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
    currentProjects[str(newframe)]['builtSSS'] = builtSSS(projectDic)
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
    
