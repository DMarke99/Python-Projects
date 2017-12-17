#imports libraries
import numpy as np
import sympy as sym

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

        #matrix is X * X.transpose                
        XX = np.dot(np.transpose(X),X)
        
        #in this model, y = Xb, where X is the matrix of powers of X, and b are their corresponding coefficients
        #it can be proven that the equation of best fit is given by b = (Xt * X)^-1(Xt * y)
        b = XX.I*(np.transpose(X)*np.transpose(np.matrix(y)))
        
        #creates symbolic equation for polynomial
        x = sym.Symbol("x")
        
        #evaluates polynomial using Horner's rule
        y = float(b[n][0])   
        for i in range(n-1,-1,-1):
            y = y * x + float(b[i][0]);
        
        #returns polynomial
        return sym.expand(y)
    
    except np.linalg.linalg.LinAlgError:
        #LinAlgError occurs only when Xt X is not invertible
        #this occurs when the degree of the polynomial is too high
        #to combat this, reduce the degree of the polynomial by 1 and trying again
        return PolynomialRegression(y,x,n-1)
