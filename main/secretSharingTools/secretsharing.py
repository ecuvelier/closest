# -*- coding: utf-8 -*-
"""
Created in 2016-2017

Author : Edouard Cuvelier
Affiliation : Université catholique de Louvain - ICTEAM - UCL Crypto Group
Address : Place du Levant 3, 1348 Louvain-la-Neuve, BELGIUM
email : firstname.lastname@uclouvain.be
"""

from mathTools.field import Field
from secretSharingTools import managefiles as mf
import pickle

class SecretSharingScheme:
    """
    SecretSharingScheme is an abstract class defining the formal methods a 
    secret sharing scheme must implement.
    """
        
    def share(self,message):
        raise NotImplementedError('subclasses must override share()!')
        
    def sharelist(self,messageslist):
        listofsharesofmessages = []
        for message in messageslist :
            shareslist = self.share(message)
            listofsharesofmessages.append(shareslist)
        return listofsharesofmessages
    
    def retrieve(self,shareslist):
        """
        shareslist is a list of different shares of one message
        """
        raise NotImplementedError('subclasses must override retrieve()!')
        
    def retrievelist(self,listofsharesofmessages):
        """
        listofsharesofmessages contains a list of shares each message, there are
        k messages where k = len(listofsharesofmessages)
        """
        
        messageslist = []
        for shareslist in listofsharesofmessages :
            message = self.retrieve(shareslist)
            messageslist.append(message)
        return messageslist
        
    def resharelist(self,listofsharesofmessages):
        
        new_listofsharesofmessages = []
        for shareslist in listofsharesofmessages :
            #print('sl',shareslist)
            new_shareslist = self.reshare(shareslist)
            new_listofsharesofmessages.append(new_shareslist)
        return new_listofsharesofmessages
        
    def reshare(self,shareslist):
        raise NotImplementedError('subclasses must override reshare()!')
        
    def encode(self,b):
        """
        encode bytes array b into the right format for further sharing
        """
        raise NotImplementedError('subclasses must override encode()!')
        
    def decode(self,m):
        """
        decode m from the sharing format back to the bytes array
        """
        raise NotImplementedError('subclasses must override decode()!')
        
    def shareToBytes(self,share):
        """
        Turn a share into a bytes array
        """
        raise NotImplementedError('subclasses must override shareToBin()!')
        
    def bytesToShare(self,byteshare):
        """
        Turn a bytes array into a share 
        """
        raise NotImplementedError('subclasses must override binToShare()!')
        
    def save(self,filename):
        """
        save the secret sharing scheme into the file 'filename' using pickle
        """
        f = open(filename, 'wb')
        pickle.dump(self,f)
        f.close()
        
    def __str__(self):
        return 'Abstract Secret Sharing Scheme object'
        
    def __repr__(self):
        return str(self)
        
        
class ShamirSecretSharing(SecretSharingScheme):
    
    def __init__(self,F,t,n):
        """
        - F is the prime field used
        - t is the threshold of shares to collect in order to recombine a message
        - n is the number of shares created when sharing a message
        """
        
        assert type(F) is Field
        assert type(t) is int, "t is not an integer: %r" % t
        assert type(n) is int, "n is not an integer: %r" % n
        assert t<= n, "threshold t must be <= than n"
        assert t>1, "threshold t must be >1 %r" % t
        
        self.t = t
        self.n = n
        
        self.F = F
        self.p = F.p # order of F
    
    def share(self,message):
        
        F = self.F
        n = self.n
        t = self.t
        
        Alphas = ()
        '''
        Alphas is a n-uple of random coeficients in F :
        there are the absicesses at which one evaluates the polynom P
        '''
        for i in range(n):
            #alphai = F.random() # in F* (F except 0)
            #Alphas += (alphai,)
            Alphas += (F.elem(i+1),)
            
        A = () # the coefficients of the degree t polynomial P
        for i in range(t-1):
            if i < t-2 :
                ai = F.random(high = self.p) # in F including 0
            else :
                ai = F.random() # in F* (because we want a polynom of degree t)
            A += (ai,)
           
        #print 'A',A
        
        shareslist = []
        for i in range(n):
            Z = F.zero()
            alphai = Alphas[i]
            alphaik = alphai
            for k in range(t-1):
                c = A[k]*(alphaik)
                Z += c
                if k < t-2 :
                    alphaik *= alphai
            #Z = sum(A[k]*(Alphas[i]**(k+1)) for k in range(t))
            si = message + Z # share for party i
            '''
            'si' is the evaluation of polynom P(X) = message + sum_{j=1}^t (aj*X**j)
            in the value X = Alphas[i]
            To open, one must evaluate P(X) in X=0
            '''
            shareslist.append((Alphas[i],si))
            
        return shareslist
    
    def retrieve(self,shareslist):
        F = self.F
        t = self.t
        
        k = len(shareslist)
        
        assert k >= t
        
        S = F.zero()
        for i in range(t):
            P = F.one()
            for j in range(t):
                if i == j:
                    pass
                else :
                    alphai = shareslist[i][0]
                    alphaj = shareslist[j][0]
                    P *= alphaj/(alphaj-alphai)
            si = shareslist[i][1]
            S += si*P
            
        return S
        
        
    def reshare(self,shareslist):
        
        shareslistofzero = self.share(self.F.zero())
        newshareslist = []
        
        for x,y in shareslistofzero :
            for z,w in shareslist :
                #print('here',x,z,x==z,x.val==z.val,x.F==z.F)
                if x == z :
                    
                    newshareslist.append((x,w+y))
                    break
        
        return newshareslist
        
    def encode(self,b):
        """
        encode bytes array b into the right format for further sharing
        """
        
        F = self.F
        
        k = len(b)
        messageslist = []
        
        plp = len(bin(self.p))-2
        blockSize = int(plp/8)-1
        #print('block size :'+ str(blockSize))
        
        pad = k % blockSize
        if pad != 0 :
            '''
            append 0 to b so as it has the desirable length
            '''
            for i in range(blockSize-pad):
                b = b + bytes([0])

        k = len(b)
        #print('k: '+str(k))
        assert k % blockSize == 0
        #nbBlocks = int(k/blockSize)                
        
        T = mf.fromBytestoInt(b,blockSize)
        
        for i in range(len(T)):
            assert T[i]<self.p-1
            m = F.elem(T[i])
            messageslist.append(m)
        
        """
        #DEPRECATED
        
        plp = len(bin(self.p-1))-2
        if typ == 'bin' :
            lp = plp-1 # bit length of p minus 1
        elif typ == 'hex' :
            lp = int(plp/16)
        else :
            lp = 0
        
        index = 0
        
        while index < k :
            ms = s[index:index+lp]
            while len(ms)< lp:
                ms = ms+'0'
            if typ == 'bin' :
                m = F.elem(int(ms,2))
            else :
                m = F.elem(int(ms,16))
            messageslist.append(m)
            index += lp
        """
            
        return messageslist
            
        
    def decode(self,messageslist):
        """
        decode m from the sharing format back to the bytes array
        """
        plp = len(bin(self.p))-2
        blockSize = int(plp/8)-1
        
        T = ()
        for m in messageslist:
            T = T +(m.val,)
        
        return  mf.fromInttoBytes(T,blockSize)
        
        """
        #DEPRECATED
        lp = len(bin(self.p))-3
        s =''
        for m in messageslist:
            ms = bin(m.val)
            sm = ms[2:]
            while len(sm)<lp :
                sm = '0'+sm
            s += sm
            
        return s
        """
        
    def shareToBytes(self, share):
        plp = len(bin(self.p))-2
        blockSize = int(plp/8)
        ai,si = share
        #assert ai.val < self.p-1
        #print(si.val < 256**(blockSize+1))
        #print(blockSize)
        #print(ai.val,si.val)
        
        return mf.fromInttoBytes((ai.val,si.val),blockSize)
        #return bin(ai.val)+'\n'+bin(si.val)
        
    def bytesToShare(self, byteshare ):
        #sbs1 = int(bs1,2)
        #sbs2 = int(bs2,2)
        plp = len(bin(self.p))-2
        blockSize = int(plp/8)
        sai,ssi = mf.fromBytestoInt(byteshare,blockSize)
        ai = self.F.elem(sai)
        si = self.F.elem(ssi)
        return ai,si
        
    def __str__(self):
        return 't-out-of-n Shamir Secret Sharing Scheme with the following parameters:\n Field :'+str(self.F)[:min(10,len(str(self.F)))]+'\n n :'+str(self.n)+'\n t :'+str(self.t)
        