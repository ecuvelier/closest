# -*- coding: utf-8 -*-
"""
Created on 2013-2014

Author : Edouard Cuvelier
Affiliation : Université catholique de Louvain - ICTEAM - UCL Crypto Group
Address : Place du Levant 3, 1348 Louvain-la-Neuve, BELGIUM
email : firstname.lastname@uclouvain.be
"""

from numpy import *
import gmpy2 as gmpy
#from Crypto.Random.random import randint
from binascii import hexlify
import os
import tools.fingexp as fingexp
import tools.utils as utils

#TODO : clean this module to keep only needed elements

def myrandom(a,b):
    """
    return a random number between a and b
    """
    c = b-a
    l = int(((len(bin(c))-2)/8))
    r = int(hexlify(os.urandom(max(l,128))),16)%(c+1)
    assert a+r<=b
    return a+r


class Field(fingexp.FingExp):
    'Class for Field'

    def __init__(self,p):
        '''Defines the modulus p which must be a prime
        '''
        self.F = self
        self.p = gmpy.mpz(p) # prime modulus
        #self.char = self.p # characteristic
        #self.q = self.p+1 # order+1 #TODO : correct?
        assert gmpy.is_prime(p)
        #self.rep = None
        self.g = None
        '''
        g is a random quadratic residue used to compute square roots and it is
        initialized the first time a square root is computed
        '''

        self.to_fingerprint = ["p"]
        self.to_export = {"fingerprint": [],"value": ["p"]}
        super(Field, self).__init__()

    def load(self, data, fingerprints):
        self.p = utils.b64tompz(data["p"])

    def one(self):
        'unit element for multiplication'
        return FieldElem(1, self)

    def zero(self):
        'unit element for addition'
        return FieldElem(0,self)

    def elem(self,x):
        ''' return an element of value x
        '''
        if isinstance(x,FieldElem):
            assert x.F == self
            return x
        m = gmpy.mpz(1)
        assert isinstance(x,int) or isinstance(x, long) or type(x)==type(m)
        return FieldElem(x,self)

    def random(self,low=1,high=None):
        ''' Return a random element of the Field except 0
        '''
        if high == None :
            high = int(self.p-1)
        rand = myrandom(int(low),int(high))
        return self.elem(rand)

    def __eq__(self, other):
        'testing if we are working in the same field'
        try:
            return (self.p == other.p)
        except:
            return False

    def add(self, a, b):
        '''
        field operation: addition mod p
        '''
        return FieldElem((a.val + b.val) % self.p, self)

    def sub(self, a, b):
        '''
        field operation: substraction mod p
        '''
        return FieldElem((a.val - b.val) % self.p, self)

    def neg(self, a):
        '''
        field operation: opposite mod p
        '''
        return FieldElem((self.p - a.val ) % self.p, self)

    def mul(self, a, b):
        '''
        field operation: multiplication of field elements
        '''
        """
        if isinstance(a,FieldElem) and isinstance(b, FieldElem) and not a.F == b.F :
            raise Exception("multiplication between elements of different fields")
        """
        if not isinstance(b,FieldElem) :
            # Multiplication by a scalar
            if b<0:
                return self.smul(-a,-b)
            return self.smul(a,b)
        else:
            return self.pmul(a,b)

    def smul(self,a,b):
        ''' Return a*b where a or b is scalar
        '''
        if not isinstance(b,FieldElem):
            # b is scalar
            #return self.dbleAndAdd(a,a,b)
            return FieldElem((gmpy.mpz(b)*a.val)%(self.p),self)
            #return self.pmul(a,a.F.elem(b))
        else :
            # a is scalar
            #return self.dbleAndAdd(b,b,a)
            return self.smul(b,a)
    def sm(self,b,a):
        ''' Quick multiplication between a field element a and a scalar b
        '''
        return FieldElem((gmpy.mpz(b)*a.val)%(self.p),self)

    def pmul(self,a,b):
        ''' product between two field element in Fp
        '''
        return FieldElem((a.val * b.val) % self.p, self)

    def dbleAndAdd(self,P,Pp,n):
        'return n*P using double and add technique'
        #print "dblaad"
        if n == 0 :
            return self.zero();
        if n == 1 :
            return P
        elif n%2 == 1 :
            Q = self.dbleAndAdd(P,Pp,(n-1)/2)
            return P+Q+Q
        elif n%2 == 0 :
            Q = self.dbleAndAdd(P,Pp,n/2)
            return Q+Q

    def powop(self, a, b):
        'return a**b'
        m = gmpy.mpz(1)
        #self.count = 0
        'exponentiation by a scalar'
        if not isinstance(b, int) and not isinstance(b, long) and not type(b)==type(m):
            raise Exception("Exponentation by a non integer, long or mpz")
        c = b
        '''
        if c > self.char-1 or c<0:
            c = b%(self.char-1)
        '''
        #elif :
        #    return self.powop(a.invert(),(-c))
        if c == 0 :
            assert not a.val == 0
            return self.one()
        elif c == 1 :
            return a
        else :
            return self.sqrtAndMultply(a,a, c)
            #return FieldElem(pow(a.val,b,self.char))

    def sqrtAndMultply(self,P,Pp,n):
        'return P**n using square and multiply technique'
        if n == 0 :
            return self.one()
        elif n == 1 :
            return P
        elif n%2 == 1 :
            Q = self.sqrtAndMultply(P,Pp,(n-1)/2)
            return P*self.square(Q)
        elif n%2 == 0 :
            Q = self.sqrtAndMultply(P,Pp,n/2)
            return self.square(Q)

    def square(self,a):
        '''
        This method returns the square of a
        '''
        return FieldElem(pow(a.val,2, self.p), self)

    def invert(self,a):
        assert not (a.val%self.p == 0) # Do not invert zero!
        return FieldElem(gmpy.invert(a.val, self.p), self)

    #def invertible(self,a):
        #return not int(a.invert().val) == 0

    def div(self,a,b):
        assert not (b.val%self.p == 0) # Do not invert zero!
        return FieldElem((a.val*self.invert(b).val % self.p),self)

    def findnonresidue(self):
        '''
        find a random non quadratic residue in the Field F,
        that is, find g that is not a square in F, this is
        needed to compute square roots
        '''
        g=self.random()
        while g.isquadres():
            #print g, " is quad res in ", self
            g = self.random()
        return g

    def __str__(self):
        return "F_"+str(self.p)

    def jsonable(self):
        return {'type': 'FqField', 'p': self.p}


class FieldElem():
    def __init__(self, val, F):
        '''Creating a new field element.
        '''
        #assert isinstance(F,Field)
        self.F = F
        self.val = gmpy.mpz(val)
        #self.poly = polynom(self.F,[self])

        #self.to_fingerprint = ["F", "val"]
        #self.to_export = {"fingerprint": ["F"],
        #                  "value": ["val"]}
        #super(FieldElem, self).__init__()

    def __eq__(self, other):
        try:
            return (self.val == other.val and self.F == other.F)
        except:
            return False

    def __add__(self, other):
        return self.F.add(self, other)

    def __neg__(self):
        return self.F.neg(self)

    def __sub__(self, other):
        return self.F.sub(self, other)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        return self.F.mul(self, other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, e):
        return self.F.powop(self, e)

    def __div__(self,other):
        return self.F.div(self,other)

    def __truediv__(self,other):
        return self.F.div(self,other)

    def __str__(self):
        return str(self.val)
        
    def __repr__(self):
        return str(self.val)

    def iszero(self):
        return self == self.F.zero()

    def invert(self):
        return self.F.invert(self)

    def invertible(self):
        return self.F.invertible(self)

    def isquadres(self):
        ''' This method return True if the element is a quadratic residue mod q
            different than zero
            it returns False otherwhise
        '''
        if (self+self.F.zero()).iszero() :
            # case of element is zero
            return False
        else :
            # If F's order is prime we use Euler's criterium
            c = self**((self.F.q-1)/2) #TODO: Optimize this
            return c==self.F.one()

    def squareroot(self):
        ''' This method returns the positive square root of
            an element of the field
            using the Tonelli-Shanks algorithm

            Carefull : if the element has no square root, the method does not
            check this case and raises an error. Verification has to be done
            before calling the method.
        '''
        g = self.F.g
        if g == None :
            g = self.F.findnonresidue()
            self.F.g = g

        q = self.F.q

        s=0
        t=self.F.q-1
        while t%2==0:
            s=s+1
            t=t/2
        # q-1 = (2**s)*t

        e = 0
        for i in range(2,s+1):
            b = 2**(i-1)
            b1 = b*2   # b1 = 2**i
            c = ((self)*(g**(-e)))**((q-1)/b1)
            if not c==self.F.one() :
                e = e+b
        h = self*(g**(-e))
        b = (g**(e/2))*(h**((t+1)/2))
        assert b**2 == self # FAILURE to find square root
        return b

    def fingerprint(self):
        return fingexp.fingerprint(self.val)

    def jsonable(self):
        return {'type': 'FieldElem', 'F': self.F, 'val': self.val}

"""
class ExtensionField(Field):
    '''
    This class defines extension fields and inherits field methods.
    Depending on the degree of the extension field, we use
    different algorithms to optimize the operations
    '''
    def __init__(self,F,irpoly,g=None,rep=None):
        '''Define the base Field or extension Field and the irreducible polynomial
           F is the base field on top of which the extension
        field is built
           irpoly is the irreducible polynomial used to build
        the extension field as F/irpoly
           g is a non quadratic residue used to compute square
        roots, if it is set to None, computing a square root
        will initialize g
           rep is the representation of the root of irpoly
        (note that letter 'A' is reserved for the Complex extension field)
        '''
        self.F = F
        self.irpoly = irpoly
        self.deg = len(irpoly.coef) # degree of the irreducible polynomial + 1
        assert self.deg > 0
        self.q = self.F.q**(self.deg-1) # order of the Field

        self.tabular = self.table()

        if rep == None :
            self.rep = rd.choice(['B','C','D','E','F','G','H','J','K','L'])
            #Choose a random representation letter
        else :
            self.rep = rep

        self.char = F.char

        self.primefield = gmpy.is_prime(self.char)

        self.g = g # g is needed to compute square roots, it is a non quadratic residue

        self.to_fingerprint = ["F","irpoly"]
        self.to_export = {"fingerprint": [],"value": ["F","irpoly"]}

    def one(self):
        'unit element for multiplication'
        One = [self.F.zero()]*(self.deg-1)
        One[self.deg-2]= self.F.one()
        return ExtensionFieldElem(self,polynom(self.F,One))

    def zero(self):
        'unit element for addition'
        Zero = [self.F.zero()]*(self.deg-1)
        return ExtensionFieldElem(self,polynom(self.F,Zero))

    def unit(self):
        ''' root of the irreducible polynomial
        e.g. return element 1*A+0 (or the complex value i) if the irpoly is X**2+1
        '''
        I = self.zero()
        I.poly.coef[-2]=self.F.one()
        return I

    def elem(self,x):
        ''' Provided that x belongs to F, return an element of the extension field
            of value x
        '''
        P = self.zero()
        P.poly.coef[-1] = x
        return P

    def random(self):
        ''' Return a random element of the Extension Field
        '''
        polycoef = [0]*(self.deg-1)
        for i in range(self.deg-1):
            polycoef[i] = self.F.random()
        poly = polynom(self.F,polycoef)
        return ExtensionFieldElem(self,poly)

    def __eq__(self, other):
        'testing if we are working in the same extension field'
        try:
            return (self.F == other.F and self.irpoly == other.irpoly)
        except:
            return False

    def add(self, a, b):
        '''
        field operation: addition of polynomial > addition of coefficients in the appropriate field
        '''
        #assert a.F == b.F  and a.F.F == self.F
        if not a.deg == b.deg :
            a = self.reduc(a)
            b = self.reduc(b)
        polysum = [0]*a.deg
        for i in range(a.deg):
            polysum[i]=a.poly.coef[i]+b.poly.coef[i]
        P = polynom(self.F,polysum)
        return ExtensionFieldElem(self,P)

    def sub(self, a, b):
        '''
        field operation: substraction of polynomials > substraction of each coefficient in the appropriate field
        '''
        #assert a.F == b.F and a.F.F == self.F
        if not a.deg == b.deg :
            a = self.reduc(a)
            b = self.reduc(b)
        c = self.neg(b)
        return self.add(a,c)

    def neg(self, a):
        '''
        field operation: opposite of a polynomial > opposite of each coefficient in appropriate field
        '''
        #assert a.F.F == self.F
        ap = [0]*a.deg
        for i in range(a.deg):
            ap[i] = -a.poly.coef[i]
        P = polynom(self.F,ap)
        return ExtensionFieldElem(self,P)

    def smul(self,a,b):
        ''' Return a*b where a or b is scalar
        '''
        if not isinstance(b,FieldElem):
            # b is scalar
            A = a.poly.coef
            Pc = [0]*len(A)
            for i in range(len(Pc)):
                Pc[i] = A[i]*gmpy.mpz(b)
            return ExtensionFieldElem(self,polynom(self.F,Pc))
        else :
            # a is scalar
            return self.smul(b,a)

    def pmul(self,a,b):
        '''Multiplication between polynomials
        '''
        #assert a.F == b.F and a.F.F == self.F
        if not a.deg == b.deg :
            a = self.reduc(a)
            b = self.reduc(b)
        # Simpler notations for reading
        A = a.poly.coef
        B = b.poly.coef

        k = self.deg-1 # degree of the externsion field
        if k == 2 and self.F.rep =='A':
            # We are in the case that the extension field is Fp2
            # We assume here that the irreductible polynom is X**2+1 (beta=-1)
            # Complex multiplication
            a0,a1,b0,b1 = A[0].val,A[1].val,B[0].val,B[1].val
            p = self.char
            v0 = a0*b0
            v1 = a1*b1
            c0 = ((a0+a1)*(b0+b1)-v0-v1)%p
            c1 = (v1-v0)%p
            c0e = FieldElem(c0,self.F)
            c1e = FieldElem(c1,self.F)
            cp = polynom(self.F,[c0e,c1e])
            C = ExtensionFieldElem(self,cp)
            return C
        elif k == 2:
            # In this case, use Karatsuba multiplication algorithm
            # notations
            a0 = A[0]
            a1 = A[1]
            b0 = B[0]
            b1 = B[1]
            beta = -self.irpoly.coef[-1]

            v0 = self.F.pmul(a0,b0)
            v1 = self.F.pmul(a1,b1)
            c0 = self.F.pmul((a0+a1),(b0+b1))-v0-v1 # coefficient of X
            c1 = v1 + self.F.pmul(v0,beta) # independant term
            cp = polynom(self.F,[c0,c1])
            C = ExtensionFieldElem(self,cp)
            return C
        elif k == 3:
            # In this case, use Karatsuba multiplication algorithm
            # notations
            a0,a1,a2 = A
            b0,b1,b2 = B
            beta = -self.irpoly.coef[-1]

            v0,v1,v2 = self.F.pmul(a0,b0), self.F.pmul(a1,b1), self.F.pmul(a2,b2)
            c0 = self.F.pmul((a0+a2),(b0+b2))-v0+v1-v2  # coefficient of X**2
            c1 = self.F.pmul((a2+a1),(b2+b1))-v2-v1+self.F.pmul(beta,v0) # coefficient of X
            c2 = v2+self.F.pmul(beta,(self.F.pmul((a1+a0),(b1+b0))-v1-v0)) # independant term
            cp = polynom(self.F,[c0,c1,c2])
            C = ExtensionFieldElem(self,cp)
            return C

        else :
           prod = convolve(A,B)
           return self.reduc2(prod) # return EProd % ired. polynomial

    def square(self,a):
        ''' This algortihm returns the square of a in the field
            using different methods if the degree of the extension
            is 2,3 or more
        '''
        #print a.F
        #print self
        assert a.F == self

        if not a.deg == self.deg-1 :
            a = self.reduc(a)
        #notations
        A = a.poly.coef
        k = self.deg-1 # degree of the extension

        if k == 2 and self.F.rep == 'A':
            # Using the complex multiplication
            # We are in the case that the extension field is Fp2
            # We assume here that the irreductible polynom is X**2+1 (beta=-1)
            a1, a0 = A[0].val,A[1].val
            p = self.char
            v0 = a0*a1
            c0 = ((a0+a1)*(a0-a1))%p
            c1 = (v0+v0)%p
            c0e = FieldElem(c0,self.F)
            c1e = FieldElem(c1,self.F)
            cp = polynom(self.F,[c1e,c0e])
            C = ExtensionFieldElem(self,cp)
            return C
        elif k == 2:
            # Using the complex multiplication
            a1, a0 = A
            beta = -self.irpoly.coef[-1]
            v0 = self.F.pmul(a0,a1)
            c0 = self.F.pmul((a0+a1),(a0+self.F.pmul(a1,beta)))-v0-self.F.pmul(beta,v0)
            c1 = v0+v0
            cp = polynom(self.F,[c1,c0])
            return ExtensionFieldElem(self,cp)

        elif k == 3:
            # Using Chung-Hasan Squaring2
            a2,a1,a0 = A
            #print a0
            #print 'a0',a0.F, a0.F.deg-1
            #print 'self',self.F, self.F.deg-1
            assert a0.F == self.F
            beta = -self.irpoly.coef[-1]
            s0 = self.F.square(a0)
            t1 = self.F.pmul(a0,a1)
            s1 = t1+t1
            s2 = self.F.square((a0-a1+a2))
            t3 = a1*a2
            s3 = t3+t3
            s4 = self.F.square(a2)

            c0 = s0 + self.F.pmul(beta,s3)
            c1 = s1 + self.F.pmul(beta,s4)
            c2 = s1 + s2 + s3 - s0 -s4
            cp = polynom(self.F,[c2,c1,c0])
            return ExtensionFieldElem(self,cp)

        else :
            return self.F.pmul(a,a)

    def invert(self,a):
        ''' Ths method returns the inverse of a in the field
            The inverse is computed by determining the Bezout coefficient using the
            extended Euclide's algorithm or by specialized algorithms depending
            on the degree of the extension (2 or 3)
        '''
        #assert self.invertible(a) #The element must be invertible
        assert a.F == self
        k = self.deg-1
        if k == 2 and self.F.rep == 'A':
            # inversion in a field of characteristic 2 over prime field
            # We are in the case that the extension field is Fp2
            # We assume here that the irreductible polynom is X**2+1 (mod=-1)
            A = a.poly.coef
            a1,a0 = A[0].val,A[1].val # a = a0+a1*i
            p = self.char

            norm = a0*a0+a1*a1
            invnorm = gmpy.invert(norm,p)
            c0 = (a0*invnorm) % p
            c1 = (-a1*invnorm) % p
            c0e = FieldElem(c0,self.F)
            c1e = FieldElem(c1,self.F)
            invap = polynom(self.F,[c1e,c0e])
            inva = ExtensionFieldElem(self,invap)
            return inva

        elif k == 2 :
            # inversion in a field of characteristic 2 over prime field
            A = a.poly.coef
            a1,a0 = A[0],A[1] # a = a0+a1*i
            #print 'A',A
            #print 'a1',a1
            mod = self.irpoly.coef[-1] # i**2 = -mod
            #a1b,a0b,modb = self.F.elem(a1), self.F.elem(a0),self.F.elem(mod)
            #print 'a1b',a1b
            #a1b2 = self.F.square(a1b)
            a12 = self.F.square(a1)
            #mid = self.F.pmul(a1b2,modb)
            mid = self.F.pmul(a12,mod)
            #norm = self.F.square(a0b)+mid
            norm = self.F.square(a0)+mid
            #invnorm = self.F.invert(a0**2+mod*a1**2)
            #invnorm = self.F.invert(norm.poly.coef[-1])
            invnorm = self.F.invert(norm)
            c = self.F.pmul(a0,invnorm) # c = -a1/(a0**2+mod*a1**2)
            d = -self.F.pmul(a1,invnorm)
            invap = polynom(self.F,[d,c])
            inva = ExtensionFieldElem(self,invap)
            return inva

        elif k == 3 :
            # inversion in char. 3 field
            A = a.poly.coef
            a2,a1,a0 = A[0],A[1],A[2]
            mod = -self.irpoly.coef[-1]
            z0 = self.F.zero()
            z1 = self.F.one()
            if a0 == z0:
                #a0 = 0
                if a1 == z0:
                    #a1 = 0
                    c0,c1,c2 = z0, self.F.invert(self.F.pmul(a2,mod)), z0
                elif a2 == z0:
                    #a2 = 0
                    c0,c1,c2 = z0,z0,self.F.invert(self.F.pmul(a1,mod))
                else :
                    #a1,a2 != 0
                    a22 = self.F.square(a2)
                    a12 = self.F.square(a1)
                    c2 = self.F.pmul(a12,self.F.invert((self.F.pmul(self.F.pmul(a22,a2),mod)+self.F.pmul(self.F.pmul(a12,a1),mod))))
                    c1 = self.F.pmul((z1-self.F.pmul(self.F.pmul(a1,c2),mod)),self.F.invert(self.F.pmul(a2,mod)))
                    c0 = self.F.pmul((-(self.F.pmul(self.F.pmul(a2,mod),c2))),self.F.invert(a1))
            else :
                #a0 != 0
                if a1 == z0 and a2 == z0:
                    #a1 = 0 , a2 = 0
                    c0,c1,c2 = self.F.invert(a0),z0,z0
                else :
                    a12 = self.F.pmul(a1,a2)
                    a12m = self.F.pmul(a12,mod)
                    a00 = self.F.square(a0)
                    abis = a00-a12m

                    if abis == z0:
                        #a0**2-(a1*a2*mod) = 0
                        a11 = self.F.square(a1)
                        a22 = self.F.square(a2)
                        a02 = self.F.pmul(a0,a2)
                        a01 = self.F.pmul(a0,a1)
                        c2 = self.F.pmul(-a,self.F.invert(self.F.pmul((a02-a11),mod)))
                        c1 = self.F.pmul(-a2,self.F.invert(a01-self.F.pmul(a22,mod)))
                        a1c2 = self.F.pmul(a1,c2)
                        a2c1 = self.F.pmul(a2,c1)
                        c0 = self.F.pmul((z1-self.F.pmul(a1c2+a2c1,mod)),self.F.invert(a0))
                    else :
                        #a0**2-(a1*a2*mod) != 0
                        if a1 == z0:
                            #a1 = 0

                            inva0 = self.F.invert(a0)
                            a02 = self.F.pmul(a0,a2)
                            a000 = self.F.pmul(a00,a0)
                            a22 = self.F.square(a2)
                            a222 = self.F.pmul(a22,a2)
                            mm = self.F.square(mod)
                            a222mm = self.F.pmul(a222,mm)

                            c2 = self.F.pmul(-a02,self.F.invert(a000+a222mm))

                            a02m = self.F.pmul(a02,mod)
                            a02mc2 = self.F.pmul(a02m,c2)
                            inva00 = self.F.square(inva0)

                            c1 = self.F.pmul(-a02mc2,inva00)

                            a2m = self.F.pmul(a2,mod)
                            a2mc1 = self.F.pmul(a2m,c1)

                            c0 = self.F.pmul(z1-a2mc1,inva0)
                        elif a2 == z0:
                            #a2 = 0
                            a11 = self.F.square(a1)
                            a111 = self.F.pmul(a11,a1)
                            a000 = self.F.pmul(a00,a0)
                            a111m = self.F.pmul(a111,mod)
                            inva0 = self.F.invert(a0)

                            c2 = self.F.pmul(a11,self.F.invert(a111m+a000))

                            a11m = self.F.pmul(a11,mod)
                            a11mc2 = self.F.pmul(a11m,c2)
                            inva00 = self.F.square(inva0)

                            c1 = self.F.pmul(a11mc2-a1,inva00)

                            a1m = self.F.pmul(a1,mod)
                            a1mc2 = self.F.pmul(a1m,c2)

                            c0 = self.F.pmul(z1-a1mc2,inva0)
                        else :
                            #a1,a2 != 0
                            a01 = self.F.pmul(a0,a1)
                            a22 = self.F.square(a2)
                            a22m = self.F.pmul(a22,mod)
                            a02 = self.F.pmul(a0,a2)
                            a11 = self.F.square(a1)
                            abus = a01-a22m
                            abos = self.F.pmul(a02-a11,mod)
                            invabis = self.F.invert(abis)
                            abb = self.F.pmul(abus,invabis)
                            abb1 = self.F.pmul(abb,a1)
                            abbbos = self.F.pmul(abb,abos)

                            c2 = self.F.pmul(abb1-a2,self.F.invert(abis-abbbos))

                            abosc2 = self.F.pmul(abos,c2)

                            c1 = self.F.pmul(-a1-abosc2,invabis)
                            a1c2 = self.F.pmul(a1,c2)
                            a2c1 = self.F.pmul(a2,c1)

                            c0 = self.F.pmul(z1-self.F.pmul(a1c2+a2c1,mod),self.F.invert(a0))

            invap = polynom(self.F,[c2,c1,c0])
            inva = ExtensionFieldElem(self,invap)
            return inva


        else :
            # inversion in a field of char. != 2,3
            # this inversion takes a longer time (than previous method)
            # it uses extended Euclid's algorithm
            P = ExtensionFieldElem(self,self.irpoly)
            r,u,v = self.extendedeuclide(P,a)
            n,d = r.poly.truedeg()
            assert n == self.deg-2
            c = r.poly.coef[len(r.poly.coef)-1].invert()
            cp = polynom(self.F,[c])
            ce = ExtensionFieldElem(self,cp)
            return ce*v

    def invertible(self,a):
        ''' Return True if a is invertible
        '''
        return not self.reduc(a)==self.zero()

    def div(self,a,b):
        return a*self.invert(b)

    def eucldiv(self,a,b):
        ''' Return a/b and a%b
            a and b are of length d-1 where d is the degree of the irreducible polynomial
        '''
        zero = self.F.zero()
        izero = self.zero()
        d = self.deg
        assert not b.poly.iszero() # Do not divide by zero

        if a.poly.iszero() :
            return izero, izero # quotient is zero, remain is zero
        elif a == b:
            return self.one(), izero # quotient is one, remain is zero

        #Notations
        A = a.poly.coef
        B = b.poly.coef
        n, da = a.poly.truedeg() # position of first non zero elem of a and degree of a
        m, db = b.poly.truedeg() # same for b

        if da<db :
            #  deg(a)<deg(b)
            return izero, a # quotient is zero, remain is a
        elif da==db:
            #deg(a)=deg(b)
            deg = max(d-1,da)
            rc = [zero]*(deg)
            qc = [zero]*(deg)
            q = A[n]/B[m]
            for i in range(1,deg):
                rc[i] = A[n+i]-q*B[m+i]
            qc[deg-1] = q

            rp = polynom(self.F,rc)
            qp = polynom(self.F,qc)
            remain = ExtensionFieldElem(self,rp)
            quotient = ExtensionFieldElem(self,qp)

            return quotient, remain
        else :
            # deg(a)>deg(b)
            deg = max(d-1,da)
            p = deg - da
            rc = [zero]*(deg)
            qc = [zero]*(deg)
            rc[deg-da:] = A[n:]
            pm=0
            while p+pm+db<deg+1:
                #k is the position of the index of the quotient
                k = deg-(da-db)-1+pm
                qc[k] = rc[p+pm]/B[m]
                for i in range(db):
                    rc[i+p+pm] = rc[i+p+pm]- qc[k]*B[m+i]
                pm=pm+1

            rp = polynom(self.F,rc)
            qp = polynom(self.F,qc)
            remain = ExtensionFieldElem(self,rp)
            quotient = ExtensionFieldElem(self,qp)

            return quotient, remain

    def reduc(self,a):
        ''' Return a % self.irpoly
        The polynomial a = [a_0,...,a_n-1] is returned modulo the irreducible polynomial
        The reduced polynomial has length at most d-1 where d is the length
        of the irreducible polynomial
        '''
        assert a.F.F == self.F

        if a.poly.iszero() :
            return self.zero()
        elif a.poly == self.irpoly :
            return self.zero()
        elif a.deg < self.deg :
            c = [self.F.zero()]*(self.deg-1-a.deg)
            newacoef = c+a.poly.coef
            newapoly= polynom(self.F, newacoef)
            newaelem = ExtensionFieldElem(self, newapoly)
            return newaelem
        else :
            # Case where a is not zero or the irreducible polynomial and deg(a)>=deg(irpoly)
            q,r = self.eucldiv(a,ExtensionFieldElem(self,self.irpoly))
            r = self.trunc(r)
            return self.reduc(r)

    def reduc2(self,a):
        ''' a is a list of length (d-1)*2-1 (polynomial length)
            this method returns the equivalent element of length d-1
            using the table of equivalences (build from the irreducible polynomial)
            in the function self.table()
        '''
        As = a[:(self.deg-2)]
        Ad = a[(self.deg-2):]
        b = list(dot(As,self.tabular)+Ad)
        newapoly = polynom(self.F,b)
        newa = ExtensionFieldElem(self,newapoly)
        return newa

    def trunc(self,a):
        '''Return an ExtensionFieldElem of length d-1 where d = deg(irpoly)
        '''
        d = self.deg
        if a.deg == d-1:
            return a
        c = a.poly.coef[a.deg-d+1:] # the (d-1) last elements of a
        cp = polynom(self.F,c)
        return ExtensionFieldElem(self,cp)

    def table(self):
        ''' This method returns a table (usually) stored in self.tabular
           which is used to compute reduction after a multiplication
           between two elements
        '''
        d = self.deg
        T = zeros((d-2,d-1),dtype=object_)
        Pc = self.irpoly.coef[1:]

        for i in range(0,d-2):
           Qc = [self.F.zero()]*(2*(d-1)-1)
           Qc[i+1:i+d] = Pc
           Qp = polynom(self.F,Qc)
           Qe = ExtensionFieldElem(self,Qp)
           Q = self.reduc(-Qe)
           T[i] = array(Q.poly.coef)
        return T

    def extendedeuclide(self,a,b):
        '''Return s,u,v such as s = ua + vb, s is the gcd of a and b
        This method is used to compute the inverse of a mod b (when s=1)
        '''
        #init
        one = self.one()
        zero = self.zero()
        s = a
        u = one
        v = zero
        sp = b
        up = zero
        vp =  one
        #loop : invariants are s = ua+vb and sp = up*a+vp*b
        while not sp.poly.iszero() :
            q,r = self.eucldiv(s,sp)
            s,u,v,sp,up,vp = sp, up, vp, r, u-up*q,v-vp*q

        return self.reduc(s),self.reduc(u),self.reduc(v)

    def __str__(self):
        return str(self.F)+"/"+str(self.irpoly)

    def jsonable(self):
        return {'type': 'Field Extension', 'F': self.F, 'irpoly': self.irpoly, 'degree':self.deg-1}

class ExtensionFieldElem(FieldElem):

    def __init__(self,F,poly):
        '''Define the Extension Field and the representative polynomial
        '''
        self.F = F
        self.poly = poly
        self.siz = len(poly.coef)
        self.deg = self.siz

    def __str__(self):
        x = self.F.rep
        p = self.poly
        s = '('
        if self.siz == 1 :
            s = s+str(p.coef[0])
        if self.siz == 2 :
            s = s+str(p.coef[0])+'*'+x+' + '+str(p.coef[1])
        if self.siz > 2 :
            s =s+str(p.coef[0])+'*'+x+'**'+str(self.siz-1)
            for i in range(1,self.siz-2):
                s = s+' + '+str(p.coef[i])+'*'+x+'**'+str(self.siz-1-i)
            s = s+' + '+str(p.coef[self.siz-2])+'*'+x +' + '+str(p.coef[self.siz-1])
        return s+')'

    def __eq__(self,other):
        try:
            return self.F == other.F and self.poly == other.poly
        except:
            return False

    def fingerprint(self):
        return self.poly.fingerprint()


    def jsonable(self):
        return {'type': 'ExtensionFieldElem', 'F': self.F, 'poly': self.poly, 'size': self.siz}

class polynom:
    ''' This class represents a polynomial written P = c_nX**n+...c_1X+c_0
        c_0,...,c_n are in the Field F (which can be an ExtensionField) so they are either FieldElem or ExtensionFieldElem
        coef is a list : coef = [c_n,...,c_0] of length n+1
    '''
    def __init__(self,F,coef):
        self.F = F # The field in which coeficients belong
        if isinstance(coef,list):
            self.coef = coef # A list of coeficient in decreasing order (by convention) of the polynomial's degree
            self.deg = len(coef) # The degree+1 of the polynomial
        else :
            #coef is not a list but a single element
            self.coef = [coef]
            self.deg = 1

    def __eq__(self,other):
        try:
            return (self.F == other.F and self.coef == other.coef)
        except:
            return False

    def __str__(self):
        # Not consistent with representation letter of the fields
        x = self.F.rep
        if x == None:
            x = 'X'
        s = '('
        if self.deg == 1 :
            s = s+str(self.coef[0])
        if self.deg == 2 :
            s = s+str(self.coef[0])+'*'+x+' + '+str(self.coef[1])
        if self.deg > 2 :
            s =s+str(self.coef[0])+'*'+x+'**'+str(self.deg-1)
            for i in range(1,self.deg-2):
                s = s+' + '+str(self.coef[i])+'*'+x+'**'+str(self.deg-1-i)
            s = s+' + '+str(self.coef[self.deg-2])+'*'+x +' + '+str(self.coef[self.deg-1])
        return s+')'

    def fingerprint(self):
        L = []
        for c in self.coef:
            L.append(c.fingerprint())
        return fingexp.fingerprint(L)

    def iszero(self):
        '''Return True if it is a zero polynomial (each coefficient is zero)
           This does not return True if the polynomial is the polynomial that generates the extension field
        '''
        cond = True
        for i in self.coef:
            pcond = i.iszero()
            cond = pcond*cond
        return cond

    def truedeg(self):
        '''Return the position of the first non zero coefficient and the actual degree of the polynomial
        '''
        if self.iszero():
            return 0,0
        n = 0
        while self.coef[n]==self.F.zero():
            n = n+1
        # n  is the position of the first non zero coeff of the polynomial
        return n, self.deg-n  # position and actual degree of the polynomial

    def jsonable(self):
        return {'type': 'polynomial', 'F': self.F, 'coeficients': self.coef, 'degree': self.deg}
"""


p512 = gmpy.mpz(9319634055120059806745748435708214381572549431685774586671626637293434870481509294390553200298221079261837854412673960748108983618275089950667346940668503)
# 512 bit long prime
p1024 = gmpy.mpz(167780332417814791557185633280139094620399701270919685281072661484806859644138201313993771306912137951599884892086618860348074919967218594952879647759290846287306614649975347611649907631145784217353653507866496320995387982967013950048825794409156202596180959359044007356986797940576989969403213060035412266103)
# 1024 bit long prime
p2048 = gmpy.mpz(25470863719506445965075708354842107079884472650917771904021312045515220817417829515566709610109324303465461055432109006852236264861183112224977782911020928879118877401841120368392592182122340161519445975767856835669124012730950619704221016829258214575328653215513658082947894192466547032909169462559951013658605607416084963816031733602131783737713557467711049947600732765469680694980354036750452839633158342343281937462940531128893095166317622982135219104382743092946903628482092994756550387431788462546691099242369662804189941944982531651939152066912922798062738180568924256478351280742360606242522586581950669965699)
# 2048 bit long prime
p4096 = gmpy.mpz(921629896787945998651227620043239546596666276406476071639023278383824510783893240935595541307812013091050923887521049077768439156719992897132781251696799414137580956731811073261306783312697795057081221809000762189285114076184466695226819581712448075024616534148639975327629860998751398311146525753981790056893898957118582467750050428004910822024528223803017782057603128662226507252269779258719676911892172164080054973965316693792510606717600718654184838581621613080284387885546948258873893548793995188364616309128273691690028885740711192851638758530010265230258792972108882071566621980576208543346861132693204808855621758282363778762051552414179680974679123101400358237601342506860131539413302176842865847611929274931677048948816387213125465100346751981092172459844769325178199307508927671679405104246394264091735562643130119948126023382293660050290458688530348035960558250841069580560422879427005581833101577863920448541772801900684124066777824739955929726393133533280524668690328555349462327895650451867040891210125835513327765100194472364016509884880421036098703442706344617748909903411847601902126128170835180454431397772997408604937677590169909547986868659771802399498539689577625833915273175445729580176332714163380874741339047)
# 4096 bit long prime
p8192 = gmpy.mpz(945745325581499379785198312329978249973001592401086178631688631205617134924918039137507041525838262878359867186990255361935560071405125521057066249031181667477805525378998173547945157921003546427805485254656743036621229090181968381075253114211131311680642372034309713444784502536865069959007692897347180133834803188893544664394357589119844621345845554783473187649524483380896077257392271333954716883507513954524215169189936111689848929672471996226410156506052601678484445871310740426422184132020400014409471255105571424948964116723417890742975304885922106714413804027409339794023827367009515695334968901901332118007357426849233865218483605774461139796501518140604896065434392679924365509592916318983225519360299159211669077392736920241646961195144006710003326411517902506570364046029386386832772201576242697281984632275300022482074437858039840877278121139434581759265706740505793086457725317374268233658115642766671621403029396705459335037666497323942936815354862502608823591245244540750865450142940569484466971373787309044829914435436312819387033034429345178343376876184297827398334740947729457430721796785053594365773518929642849502522333392685478338280728287221246111794769828271802549577813582018468612983033551206636571205774414617460303465042979001431189411209131241906925113063263221480350294105353365324965917278747651128180215455170084888892189840589486243823142390315299402494567884340407249328289355521162432072525458863932217086769804658578081875817452101304634455550127530053980965896021074169338270348557085616185018404021343887052381964365596050502031300013654944039555603174621108951291162244698403791344673433656545541403187103368458375751026243912423449716459270023348330426562117482970996177418476015231849729892476483830768833910702576866662292740340382504508550210089174063934273099006815991353328378067977303395623154014249924755716496790943370754145816857343013129505495469945069650895428409923979388246361231138256633858154919784693927935422168799417968503787972595189128519318542352168395732296213790436584052320457082810498803963225038353409199669275275273017235810714429450847665800353233419890714377172402235001449375038108246264421290626254981463218710645327695856752085378821797373958629566124117645422994068090808760837458956250888763925429873024973605668409035800746109568905366234210519561041402448269055701885777632704846643082510672256570921953778216741286885013372753823558696700195385736880961217432228109040507262338648246855081)
# 8192-bit long prime
p16384 = gmpy.mpz(1140305476314610696645029532268875953382014019458260883147358149750612367307202600650912519511881356343827036285562292836067819838175415747757790654120786999862496774276525967978176646798569048629631386397226260317474145539826806576197186586070229671972822768362615432323760786230733219689226180721360776397912480392629097553611409775691891640337016075202091380405749523434816816850434624104473757537325085328923663814100588974067298741519361223242500655206119243051966532970361839055070486278747915320891378498448527028467349872449811430648851045525231602573565851062853342331216960251294395093377346143982011991518900604707303260479726991331201501797980040474920553830648053225870163766308124898438546707527070829168483743232781891544884527610958585154817815031725253973979595607199246852549628604637555032944887460316945250010847798059180770168891201927138718262975949008019730525000438868333217142453894545211774687310149895255184025601722558905541450483931546111618364202180233013325602400471923597834448890031390787380698124259558844566103170548511732219102669539063819876032033723179420233270394046166586070432622124999876097745992150277318270421458292991260941485640711612845931136730828279247665093621482146873301026409581801557236351746943664208058462160821565100017000182958660126734449918552839797874763922452772057939740679083908342285123225301791933765851160140599974765673856776755556496639761761064215489344893702715842407127896412579286744398625389784551327166475380975586360446136983487567902988992897100075042454263253838673784813649812777982951225691978865698265739198273344165005466341421303561923173769188332278210409934472971407353212270479940595616091050440566010811387693333420254134174916669992051859599631685596389086752701801294558795414508885641281426114254344411540204214773157366635960820714170839527285263466443974222383088271005149060528349396135599164107944199112028559360761728305757648614331723222633866398067813748306568864037032634891138039891855191099767192892387082046946406671239410629356227052172698681554014963328199790590197938715568425701096444130929500538673642301679631929860550450830951285753639846914085867984277760909915379087842211576061897595151246859373767570707631769306132596214775245343952651637640601900715970742021692188007280606930789445084518879751218983143441900158462363727585766418316654810778605482522245468391479925053876712012228393778410083425337148288319121530969541062332712773436250887131971715423220985292634642141139812158156355117205726125758095344102647502387988361692096615000562838154250645726372364303276221060246164261101720801754467284427544464529846557471958107114812565769565731902318473072038018130440201669202607191385307070597031169828188862972498508876495056563736078864807107903291367541638460109759107486994870124824185788266271391107469614130753516353904298075940694870726208369236358267732075147114416717707999659365848565659030791508828453480530512424316975330212645805549260518900604850678937976626964233758132647908294406964771494488782383827147196016328456817185610836845914703166111120309024626428065288693613944086706913331314564351603371949058720423813201531094042337047523818736894089999692254131030323069315312808668187806100913227580642598268187678706988505811636154106773795034456759723559894123080555747950240457772359452956153819548630356297187889468306936525900044097781850788407738096256969723123111591817883337389290938280337707502734194434485644227822343226675957399348475087361291772992607990390078311347068001136752835298642887960363543867446810295711149415359141971074382076256097510626944147272156612139456300601658895643947275872839765591700482011388610351490701617964178872444126156938642991182705084084803490724579109298861946557954728181621559577974788555023211975951274462896477667244279063105770902405232773527099861103790916975642932852549672609853282367324640094489518130207112278371442453704937000976398339427465704822874229817990899581050622059903326672360975219438651886536258860092955785638849655758882720938201258422318971010068286518241794217157940857051238804304770637069765460791514023097776194822860853820416334030297188504944103140721711921700609378858304379967958497178362132505394075698828829957974964515718920014362279399555546256392715421840571572750726598723956927985878432802613874943929149999378361291758291055313886083726300611099989387888138460310932918125321841451093855066910532910523498395149576702610181460961648806365651354776240915843433624847653092070025479742433671011501879354968308722744215895954711353042248154056586643020451091196652355767750165819937930272432879149528621204140900846565634186458392590698394232377635534515931575023606012182283623905350479652590198527455192180283505802135131205328228277878744981896362854195090838062705986641296248507117738877387969263516867050457531481448809344918025222313446614873389061061619612523660849867561194032834640307898548019627458716761)
# 16384-bit long prime
p32768 = gmpy.mpz(1110983818139946563763995463256859843870501697389399315745097374253002671619059581476293431148601284010728267985689538613683171663166844258504061579182998123937310477222650564059351438482185006188812013956055964298793021405734822569580797639081971611542230633764310594611689825540366921862197668066368793227528893617510811895795087883874774651364988909876214654787418173971728950404737597053851555858046719790715494141365425224879503750988111107631332898608772396469895594298502823427283478664832520068901872993178762365667333454090881047333538392896039913521237432811038361988124064866588627498700871457875257678640994586922929802119817678510893146659434606219942708848617611855209905631433297704986028859836150936728736998496872402565276382090669889750123224309455200039512248402965370982066071794878302001328660526289279224547807716049272237361948834707341079469561479045758183049073563681126655349392136077764809528978615561439735925890316462839342437749704237468289474784781563446973020228179908411182793830640580660832437638439738627302718270840761156158999590697131243331329872649923433740944988895093788864963916543365353798938162542556105248935368186717471123700764097567978111134398786385509426530078904614491627663334308417978742217564082792700799113580138023930632627607549787295266304865381731643126461360528044130359090115496901062441945759658971769004631870344313000688250660557551870547493486806360818440123317183909910075251068236671057433313985690450574457246853397028036851458810478273073302292159015091604056394433081310295602458354788202972665942793267344929834609413826414300614204246145181173494356744365197668297425713900897990013105389916463214713888744460661217258727678834445277353775477117597736513917300772941011505535845170139007586844761574099965408749106969293382782897303482690241410828895707023963200192766094445980034546741845955477655034198351706817299681724139252246579771524571250515142985992373185767151419175161592307927586406602681055231270012556250582538264331208623648791286811652732323559085647960901777129358098833777539994597744448241904493891250892968521669515501003199913030832313269558943757391033490942598005598561088792767329861466454402822608993500859010485067807679819868287239539358597532442349674231169443090623447977396644579253344280886460725457287994993338866662204247579606850421025972156767294438920684153326131934248605616489904932019809851089349259361936071663436982770022372373469143864171606401566877337917331247619772935103981287347517805014716944759832223516672029016895359873259331761434123570740307271572969205708727550994413804202738912564904444022135445430603995534192088035320220370159592081625963473358746347441306937332658076214330411197355063452632201522306207289418226537776298531608325692154806761518159770228594603136266349976423720700274848418350597085006952478538833505235547029708381034598676643178309438490264563367527446783572752792220335461024737852873314321671325897460236265421957622805205767056525531280963343174646988096841483807845464610464881938757631697707377289588666456958435041646754603356122986242746046888516396947419764685083607501557107227968765185072662512271053736006472660247232622567195156754202789601027786087020592443675408893645811033781351621668886657849819082025902497112158617628009059465501352905729262819063265129915840086774698479239705060798300225761672563429595157738525553642856184172702205290386973911994549644440385995365185955653896793565942747414554839493873482117899946488979597270315732523493842956006054844901262869509676622761741235725188309741546682111643679961641191315029466652055646462783817649568212447953979687697069338030032867146403975644691728424261187467298533330823012743988613256198442305292857853702447894963702242593098448286769240498881352714025664333768911147894320407335970425760818891441179956650813843204700128968497591037662981421660370101153713068922558151931467168482717110534839226634447396783451883111430307690014412316532775028051284289701472552523485421364673272369594919744298838830450142185000655837111765454342758750594230712051706757525269292784224571313133261395979610145709352368617775505498578446300405268705877400198615562402878992155477721182141853650828388406294525270768108782442444146473103585488805882641027625268953201866857168664692782830336812208149754343609806973568726600705577740761595617769275534984428504053444586043735268002690312798861841978221364689166296765729436912982025580057153672024319102468061855864168534201890773388471008201991055357512519978286539202626729869185060305059521051437953355352779728431358567616572174336022875055754752357274503431017828915669640153661159204952218080927054831866879608495935783561808905364573455655478821308177582450084110028386428263048698471439002594181449082463179509729293896832312908447385271140586269361616992319834303478870094203265749561527044694190854063780165164920649881816057640527837840882740850846884488099590796221234774721106099625074469622342840376610115121797344270031656581250101461199612888841929685630739775602299897125760394346870197499536830383903652804913673189832203964764079113541976925880909968337283831901188394637852876912003306091970064139989939973065341255064351006066736903336258897475572289462954906458760431767440140287454174367137004320447663714669028497759071944231583805438154580031164419280597603012491959744730977879761975936823825445292739877255049622831666219247907988441765720647918087271756631947039831379212539090560904083054514037182758462339140527555095897598521812007094106515857451307802482452530080019263605575175857212432264728919278567349660038870321082853957114042014055219354266062580331866051663469249343681436529948039742102998122321900800009058172357469808545047721010268885381642684581371996927945046202628266072222200319387171465055448493313455447245298498903680132673782700979214691765420631428945383796544851970594820730357359398742376778226650734626289134665191413674956021656837165515074678664628718857798847353310670902008888606081695404584625398135180681929524976949052842975304650978095452049638665257239217584856944664753309956903869633495405318383744750320399861507270492575600835249862706407060298399421490442814132508898928009749317174231002178544970708704566933839691095041379104759266101267565058931160080668213114618276105336507181345474741111890849297517498839775241459586090243461401036972646909279865302938324440778137682520502083196031787927330573515223357391234427533988887279921733436718969137367236853346249095524567901399233764591080789361231924910019426760610046490942390779484940854041376752372512048025296640731825102471257626357851604633229549331619286744076418022641552706855435602275258552534491998299086992943765957301542601876482477436662001162924611633539604345430979354387539037330192037029270393794415396336092586406194612231842808816766407548987654779883930083573829440950938433511865061111144233628888932704980221880825029512548645422433573423138814982258384965596843950538422711753087552856105308194700635416765583802832663782509154015615801064880886338143095575704245603160008297050915892605662546745456774792473453877901048450946775451568079262806285250066321983120499050806492847864206612261821001643331170676617262273683536822614158341561756712490522100090937097277324559517336667726271502269317013689633679126000808001977919100910194597509067592520917231662680931946620436259388788468224894848066388418473509152284413988675704161835137005114486004889562631762480477038138598852565473221485248113721656491316676151352664797425440266812296730592701372134422210857242745325764287683307890444197439026306965740683081780110121559927700431395701014196896578096345002233596151109303492561620504053302461911704401321037207956403010461692775079796894643536554333647635815922525388138461647965339231710347133844865174555834188344266016447560037916175322705497276504042052988531324455949796204708825403126195503870440913380412313309548620860328905161087975531493813528137340693792479992450827936342683253426656538286367050717727486518564299819630847315259282887720726367119877704689134948157407087529177198941453450368903044955811194605693039105599400775264086242092205848068653200774245008273348003774299359355795092039389781585141413977362659976799194068849695009045411870100501982225261615192558959096989219953349716840077248652248832972790228021745212009149107184798562379375487656646445620436757681594921178829514750764404052015903905047350594163031650318869649943897855500253666334379581292493269366965254958105432439389933842007456949044480045359142368355277828315471430619817583028548549193082943813283935608615782569919466197151538905711917603068516227516689686854459468135099617527585078017574330490703218144690341668067774272406902842167557600479509581640393108306675915178177882822692025559502022466769770402101910563822822209718884775749574838248997422862217687461410210338489458441953960805639994365721900325051645279072522373741640271795562429432423270209783906908746740293629646998225576814834238799834929796492069508264477444504690278397673678434160926220439303650395914017515274144575075197459372226204096078467171476541197400561641623907471529729266694237423311600134081013100882507119001512727035742596122828170168629830439627320077591533060773255129003193087995447822669564930906847178246431716738549093958414301823756071064428671663914519665168489400669070470833915157046303440743601094229373826146244915798052588773790925212205975348387371918868378596503216175436980585389105547806456457472597581443074256630744040383040240912935099616344133910393568641531583488968145923412671884501371123026306930783745248372938929718594853437843233566716133073274596157115593576907542018632217827243292774847198191668666439651053499326494734872459251180733806639904518407762360626422954158159248243953362559244783990870966127768747325605743529036983009458779)
# 32768-bit long prime
p65536 = gmpy.mpz(1285322824090455736597323986848783999565878469437977773380477543022335535756392222236458059918071832451457117249653139717238478640951314791133977632801406078540137587127690005943144801062193585683450548075735969371100711964024701658982173085710962819320646111979804595202742249464013146735282641912983856801106861015997259075319506365902291050298972463860634139351766489177062883121954339823314951403719661215749303643952398066249681409465260563742281426177688806536011124209798352459628715150650223967146903582041248383496116815822661127416720031227929646681614333359422345409439312800728309281262573309342132907356721086358526361457477515930964908131850365107077270923431157400574779388282820004786201436204120633370029754650795804748334179012682512438672584774439897663004691034277936690608091338451087256293683788087882936987419778722838969295387837253871726289597702539234542181322602824795425645623586974626429640291195581134388196791356262868756529215596539048585283328678827221835194125302764868927153645423843228019124632244614351275292292914259463998937760390630470053651054454142047257633827521436481637951127241465924403205250249858203982282135647832906281761834485896056764531326527024233566470121617539367686633748460010691756918310187183073397290287570304675800358423725985367045562194158540734419100922437272413409727668256751088572774431939137134116007165749005401506651929603386061820233418038388710221292138949058172885649922692199026551269010236098898796331009353074255048726634602968872162280082559222748007971686897515408154008970436973309617111717810722916521616927771925286283039243451184170392320203040301856201022152497500076579123198311299005754380978634428619847270466121519740965289618783907224394027921054461297359847701308326094581600350829366076006104301850056230091527105976978833199000394234245862009021177864966421467249712408969155828211651547066976916274666900495229536915964796533568993413750099153129211995616350785287619262949919284011040439691338072868472185227083798327708805483141307696706326702115100363291347169987349690223061043005129971927285753865321315995578251208979308920048390230804652770867949411172085529853868454423223289220818956695909306822284435914791543199520874764466603186322805714961004869142461584203137639680902204494903941398389180959614561326574773859212201651241317348261302806697283410102101506670781895323923400004475763323646606766831462841646808785508215237727661157571798904485991071710546189309491565131112268348893044765556622316400841861319600172538765842936509558899060323393655845607210734771164527476272584116666630077353337772491497443626357407278912960135859982992044825302738669546061132812275109859764897082081551046724051587873793825198588193082330349907055530309427420862732685092140105232491742311371847085470937423357331529660574641139493961538120303687297462757879944152860515397315157298817547504449651347398321936381918351786386861174706417756520904857617416089156883696300082445694515913137597245575690055747601542868583428923178728587438281963380368782581164904296077196681451794621344519497322765279197934921118280579959076641714329387352895271844023396601480820612756692223215743659860200650094982219737941882414544172929184949588116835802142626069227712741765150347065028619154305917586261305553801969841408386537880191567304408367303743728206665538830249227556473210638477918303458370829980440977433943081262257766718514584986156254120011252807620428489966504332583836653806375735895909158499921117425015949324009008746349390768365360530760252787413421484149061568239245508010654285007833941895655963608637440692612257354320832720990201266311081130842235477580113458483568342027239914903914786436912619576621009147692136357782670301437292160654404830310685638484338835977039929569158599953354921770790410063244531064141132846414852614629079147124852565411023891531113508440273270669702285692922066210909365033004906041264861029512051590476106565973054608364234406904620105991585583334221267739145660970376862498050015815061216237022793768916228830659603766213777640174117393245764293956875211282792490812580432058300220651206711495601518519542307563428032934820899099013211181943318581989002034267558496648289208382806317332333652605696898176587173768444992680816098829609583937167822833139340256239453656785166856723159171525003045939096530576725162879096789037983712811877778493391048567613822712486513362536904855158712433554593889627626643447437932885149176535220786273721098873806510653323427726701309072014639895389082369329754774113535473891046174721114461675667642821202176955621302532459137446759058472401843511501991188599499661257420410790095178925269618227206913044118885982784093692970005573500673199346824296811567246964683665204473084554640309103015986380899518162035678686938104630644421122394137966833756926079832513171415187233230717395572839863938361787108720377545191700976449227647398157105411603078730731963567104154005485153882870476373152582109127461738228919115031768507222617174852945810785366288244621153365603623467367431265508477102323835977321557873836291020245466008543126348139557111515227197232057485799132020815639034590596475794460852911591005978942187387684742840929047100207383630253896206596830399057718523193090863309624823950929454577757179826389150233244420062615877584080818102699125167950196273057506351615246711700523190910880824852130429074600634843127462817435000082788193245152953836482714248844463363313176458113765214866243764667640952236339092615950977289997405688842136176343880468619665798545369353757861264555911702556975573140519891086743767819789340167643091576809659891025469416508999248235834091278680354830015864593917561167635243483120557261639571160280178262386810368327745367146709299016504549646319582398292558212175665618967717939063067042826365400516773635294878694074343433505286154481571906763405476951071505907792328987127855328800391069878174652129535612836196123783084098588634367929861752691547493323321891213889473164106854782056891657394281022285370469023559306875527138557276367804479091724341435537546340272288985245487740643786733563682212616279364654541727428590211077961688768234498635576297244211514632280749305293107683614886766909957327250203158815735683125133972108848849235034387544948602622279771017989365921971642097977294148757581834866077541099083689706820358109226026040366823999800606724371576757556340674257870829681930108259947511756689037251167525160021640239092074324078708054608105187370007276675736712268324810530915865394892493517885206136238330381870242961593810578584602844203808815984367590573860773184008701858129747578084198896264912606799422672552079824337618074387728810542598854193123161314312503057189412105806254142949632428009338194304969800021285190550844862375309596560420518630423875775063710129092990755500632562282599373751001835663659006953712758301279847220853320340842326054737443544612297674875525223609635507716521891426289918867402928960823039412194978899731987348628170799302353441589845034953991994754669774976188069970678362121688127295325619995888063902617206233617317948459381745415517952516300858940126154884568381088420682714303715728106369405716206919969012447560778068223805948660567577525606592983745605484883151479710887306905785506061236860908147268567488229729273266339979317363083217603679000847087988982026869594334280482864094070097188847522931161145473304603541778068031295942258370301966626673629573002079080520294140002784278741815028674945765365178981347835720217189299537406558048681208876635671663339132872906477266069035056810180831096843141961627818065733806646318079815239669983256105189507137448107886214980928266803597943370861697925223041029283501758118385876063190219966427974310990550168625992727238242260558219556096106534554020748320848167172224926243326403985365422200722451860046037681681860513816117152833073170167910238197647492375380954207528860666833226720073248139617490792452097074628902807260635183968046765420701170037878543166108276350825057568769912754386942532316499803475546751999204384606075016223288516120287843322758316582845868011707736762451673746406774871673427987878617616017362766348264657332182020843102260951699769423929214018685910137616232977087329245119727686501747242615797621747641367354797080923494534935877674605082908335006129194114979396045144909916551440271642993037993609867190705665333408266829581528069751955777242150352388012981706329341963387116508372557312330139723078300630080429980055637639448138001687688289786581452007678168148183677712510623382718476488198866927308772016277283848295104849615934879496518865768528564655957662173322776654556092957723434211527919763092035244781077932811334635239172206721895602966420128140340969737736599764258726630512680830697348912716255622378853992333466308803038521166452310306874928839634775339688485153398884620990460381915311555325085980612284185334160496881713778624918117992597852544340264788217557906447608898582133481739150703245030495112195426241632892475854681058310916197083531334408888029275348546877165912982943763363579710907245807299597134578501894867902837611896048394719169478798255413766099628922859152820917765667918031796020846364024554721559244985862570124863955485513783321645521800975685012947993718389535167756965312523239537048116904630494360066205492141087787840219871062067955581288768899219633050695221197549788149856357261382125011404246573630529938235633603946779859626489946306462490533188049203439778772194819200420194939149871332731121387621317865701207240901474774036099886859519507567068098022861844828735038047651070013934005386900149421394397372984648062468115757629316654670191117787362272687475078209275460556531837490405287699226907794477682808703844614857943866885114915096208335290728347632678577916026882563264270356144795816155672655415764487961035978686288742997453152308043362951410591631920752034370143198172610790543135802167513202224386381309577139802678436360721965687621233121944825743205951649975161094725987421545625494329966701234490309817674527805172868993581662479240715039428458688394143248235264367805546453180741346613463742324478328957415582580139794562375501046923056454124499785365585560069579880421282781923180360007617240935346464095625947960067472012814580575055692048810794389872476873201567755433884141581551744846376935104618904101778327289656622948370386360170023981851479654540338456811070295544955704705955635862716699610250965850098033435696163038653790013671463541519245132781298520354990679232024831362430485657724401786213147727461974312049886371421003511815423807901322977862090221809892075065753993674989415961289306181637439141942191984155434736122549947591768992560734460903482936879028285350193647915755602926896254704456841585723957110055813154717094080118283586045941399977220207652920618627239848948265569462227590289889021515444732424563146706427253128920139913159286500555655663154940197865387585382590518951567221177871210792294104807633227651644581144608316092368815511367519511729691719116933003411153002145204168704800528078157928396761608884627775762182975637290096023151241502255937307007442114832316213697389406297279669856484588741164434508320749025124745608855067218965274442418535067238008485197676368463789702500104204370830915571026276489112287660443711761418903538131610857201198012663591968226985872572829197050341871276791004011271369823554219398140456293323023782316278122293525496320140752297284070244887852433584023361687181637497339184344284196901953520542922446638309860468479620386488402260034127501884689016513873846078520222130574223883994635521207557873436167288742298509818987200338127096849920479689388215721373554658840628889185088329980548138424451732335500603987950921922437245293241254757048300770995154746891148693163651345276383505263571994897794375456247861455987473949826987861286280934040241709015067734448510473684360423035830338892555106089012518440469168274429575491256749484545521681169026182382197269773729031284085331793024582511738227762682519310743067715223978838878913703028047706955481528288226232360080463115085565879309004876116333181124107914717847941345571131003164937769842601564540801920529915802288366575134342973480123562187636727170388059278685133218230326411261895951451236992254024046438698677132904033038605085539520600158781663690364331773210136936455849584717352936032699182610891988175376583515079799169331713425390393401207435482544020579541326821573121052592250070304694869961604176337486483077071387806867073871409812628597393482416976621900464053335908481770638351775007995414868227459932676992588973524682523947520826611290642231671779797972176646627178034765696963979790368335917048707780501783013375273343636232623915669774414598775295757327936759664526510289450224461613689899951880610417875249275889973955820001299445550230498438136514613326106679497333125745598803124231584728471553039045195571340066330548859252065064915081132976657370121296808095824453779904675164439417769417806884677881281044261575885735013015678121446989186585791992131685784376972973678267432879385840522733951618196687154072486917898664971130236979698807591628036312866241781726057053201119067382926522013656856445663248959097850713092593485188941427972897368652012562822680365008479250789832949435298393156999338065051222547068521946779020727259309156053665773411007929231182955341641862452635078505918383503372112218889557425927364004401269146336200594261560487540742120820160108371628715844672230697000264786384909479364760659311389163049245098079439247155004340526829180275929308575335494090459193445750856072138060193746906541050265953679784114460914140437886632603249529934741643178060209637002739797286608445216512484571235265786252426629753009826749886251417557162942081055099738633137259216988696823448509178555542996741200634780171518796030446452473095594193213696832867183635777610578095740048173002786733625316118208974045392655703761079306662118407240789486541568620446111023236787588186690909196838134115809151586017736226660409178282887848133318371306000803829427384917267191290520874352010881796083005222964776422544981232859293971653276652422350192408572628794858100900917227197556790598363003695038775988345607980893948321819447762894716929271334340565970838377619776558300222517075143847888139867215684677968745036620297279866808108883070811661684464655842196197372200201147120688545504210938978535849049629152517570075964068735547976488122214538858679568916641899076231203201200412777757885538506290844592277756064176717347736664088484338834068087057450941068859284070475636027873916996663918686483396220193157292424972333324875039019833077200741236836109997814951624207830938536628920182075369031222212996507070999587023009529536665752020237832820901205398558576261959955040953607243736492418626313578372330268678057175152680410049713606327777499943074104230591677765591016348594313311596308814148171621740463524171073124244130963675539866786701801127321818726509869148088346973202260272225221876486130916541526924038548663901270046054385899458638473609234074056758985712590162290484604518067717037012505373717186152683982874082212089547137044308507071060625893234233883041938085178893456518410984194824609751024449213749271396136781330986475531350284102523456075775576764311979224068927224334809155000590166277659056923951059276401817875641129101199050363397565410341168464512066140794136009439914896875961543790626598361254059514637652226218492488832120504276517554853378234596244452732904717581340458330980082236392664651218886061113098016630105112882908933197253906893721823696568515250003752992960955898674179684670539952954859542432461690656513782645025225069994642003304200006795015224849935117109243020983523622108113156007717107741562833890581322183423782898948701633436373884367015754872519233907719707662045164618329121573072830324689496255436104102948849703330684071879139370306172590174722591776456702074352232490547197385074667659800046166239664594307727756252186005853929414070146453131098220005163374790127844308989474859070589986726272342116193468815471367375970866311912079447993025401087600145440669347722290623014534658669696345205859348056228545702735587806451316949495691419417563161513732055098107462752238207838269385044566576051512915747859386701327994359206221531536607914046740412981514019699105491610499709745204888015209598724635667203110591426214313650155238232905041727197301828619668613256455134670948752624357145186868248199865756518563771583682991734939724027010450463117375282639641781304923313091622665928530119686269233581737876520730830829211744542188476382276819859757453832080966692737305145130354377285882872999494542842201213787436511715186885532706246622281911374331876702399664162930968837403765218588262068822023356827353774446890878146549930599171827314904097743019321810599081038985207610712102152216945706251113115749539903704009446361280870352534156255739930054926086688037457815662862007619163472439421660889197274389052189244823432007182248639813936879166671398293759597917128883869832259086385944186870766887349516615726973859732706878676998731280817919612079199118220632191156456407074586710897331349260180975262161301623006848836795492616542012082776995641810816623830577488511870578534555368698318193578827653420573475343108889657392889923064609529496479860490582971969607540210708582251736488872615453435268790939575879129144053955376883850040406761870184214853328332461569855105250027181553408465247952023478620787793466065255957760969965876962013460779042966614309246863988895437496393154920773264806296130263213877415587941148109166397168366186368466702304152090868384883862925447964881158283179352354687195801542584280120735339189011237969746141816431919894573479596890449561695984362776218946378359695866505384310698384675463824844970153185052898888192628185972268855438490980256227969337874390285924760470637147343687056671154966729364609861174550747353797207449416503565121965783547699901803555341293152412158400413324817602238311957846829803090542682550637277554749992085158640242265145326904442960995441718082293228216780455086204923418467344411595940400765656837500081951762518017509334564901569363579380118154993160310909066638024211012816018073699809445453588306919709006038092202436535432297857914967331667852492880027684146278417443915373660743217962691390495717857469822469424132507309476251589656970407408175207439727400678738060879733535507348677303194727590744288936516311307526117430008599834333894354387068091088142055396326344869037326834167395318508376490812646098974690416236931066902193874230720079381592645900602249905591702702771072431386926356229469696273027872083041975460111156770395340736173633104269876958955873769823957831173631955840146082563262549899787624040132432451301973775698258913198877510972556335236125951060615541652805687094489515609651362565126919958522793416501551135759636934592253016210384883197619598515388574256675556524257777888802844324362915310685248048056620615475154863651682191220832498732353002968612508438308051020324600828942989372519775392927323570667344814525259492958060481323706586010323578709111965437725774481833776206776914648724802222853757678003091774198067343495602162065266206318296499410747533322566887082838602925249310267482202017245775507384318512587321740363543310262645269098692880452379778319046696800216216857212896235336789963425550410521733832037271342453976733768693643171517637787265148609974427385052570558596004948876002812755961712261115135976214784760268351443250593024979942426590095785579636279592507638822715037811561607082871119819694203370554906060240285028038599110277207661555493956390465591689284718644887215780586062050571436038567203647510587454783085879492742297501515334123101005178685818659814980441)
# 65536-bit long prime
pDict = {'p512':p512,'p1024':p1024,'p2048':p2048,'p4096':p4096,'p8192':p8192,'p16384':p16384,'p32768':p32768,'p65536':p65536}