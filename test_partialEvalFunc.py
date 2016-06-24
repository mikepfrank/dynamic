import os; os.chdir("C:\\Users\\mpfrank\\Documents\\GitHub\\dynamic")
import partialEvalFunc; from partialEvalFunc import *

a = PartiallyEvaluatableFunction('g', ['a', 'b', 'c'],
				 lambda a,b,c: a**3 + b**2 + c)
print("a = %s" % str(a))

b=a(b=3)
print("b = %s" % str(b))

c=b(2)
print("c = %s" % str(c))

#d=c(h=7)    # Exception

d=c(c=100)
print("d = %s" % str(d))


