import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

# TODO: Actual unittest

import pyext

class A0(object):
    a0 = "a0"
    def __str__(self):
        return "<A0: {}>".format(self.a0)

class A1(A0):
    a0 = "a1"
    a1 = "a1"

class A2(A0):
    a0 = "a2"
    a2 = "a2"

class A3(A1, A2):
    def __str__(self):
        return "<A3: {}, {}, {}>".format(self.a0, self.a1, self.a2)

class B0(object):
    b0 = "b0"
    def __str__(self):
        return "<B0: {}>".format(self.b0)

class B1(B0):
    b0 = "b1"
    b1 = "b1"

class B2(B0):
    b0 = "b2"
    b2 = "b2"

class B3(B1, B2):
    def __str__(self):
        return "<B3: {}, {}, {}>".format(self.b0, self.b1, self.b2)
    

Test = pyext.multimethod(pyext.ClassResolutionStrategy())
def __default(*args):
    print("DEFAULT", args)
Test.default = __default

def tests():
    Test(A0(), B0())
    Test(A0(), B2())
    Test(A2(), B0())
    Test(A2(), B1())
    Test(A1(), B2())
    Test(A2(), B2())
    Test(A3(), B3())
    Test("foo", 3)
    print()

@pyext.methodof(Test, A2, B0)
def Test_A2B0(a, b):
    print("Test_A2B0", a, b)
print("Adding:", Test_A2B0)
tests()

@pyext.methodof(Test, object, object)
def Test_base(a, b):
    print("Test_base", a, b)
print("Adding:", Test_base)
tests()

@pyext.methodof(Test, A0, B0)
def Test_A0B0(a, b):
    print("Test_A0B0", a, b)
print("Adding:", Test_A0B0)
tests()

@pyext.methodof(Test, A0, B2)
def Test_A0B2(a, b):
    print("Test_A0B2", a, b)
print("Adding:", Test_A0B2)
tests()

@pyext.methodof(Test, A1, B2)
def Test_A1B2(a, b):
    print("Test_A1B2", a, b)
print("Adding:", Test_A1B2)
tests()
