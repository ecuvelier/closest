# -*- coding: utf-8 -*-
"""
Created in 2016

Author : Edouard Cuvelier
Affiliation : Université catholique de Louvain - ICTEAM - UCL Crypto Group
Address : Place du Levant 3, 1348 Louvain-la-Neuve, BELGIUM
email : firstname.lastname@uclouvain.be
"""

import pickle
import secretsharing as sss
import time
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
    
def toBin(s):
    """
    turn the character string s into a binary string
    """
    b = ''
    for x in s :
        bx = format(ord(x), 'b').zfill(8)
        b += bx
        
    b += '11111111'
        
    #for i in range(n-1) :
    #    b += '0'
        
    return b
    
def toChar(b):
    """
    remove the last bits of b that follows and include the byte '11111111' then turn 
    the remaining b into a character chain by converting bytes to characters
    """
    endp = b.rfind('11111111')
    b = b[:endp]
    s = ''
    index = 0
    assert len(b) % 8 == 0
    k = len(b)/8
    for i in range(k):
        bs = b[index:index+8]
        x = chr(int(bs,2))
        index += 8
        s += x
    return s
    
def loadPointer(filename):
    f = open(filename,'r')
    mysharedfile = pickle.load(f)
    f.close()
    assert type(mysharedfile) is Mysharedfile # the pointer is not a Mysharedfile object
    mysharedfile.loadSecretSharingSchemefromfile()
    

    
class Mysharedfile:
    
    def __init__(self,filename, SSS = None, filenameofSSS = '',listofsharesofmessages = [],listoflocations = [],epoch = 2678400 ):
        """
        Construct a mysharedfile object given
        - filename, the name of the file
        - eventually the secret sharing scheme used SSS
        - eventually the name of the file, filenameofSSS, containing the SSS
        - eventually a list of shares : listofsharesofmessages
        - eventually a list of the messages locations where each element is 
        a list 'msgID' for every message and in the list 'msgID',
        each element is on the form (shareID, location)
        - epoch is the interval of time after wich a file has to be reshared, 
        by default the time is one month
        """
        if not SSS == None :
            assert type(SSS) == sss.SecretSharingScheme
        assert type(filename) == str
        self.filename = filename
        self.SSS = SSS
        self.filenameofSSS = filenameofSSS
        self.listofsharesofmessages = listofsharesofmessages
        self.timestamp = time.time()
        self.epoch = epoch
        
    
    def sharefile(self):
        try :
            f = open(self.filename,'r')
        except :
            print 'Error : trying to open a non exisiting file named : %r \n try to create it first' % self.filename
        else :
            s = f.read()
            f.close()
            bs = toBin(s)
            Mlist = self.SSS.encode(bs)
            SLM = self.SSS.sharelist(Mlist)
            self.listofsharesofmessages = SLM
        
        
    def rebuildfile(self):
        """
        From the myfile object, produce the original file
        """
        assert self.listofsharesofmessages != []
        
        ML = self.SSS.retrievelist(self.listofsharesofmessages)
        bx = self.SSS.decode(ML)
        sb = toChar(bx)
        
        f = open(self.filename,'w')
        f.write(sb)
        f.close()
    
    def loadSecretSharingSchemefromfile(self):
        f = open(self.filenameofSSS,'r')
        SSS = pickle.load(f)
        self.SSS = SSS
        
    def save(self):
        """
        this wraps the myfile object into a file named 'pointerto'+self.filename
        to avoid saving multiple times unnecesary object, we explicitly do not
        save self.listofsharesofmessages and self.SSS
        """
        assert self.filename != '' # Cannot save a pointer to a blank name
        assert self.filenameofSSS != '' # The pointer must contain the filename of a Secret Sharing Scheme SSS
        pointertomysharedfile = Mysharedfile(self.filename, None, self.filenameofSSS, [], self.epoch)
        s = 'pointerto'+self.filename+'.pointer'
        f = open(s,'w')
        pickle.dump(pointertomysharedfile,f)
        f.close()
        
    def saveShares(self,directoryname, numberofshares = 0):
        """
        This saves the shares into files (using pickles) that are stored into
        ./directory/sharej where j range from 0 to numberofshares
        if numberofshares is default, the number of shares used is n of the Secret Sharing Scheme self.SSS
        """
        SSS = self.SSS
        sList = []
        if numberofshares == 0 :
            n = SSS.n
        else :
            n = numberofshares
        sdir = [0]*n
        try :
            os.mkdir(directoryname)
        except :
            pass #the directory already exists
        for j in range(n) :
            sdir[j] = directoryname+'/shares_of_party_'+str(j)+'/'
            os.mkdir(sdir[j])
        for k in range(len(self.listofsharesofmessages)) :
            sItem = []
            shares_of_message = self.listofsharesofmessages[k]
            for j in range(len(shares_of_message)) :
                share = shares_of_message[j]
                s = sdir[j]+self.filename+'_share_of_msg_'+str(k)+'.share' #TODO: maybe filename should not appear, use (salted) hash somehow?
                f = open(s,'w')
                #pickle.dump(share,f)
                binshare = SSS.shareToBin(share)
                f.write(binshare)
                f.close()
                sItem.append(s)
            sList.append(sItem)
                
        return sList
        
    def rebuilt_listofsharesmessages(self,sList):
        SSS = self.SSS
        LOSM = []
        for sItem in sList:
            LOSMitem = []
            for s in sItem :
                f = open(s,'r')
                #share = pickle.load(f)
                binsharel1 = f.readline()
                binsharel2 = f.readline()
                f.close()
                share = SSS.binToShare(binsharel1,binsharel2)
                LOSMitem.append(share)
            LOSM.append(LOSMitem)
        self.listofsharesofmessages = LOSM
        
    def __str__(self):
        s = 'Pointer to '+self.filename+' created on '+str(time.ctime(self.timestamp))+'\n this pointer uses the SSS '+str(self.SSS)+'\n stored in '+self.filenameofSSS+'\n it also should refresh every '+str(self.epoch)+' seconds'
        return s
        
    def __repr__(self):
        return str(self)
