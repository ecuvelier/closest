# -*- coding: utf-8 -*-
"""
Created in 2016

Author : Edouard Cuvelier
Affiliation : Université catholique de Louvain - ICTEAM - UCL Crypto Group
Address : Place du Levant 3, 1348 Louvain-la-Neuve, BELGIUM
email : firstname.lastname@uclouvain.be
"""

"""
This module handles the pointer version of a file when it is no longer stored
on the device.
"""

class Pointer:
    
    def __init__(self,myf):
        self.filename = ''
        self.filetype = ''
        self.sharingscheme = None # A SecretSharingScheme object
        self.shareslist = [] # A list containing the ids of the shares and their location
        self.timetag = None # The time the tag was created
        self.reshareperiod = None # The intervall of time the shares must be reshared