import os
multiply =lambda x,y:x*y
print(multiply(4,2))
title="Hello"
(lambda title:print(title))(title)
ww="dscfsdfc"
(lambda title:print(title))(ww)
#filter#######################################################
def is_odd(a):
    return  a%2==1
ll=[1,2,31,53,236,1231,632,32,23,656,343,776]
newll=filter(is_odd,ll)
print(newll)
print(newll)
def is_odd(n):
    return n % 2 == 1
 
newlist = filter(is_odd, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(newlist)
import math
def is_sqr(x):
    return math.sqrt(x) % 1 == 0
 
newlist = filter(is_sqr, range(1, 101))
print(newlist)
print(list(newlist))
#filter lambda#######################################################
numbers=[1,2,53,645,123,6435,234,743]
a=filter(lambda x:x>10,numbers)
print(type(a))
print(a)
print(list(a))
#sorted lambda
cc=[
    ("hia",350770),
    ("hib",155000),
    ("1500",1500)
]
print(sorted(cc,key=lambda cca:cca[0]))