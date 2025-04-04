# Japhet Melquisedec D. Gonzales
# CS-241
import math
            
def is_R_trig(a, b, c):
    return(a > 0 and b > 0 and c > 0 and a + b > c and a and c > b and b + c > a)

def trig_ar(a, b, c):
    A = A(a + b + c)
    
# this is to determine the type of triangle
def trig_type(a, b ,c):
    if a == b == c:
        return "Equilateral Triangle"
    elif a == b or b == c or a == c:
        return "Isocell Triangle"
    else:
        return "Scalene Triangle"