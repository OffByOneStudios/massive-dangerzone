import importlib
madz = importlib.machinery.SourceFileLoader("madz", "D:/documents/massive-dangerzone/examples/language_tests/plugins/python.set0[0.1.0]/.wrap-c/madz.py")

def test1_func():
    print("Hello From test1_func")

def test2_func0():
    return 0

def test2_func1(a, b):
    return a+b

def test3_func():
    print("Hello From test3_func")

def test5_func(a, b):
    #TODO(Clark) This function needs access to _madz.py's type declarations.
    ret = madz.TEST5_STRUCT()
    ret.b = 16
    return ret