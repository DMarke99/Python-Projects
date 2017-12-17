#imports libraries
import numpy as np
import sympy as sym
from numpy import transpose
from numpy.linalg.linalg import LinAlgError

#performs polynomial regression on data y and x, and returns the equation of best fit
#y = p(x), where p is a polynomial of maximum degree n
def PolynomialRegression(y,x,n):
    try:
        #due to recursive error handling there must be a base case
        if n < 0:
            return 0
        
        #manually raises error if y and x aren't compatible
        if len(y) != len(x):
            raise ValueError("the length of 'y' and 'x' are different")
            
        #creates matrix of values corresponding to powers of x from 0 to n
        X = np.matrix([[k**i for i in range(n+1)] for k in x])
        
        #matrix is Xt * X, where Xt is the transpose of X               
        XX = transpose(X)*X
        
        #finds eigenvectors and eigenvalues
        lambdas, V =  np.linalg.eig(XX)
        
        #if zero is an eigenvalue, then there is a linear dependency: a non-trivial definition of 0
        #this is better than relying on the program to raise a LinAlgError when attempting to invert XX
        #because the method used to calculate inverse for larger matrices can be quite inaccurate
        if any([abs(i) < 10**-13 for i in lambdas]):
            raise LinAlgError("n")
        
        #in this model, y = Xb, where X is the matrix of powers of X, and b are their corresponding coefficients
        #it can be proven that the equation of best fit is given by b = (Xt * X)^-1(Xt * y)
        Xy = transpose(X)*transpose(np.matrix(y))
        b = XX.I*Xy

        #creates symbolic equation for polynomial
        x = sym.Symbol("x")
        
        #evaluates polynomial using Horner's rule
        y = float(b[n][0])   
        for i in range(n-1,-1,-1):
            y = y * x + float(b[i][0]);
        
        #returns polynomial
        return sym.expand(y)
    
    except LinAlgError:
        #LinAlgError occurs only when Xt X is not invertible
        #this occurs when the degree of the polynomial is too high
        #to combat this, reduce the degree of the polynomial by 1 and trying again
        return PolynomialRegression(y,x,n-1)
