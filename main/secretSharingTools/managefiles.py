# -*- coding: utf-8 -*-
"""
Created in 2016-2017

Author : Edouard Cuvelier
Affiliation : Université catholique de Louvain - ICTEAM - UCL Crypto Group
Address : Place du Levant 3, 1348 Louvain-la-Neuve, BELGIUM
email : firstname.lastname@uclouvain.be
"""

import pickle
from secretSharingTools import secretsharing as sss
#import time
from hashlib import sha256
from binascii import hexlify
import tarfile #zipfile#gzip, shutil
import os


"""
This module handles the file uploading to and from their storage locations
on the dataservers or clouds
"""

def uploadfile(f,loc):
    """
    Upload the file to location loc
    """
def downloadfile(fname,loc):
    """
    Download the file with the file name fname from the location loc
    """    


"""
#DEPRECATED
def toBytes(s):
    '''
    remove the characters folowing the last 'ffffffff' substring of s then  
    turn the hex string s into a bytes type
    '''
    endp = s.rfind('ffffffff')
    c = s[:endp]
    return bytes.fromhex(c)
    
def toHex(b):
    '''
    turn the bytes object b into a hex string and concatenate with 'ffffffff'
    '''
    return b.hex()+'ffffffff'

def toString(b):
    '''
    remove the last bytes of b that follows and include the byte '11111111' then turn 
    the remaining b into a string
    '''
    endp = b.rfind(b'1111111')
    c = b[:endp]
    return c.decode('ascii')
"""

def appendEndBytes(b):
    '''
    Append the bytes b'\xff\xff\xff\xff\xff\xff\xff\xff' and return
    '''
    return b+b'\xff\xff\xff\xff\xff\xff\xff\xff'
    
def removeEndBytes(b):
    '''
    remove the bytes folowing the last b'\xff\xff\xff\xff\xff\xff\xff\xff' bytes of b and return
    '''
    endp = b.rfind(b'\xff\xff\xff\xff\xff\xff\xff\xff')
    return b[:endp]


def fromBytestoInt(b,k):
    """
    Convert a bytes array to a tuple of int ranging from 0 to 256**(k-1)
    """
    assert len(b)% k == 0
    i = 0
    ck = 0
    T = ()
    while i < len(b):
        nb = 0
        while ck < k :
            nb = nb + b[i]*(256**ck)
            i+=1
            ck+=1
        ck = 0
        T = T+(nb,)
    return T
    
def fromInttoBytes(T,k):
    """
    Convert a tuple of int ranging from 0 to 256**(k-1) to a bytes array 
    """
    b = []
    rT = [0]*k
    for j in range(k-1,-1,-1):
        rT[j] = 256**j
    for i in range(len(T)):
        nb = T[i]
        cb = []
        for j in range(k-1,-1,-1):
            r = rT[j]
            if nb >= r:
                hj = int((nb-nb%r)/r)
                cb.append(hj)
            else :
                cb.append(0)
            nb = nb%r
        cb.reverse()
        b =  b +cb
    return bytes(b)
        
"""
#DEPRECATED in Python 3
def toBin(s):
    '''
    turn the character string s into a binary string
    '''
    
    b = ''
    for x in s :
        bx = format(ord(x), 'b').zfill(8)
        b += bx
        
    b += '11111111'
        
    #for i in range(n-1) :
    #    b += '0'
        
    return b

def toChar(b):
    '''
    remove the last bits of b that follows and include the byte '11111111' then turn 
    the remaining b into a character chain by converting bytes to characters
    '''
    endp = b.rfind('11111111')
    b = b[:endp]
    s = ''
    index = 0
    assert len(b) % 8 == 0
    k = len(b)/8
    print(k)
    for i in range(int(k)):
        bs = b[index:index+8]
        x = chr(int(bs,2))
        index += 8
        s += x
    return s
"""
    
def loadPointer(filename):
    f = open(filename,'rb')
    mysharedfile = pickle.load(f)
    f.close()
    assert type(mysharedfile) is Mysharedfile # the pointer is not a Mysharedfile object
    #mysharedfile.loadSecretSharingSchemefromfile()
    
    return mysharedfile
    
    
def hashname(string):
    """
    Return a SHA-256 of string in hexa decimal representation
    """
    return str(hexlify(sha256(bytes(string,'ascii')).digest()))
    
def getpath(pathf):
        i = pathf.rfind('/')
        return pathf[:i]

def compress(fileordirectoryname,pathf,isaDirectory):
    """   
    def getname(dirname):
        i = dirname[:-1].rfind('/')
        return dirname[i:]
    def addFile(fileordirectoryname,L,tf):
        dirname, subdirs, files  = L
        for fname in files :
            if fname == fileordirectoryname :
                pass
    def addDirectory(L,tf):
        pass
    """
        
    
        
    if isaDirectory :
        tf = tarfile.open(fileordirectoryname[1:]+'.tar.xz', 'w:xz')
        main = os.getcwd()
        os.chdir(getpath(pathf[:-1]))
        for dirname, subdirs, files in os.walk(fileordirectoryname[1:]):
            tf.add(dirname)
            for fname in files :
                tf.add(os.path.join(dirname, fname))
        os.chdir(main)
        tf.close()
        return fileordirectoryname[1:]+'.tar.xz'
                
    else :
        tf = tarfile.open(fileordirectoryname+'.tar.xz', 'w:xz')
        p = getpath(pathf)
        main = os.getcwd()
        os.chdir(p)
        tf.add(fileordirectoryname)
        #addFile(fileordirectoryname,L,tf)
        os.chdir(main)
        tf.close()
        return fileordirectoryname+'.tar.xz'
        
    
    

"""
def compress(fileordirectoryname,pathf,isaDirectory):
    def getname(s):
        i = s[:-1].rfind('/')
        return s[i:]
    
    def addDirectory(dirname,files,tf):
        tf.add(dirname)
        for filename in files:
            tf.add(os.path.join(dirname, filename))
    
    if isaDirectory :
        tf = tarfile.open(fileordirectoryname[1:]+'.tar.xz', 'w:xz')
        L = os.walk(pathf)
        for dirname, subdirs, files in L:
            if getname(dirname) == fileordirectoryname :
                addDirectory(fileordirectoryname,files,tf)
                for subdirname in subdirs :
                    for dirname, subdirs, files in L:
                        if getname(dirname) == subdirname :
                            addDirectory(dirname,files,tf)
        tf.close()
    else :
        f = open(pathf,'rb')
        b = f.read()
        f.close()
        f2 = open(fileordirectoryname,'wb')
        f2.write(b)
        f2.close()
        tf = tarfile.open(fileordirectoryname+'.tar.xz', 'w:xz')
        tf.add(fileordirectoryname)
        tf.close()
        os.remove(fileordirectoryname)
    return fileordirectoryname+'.tar.xz'#os.path.abspath('./')+fileordirectoryname+'.tar.xz'
"""

def uncompress(filename,pathf,isDirectory):
    p = getpath(pathf)
    main = os.getcwd()
    os.chdir(p)
    #TODO: check if file already exists
    if isDirectory :
        tf = tarfile.open(filename[1:], 'r:xz')
    else :
        tf = tarfile.open(filename, 'r:xz')
    tf.extractall()
    tf.close()
    os.chdir(main)

    
class Mysharedfile:
    
    def __init__(self,filename, SSS = None, filenameofSSS = '',listofsharesofmessages = [], salt = 0 ):
        """
        Construct a mysharedfile object given
        - filename, the name of the file
        - eventually the secret sharing scheme used SSS
        - eventually the name of the file, filenameofSSS, containing the SSS
        - eventually a list of shares : listofsharesofmessages
        - eventually a salt : 8 bytes in hexadecimal if not a salt is generated 
        randomly, this is used to generate the filename of the shares

        """
        if not SSS == None :
            assert isinstance(SSS,sss.SecretSharingScheme)
        assert type(filename) == str
        self.filename = filename
        self.SSS = SSS
        self.filenameofSSS = filenameofSSS
        self.listofsharesofmessages = listofsharesofmessages
        self.numberofmessages = len(self.listofsharesofmessages)
        if salt == 0 :
            self.salt = hexlify(os.urandom(8))
        else : 
            assert type(salt) == bytes and len(salt) == 16 # Incorrect salt format 
            self.salt = salt
    
    def sharefile(self):
        try :
            f = open(self.filename,'rb')
        except :
            print('Error : trying to open a non exisiting file named :'+self.filename+' \n try to create it first')
        else :
            b = f.read()
            f.close()
            bs = appendEndBytes(b)
            Mlist = self.SSS.encode(bs)
            SLM = self.SSS.sharelist(Mlist)
            self.listofsharesofmessages = SLM
            self.numberofmessages = len(SLM)
        
        
    def rebuildfile(self):
        """
        From the myfile object, produce the original file
        """
        assert self.listofsharesofmessages != []
        
        ML = self.SSS.retrievelist(self.listofsharesofmessages)

        bx = self.SSS.decode(ML)
        sb = removeEndBytes(bx)
        
        f = open(self.filename,'wb')
        f.write(sb)
        f.close()
    
    def loadSecretSharingSchemefromfile(self):
        f = open(self.filenameofSSS,'rb')
        SSS = pickle.load(f)
        self.SSS = SSS
        
    def save(self,directoryname = '.'):
        """
        this wraps the myfile object into a file named 'pointerto'+self.filename
        to avoid saving multiple times unnecesary object, we explicitly do not
        save self.listofsharesofmessages and self.SSS
        """
        assert self.filename != '' # Cannot save a pointer to a blank name
        assert self.filenameofSSS != '' # The pointer must contain the filename of a Secret Sharing Scheme SSS
        if not directoryname == '.':
            try :
                os.mkdir(directoryname)
            except :
                pass #the directory already exists
        pointertomysharedfile = Mysharedfile(self.filename, None, self.filenameofSSS, [], self.salt)
        pointertomysharedfile.numberofmessages = self.numberofmessages
        s = directoryname+'/pointerto'+self.filename+'.pointer'
        f = open(s,'wb')
        pickle.dump(pointertomysharedfile,f)
        f.close()
        
        return s
        
    def saveShares(self,directorynames = [], numberofparties = 0 ):
        """
        This saves the shares into files (using pickles) that are stored into
        ./directory/sharej where j range from 0 to numberofshares
        if numberofshares is default, the number of shares used is n of the Secret Sharing Scheme self.SSS
        """
        SSS = self.SSS
        #sList = []
        if numberofparties == 0 :
            n = SSS.n
        else :
            n = numberofparties
            
        sdir = [0]*n
        if directorynames != [] :
            assert len(directorynames) ==  n
            for j in range(n):
                dnj = directorynames[j]
                try :
                    os.mkdir(dnj)
                except :
                    pass #the directory already exists
                sdir[j] = dnj
        else :
            # directorynames == []
            try :
                os.mkdir('./shares')
            except :
                pass #the directory already exists
            for j in range(n) :
                sdir[j] = './shares/shares_of_party_'+str(j)+'/'
                try :
                    os.mkdir(sdir[j])
                except :
                    pass #the directory already exists
                    
        #r1 = len(self.listofsharesofmessages)
        r2 = len(self.listofsharesofmessages[0])
        #Loneshare = [0]*r1
        #Lshares = [Loneshare]*r2
        Ldict = {}
        for j in range(r2):
            spre = str(self.salt)+self.filename+'_shares_for_party_'+str(j)
            st = hashname(spre)
            sj = st+'.share'
            Ldict[j] = (sdir[j],sj)
            
        def row(L,i):
            '''
            return row i of list L
            '''
            row_i = ()
            for item in L:
                row_i = row_i+(item[i],)
            return row_i
            
        for j in range(r2) :
            row_j = row(self.listofsharesofmessages,j)
            sdirj, sj = Ldict[j]
            fj = open(sdirj+'/'+sj,'wb')
            pickle.dump(row_j,fj)
            fj.close()
                
            
        """            
        for k in range(len(self.listofsharesofmessages)) :
            sItem = []
            shares_of_message = self.listofsharesofmessages[k]
            for j in range(len(shares_of_message)) :
                share = shares_of_message[j]
                spre = str(self.salt)+self.filename+'_share_of_msg_'+str(k)+'_for_party_'+str(j)
                st = hashname(spre)
                s = sdir[j]+'/'+st+'.share'
                f = open(s,'wb')
                #pickle.dump(share,f)
                byteshare = SSS.shareToBytes(share)
                f.write(byteshare)
                f.close()
                sItem.append(st+'.share')
                '''
                if not pBar == None :
                    # feedback on the progression of the sharing
                    lv = float(pBar.get())
                    #print(lv)
                    pBar.set(str(lv+progStep))
                    #time.sleep(0.1)
                '''
            sList.append(sItem)
        """
                
        return Ldict
        
    def recover_List_of_Filename_of_Shares(self,salt = 0,numberofparties = 0, numberofmessages = 0):
        sList = []
        if numberofparties == 0 :
            n = self.SSS.n
        else :
            n = numberofparties
        """
        if numberofmessages == 0 :
            nom = self.numberofmessages
        else :
            nom = numberofmessages
        """
        if salt == 0 :
            slt = self.salt
        else :
            slt = salt
            
        #sdir = [0]*n
        #for j in range(n) :
        #    sdir[j] = directoryname+'/shares_of_party_'+str(j)+'/'
        for j in range(n) :
            spre = str(slt)+self.filename+'_shares_for_party_'+str(j)
            st = hashname(spre)
            s = st+'.share'
            sList.append(s)
        """
        for k in range(nom) :
            sItem = []
            for j in range(n) :
                spre = str(slt)+self.filename+'_share_of_msg_'+str(k)+'_for_party_'+str(j)
                st = hashname(spre)
                s = st+'.share'
                sItem.append(s)
            sList.append(sItem)
        """
        return sList
        
    def rebuilt_listofsharesmessages(self,Ldict):
        """ 
        SSS = self.SSS
        n = SSS.n
        sdir = [0]*n
        
        
        if directorynames != [] :
            n = len(directorynames)
            for j in range(n):
                sdir[j] = directorynames[j]
        else :
            # directorynames == []
            for j in range(n) :
                sdir[j] = './shares/shares_of_party_'+str(j)
               
        LOSM = []
        for sItem in sList:
            LOSMitem = []
            for j in range(n) :
                s = sdir[j]+'/'+sItem[j]
                f = open(s,'rb')
                byteshare = f.read()
                #binsharel1 = f.readline()
                #binsharel2 = f.readline()
                f.close()
                share = SSS.bytesToShare(byteshare)
                LOSMitem.append(share)
            LOSM.append(LOSMitem)
        """
        Lshares = []
        ErrorList = []
        for key in Ldict :
            sdirj,sj = Ldict[key]  
            try :
                f = open(sdirj+'/'+sj,'rb')
            except FileNotFoundError :
                ErrorList.append(sdirj+'/'+sj)
            else :
                shareList = pickle.load(f)
                f.close()
                Lshares.append(shareList)
        
        def column(L,j):
            column_j = []
            for item in L:
                column_j.append(item[j])
            return column_j
            
        LOSM = []
        for j in range(len(Lshares[0])):
            column_j =  column(Lshares,j)
            LOSM.append(column_j)
            
        self.listofsharesofmessages = LOSM
        return ErrorList
        
    def erase_listofsharesmessages(self,Ldict):
        '''
        SSS = self.SSS
        n = SSS.n
        sdir = [0]*n
        if directorynames != [] :
            n = len(directorynames)
            for j in range(n):
                sdir[j] = directorynames[j]
        else :
            # directorynames == []
            for j in range(n) :
                sdir[j] = './shares/shares_of_party_'+str(j)
        '''
        ErrorList = []      
        for key in Ldict:
            sdirj,sj = Ldict[key]
            s = sdirj+'/'+sj
            try :
                os.remove(s)
            except FileNotFoundError :
                ErrorList.append(s)
                
        return ErrorList
                

    def __str__(self):
        s = 'Pointer to '+self.filename+'\n this pointer uses the SSS '+str(self.SSS)+' stored in '+self.filenameofSSS
        return s
        
    def __repr__(self):
        return str(self)
