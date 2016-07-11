# -*- coding: utf-8 -*-
"""
Created in 2016

Author : Edouard Cuvelier
Affiliation : Université catholique de Louvain - ICTEAM - UCL Crypto Group
Address : Place du Levant 3, 1348 Louvain-la-Neuve, BELGIUM
email : firstname.lastname@uclouvain.be
"""

from field import Field

class SecretSharingScheme:
    """
    SecretSharingScheme is an abstract class defining the formal methods a 
    secret sharing scheme must implement.
    """
        
    def share(self,message):
        raise NotImplementedError('subclasses must override share()!')
    
    def retrieve(self,shareslist):
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
        assert type(p) is int, "p is not an integer: %r" % p
        assert type(t) is int, "t is not an integer: %r" % t
        assert type(n) is int, "n is not an integer: %r" % n
        self.p = p
        assert t<= n, "threshold t must be <= than n"
        assert t>1, "threshold t must be >1: %r" % t
        self.t = t
        self.n = n
        
        self.F = Field(p)
        
        
    
    def share(self,message):
        raise NotImplementedError('subclasses must override share()!')
    
    def retrieve(self,shareslist):
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