# -*- coding: utf-8 -*-
"""
Created in 2016

Author : Edouard Cuvelier
Affiliation : Université catholique de Louvain - ICTEAM - UCL Crypto Group
Address : Place du Levant 3, 1348 Louvain-la-Neuve, BELGIUM
email : firstname.lastname@uclouvain.be
"""

"""
This module handles the encoding of a file into the right format (e.g. one or 
several field element) for splitting it into different shares.

It also performs the inverse manipulation.

file <---> format for sharing

"""

class Encoding:
    