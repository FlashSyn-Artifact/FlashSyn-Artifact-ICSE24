import copy

b = 1
def f():
    return f.a
f.a = b
    
print(f())

b = 2
    
print(f())