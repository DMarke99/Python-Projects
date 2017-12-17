#Defines a mathematical vector class in Python
#Import useful functions
from math import sqrt, acos

#Defines the Vector class
class Vector:
    
    #Defines initialisation
    def __init__(self, *args):
        
        #Vectors can be initialised by explicitly listing values
        if all(isinstance(arg, (int, float)) for arg in args):
            self.vals = list(args)
        
        #Vectors can also be initialised from a list of numerical values
        elif type(args[0]) is list and len(args) == 1 and all(isinstance(arg, (int, float)) for arg in args[0]):
            self.vals = list(args[0])
            
        #No other formats are accepted
        else:
            raise TypeError('Input arguments must be numeric or in list format')
    
    #Vectors are printed as Vector(x1,x2,..)
    def __repr__(self):
        return 'Vector' + str(tuple(self.vals))
    
    #The length of a vector is the number of entries it has
    def __len__(self):
        return len(self.vals)
    
    #Allows users to access items in the vector
    def __getitem__(self, index):
        return self.vals[index-1]
    
    #Allows users to change values in the vector
    def __setitem__(self, index, value):
        
        #inputs can only be numeric
        if not isinstance(value, (int, float)):
            raise ValueError('input value is not numerical')
        
        #Vectors are 1-indexed
        self.vals[index-1] = value
    
    #Allows iterating through the entries of the vector    
    def __iter__(self):
        for i in self.vals:
            yield i
    
    #Defines vector addition
    def __add__(self, other):
        
        #Vector-Vector addition is the only addition defines for vectors
        if type(other) is not Vector:
            raise TypeError('Vectors can only be added to other vectors')
            
        #Vectors must be same length to be added
        if len(self) != len(other):
            raise ValueError("Vectors aren't the same length")
        
        #Returns the elementwise sum of the vectors
        return Vector([self[i] + other[i] for i in range(len(self))])
    
    #Defines vector subtraction
    def __sub__(self, other):
        
        #Vector-Vector addition is the only addition defines for vectors
        if type(other) is not Vector:
            raise TypeError('Vectors can only be added to other vectors')
            
        #Vectors must be same length to be subtracted 
        if len(self) != len(other):
            raise ValueError("Vectors aren't the same length")
        
        #Returns the elementwise difference of the vectors
        return Vector([self[i] - other[i] for i in range(len(self))])
    
    #Defines multiplication of vectors   
    def __mul__(self, other):
        
        #If other operand is numeric, perform scalar multiplication
        if isinstance(other, (int, float)):
            return Vector([other*x for x in self])
        
        #If other operand is a vector, perform dot product
        elif type(other) is Vector:
            
            #Vectors must be the same length
            if len(self) == len(other):
                return sum(self[i]*other[i] for i in range(len(self)))
            
            #Error otherwise
            else:
                raise ValueError("Vectors aren't the same length")
                
        #Any other operand isn't compatible
        else:
            raise TypeError("Vector and other operand aren't compatible")
            
    #Both types of multiplication are commutable         
    def __rmul__(self, other):
        return self * other
    
    #Defines vector product of 3D vectors
    def __xor__(self, other):
        
        #Both operands must be vectors
        if not type(other) is Vector:
            raise TypeError("Vector and other operand aren't compatible")
            
        #Both vectors must be the same length
        elif len(self) != len(other):
            raise ValueError("Vectors aren't the same length")
            
        #Both vectors must have length 3
        elif len(self) != 3:
            raise ValueError("Vectors must be of length 3")
            
        #Returns the vector product
        else:
            return Vector(self[2]*other[3]-self[3]*other[2], self[3]*other[1]-self[1]*other[3], self[1]*other[2]-self[2]*other[1])
        
    #Defines the Euclidean distance of a vector
    def norm(self):
        return sqrt(sum(x**2 for x in self.vals))

#Function that returns the angle between two vectors
def angle(vec1, vec2):
    
    #Both arguments must be vectors
    if type(vec1) is Vector and type(vec2) is Vector:
        
        #Both vectors most be non-zero
        if vec1.norm() != 0 and vec2.norm() != 0:
            return acos((vec1*vec2)/(vec1.norm()*vec2.norm()))
        
        #If either vector is length 0, return error;
        else:
            raise ValueError('Vectors cannot have magnitude 0')
    
    #Error if either argument isn't a vector     
    else:
        raise TypeError('Both operands must be vectors')
