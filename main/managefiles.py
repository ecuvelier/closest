# -*- coding: utf-8 -*-
"""
Created in 2016

Author : Edouard Cuvelier
Affiliation : Université catholique de Louvain - ICTEAM - UCL Crypto Group
Address : Place du Levant 3, 1348 Louvain-la-Neuve, BELGIUM
email : firstname.lastname@uclouvain.be
"""

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
    
def toBin(s,n):
    """
    turn the character string s into a binary string and pad it with n zeros
    """
    b = ''
    for x in s :
        bx = format(ord(x), 'b').zfill(8)
        b += bx
        
    for i in range(n) :
        b += '0'
        
    return b
    
def toChar(b,n):
    """
    remove the n last bits of b then turn the remaining b into a character chain
    by converting bytes to characters
    """
    
    b = b[:len(b)-n]
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

    
class Myfile:
    
    def __init__(self,f):
        """
        Construct a myfile object from a file f 
        """
        None
        
        
    def tofile(self):
        """
        From the myfile object, produce the original file
        """
    
