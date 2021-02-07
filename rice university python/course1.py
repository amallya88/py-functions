# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.
import math


def project_to_distance(point_x, point_y, distance):
    dist_to_origin = (point_x ** 2 + point_y ** 2) ** 0.5
    scale = distance / dist_to_origin
    print(point_x * scale, point_y * scale)

project_to_distance(2, 7, 4)
print("---------")

# compute f(x)=−5x^5+67x^2−47 for x in [0..3]
# what is the max?
lst_x = [0, 1, 2, 3]
f_x_lst = [-5*(x**5)+67*(x**2)-47 for x in lst_x]
for x,f_x in zip(lst_x,f_x_lst):
    print("x=",x, "f(x)=",f_x)
print("max:", max(f_x_lst))
print("---------")

## Question 6
# When investing money, an important concept to know is compound interest.

# The equation  FV = PV (1+rate)^{periods} FV=PV(1+rate)**periods
# relates the following four quantities.

def future_value(present_value, annual_rate, periods_per_year, years):
    """
    Input: the numbers present_value, annual_rate, periods_per_year, years
    Output: future value based on formula given in question
    """
    rate_per_period = annual_rate / periods_per_year
    periods = periods_per_year * years

    # Put your code here.
    return present_value*(1+rate_per_period)**periods

print("Test","Expect:745.3174428239327", "Output:",future_value(500, .04, 10, 10))
print("$1000 at 2% compounded daily for 4 years yields $", future_value(1000, .02, 365, 4))
print("---------")

def area_equilateral_triangle(s):
    return (math.sqrt(3)*s**2)/4

print("Area of equilateral triangle with s=5",area_equilateral_triangle(5))
print("---------")

def f(n):
    if(n % 2 == 0):
        return n//2
    else:
        return 3*n+1

print(f(f(f(f(f(f(f(f(f(f(f(f(f(f(1071)))))))))))))))
    
