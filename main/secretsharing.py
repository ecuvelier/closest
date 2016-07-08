# -*- coding: utf-8 -*-
"""
Created in 2016

Author : Edouard Cuvelier
Affiliation : Université catholique de Louvain - ICTEAM - UCL Crypto Group
Address : Place du Levant 3, 1348 Louvain-la-Neuve, BELGIUM
email : firstname.lastname@uclouvain.be
"""

class SecretSharingScheme:
    """
    SecretSharingScheme is an abstract class defining the formal methods a 
    secret sharing scheme must implement.
    """
    
    def __init__(self):
        
        None
        
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