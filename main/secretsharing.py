# -*- coding: utf-8 -*-
"""
Created in 2016

Author : Edouard Cuvelier
Affiliation : Université catholique de Louvain - ICTEAM - UCL Crypto Group
Address : Place du Levant 3, 1348 Louvain-la-Neuve, BELGIUM
email : firstname.lastname@uclouvain.be
"""

from mathTools.field import Field
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
        
    def reshare(self,shareslist):
        raise NotImplementedError('subclasses must override reshare()!')
        
    def encode(self,s):
        """
        encode binary string s into the right format for further sharing
        """
        raise NotImplementedError('subclasses must override encode()!')
        
    def decode(self,m):
        """
        decode m from the sharing format back to the binary string
        """
        raise NotImplementedError('subclasses must override decode()!')
        
    def shareToBin(self,share):
        """
        Turn a share into a binary string
        """
        raise NotImplementedError('subclasses must override shareToBin()!')
        
    def binToShare(self,binshare1,binshare2):
        """
        Turn two binary strings into a share 
        """
        raise NotImplementedError('subclasses must override binToShare()!')
        
    def save(self,filename):
        """
        save the secret sharing scheme into the file 'filename' using pickle
        """
        f = open(filename, 'w')
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
        
        n = self.n
        k = len(shareslist)
        assert k > self.t # Not enough shares to reconstruct the message!
        if k < n :
            print 'Warning : shares missing!\n You might want to rebuild the sharing by trigering retrieve(sharelist)->m then share(m).' #TODO: triggering mechanism? 
        
        shareslistofzero = self.share(self.F.zero())
        newshareslist = []
        
        for x,y in shareslistofzero :
            for z,w in shareslist :
                if x == z :
                    newshareslist.append((x,w+y))
                    break
        
        return newshareslist
        
    def encode(self,s):
        """
        encode binary string s into the right format for further sharing
        """
        F = self.F
        
        k = len(s)
        messageslist = []
        lp = len(bin(self.p))-3 # bit length of p minus 1
        index = 0
        
        while index < k :
            ms = s[index:index+lp]
            while len(ms)< lp:
                ms = ms+'0'
            m = F.elem(int(ms,2))
            messageslist.append(m)
            index += lp
            
        return messageslist
            
        
    def decode(self,messageslist):
        """
        decode m from the sharing format back to the binary string
        """
        lp = len(bin(self.p))-3
        s =''
        for m in messageslist:
            ms = bin(m.val)
            sm = ms[2:]
            while len(sm)<lp :
                sm = '0'+sm
            s += sm
            
        return s
        
    def shareToBin(self, share):
        ai,si = share
        return bin(ai.val)+'\n'+bin(si.val)
        
    def binToShare(self, bs1,bs2 ):
        sbs1 = int(bs1,2)
        sbs2 = int(bs2,2)
        ai = self.F.elem(sbs1)
        si = self.F.elem(sbs2)
        return ai,si
        
    def __str__(self):
        return 't-out-of-n Shamir Secret Sharing Scheme with the following parameters:\n Field :'+str(self.F)+'\n n :'+str(self.n)+'\n t :'+str(self.t)