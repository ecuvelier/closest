# -*- coding: utf-8 -*-
"""
Created in 2016

Author : Edouard Cuvelier
Affiliation : Université catholique de Louvain - ICTEAM - UCL Crypto Group
Address : Place du Levant 3, 1348 Louvain-la-Neuve, BELGIUM
email : firstname.lastname@uclouvain.be
"""

from mathTools.field import Field
import gmpy

class SecretSharingScheme:
    """
    SecretSharingScheme is an abstract class defining the formal methods a 
    secret sharing scheme must implement.
    """
        
    def share(self,message):
        raise NotImplementedError('subclasses must override share()!')
    
    def retrieve(self,shareslist):
        """
        shareslist is a list of different shares
        """
        raise NotImplementedError('subclasses must override retrieve()!')
        
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
        
        
class ShamirSecretSharing(SecretSharingScheme):
    
    def __init__(self,p,t,n):
        """
        - p is the size of the prime field used
        - t is the threshold of shares to collect in order to recombine a message
        - n is the number of shares created when sharing a message
        """
        assert (type(p) is int) or (type(p) == type(gmpy.mpz(0))), "p is not an integer: %r" % p
        assert type(t) is int, "t is not an integer: %r" % t
        assert type(n) is int, "n is not an integer: %r" % n
        self.p = p
        assert t<= n, "threshold t must be <= than n"
        assert t>1, "threshold t must be >1 %r" % t
        self.t = t
        self.n = n
        
        self.F = Field(p)
        
        
    
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
           
        print 'A',A
        
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
        assert k > self.t
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
        lp = len(bin(self.p))-2 # bit length of p
        assert k % (lp-1) == 0 # k must be a multiple of the binary lenght of p, minus 1 (in order to avoid overflow)
        d = k/(lp-1) # number of blocks of size lp into k
        
        index = 0
        for i in range(d):
            ms = s[index:index+lp]
            m = F.elem(int(ms))
            messageslist.append(m)
            index += lp
            
        return messageslist
            
        
    def decode(self,messageslist):
        """
        decode m from the sharing format back to the binary string
        """
        s =''
        for m in messageslist:
            ms = bin(m.val)
            s += ms[2:]
            
        return s