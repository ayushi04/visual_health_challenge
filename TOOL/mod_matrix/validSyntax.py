from math import *

def validateSyntax(expression):
  functions = {'__builtins__': None}
  variables = {'__builtins__': None}
  '''
  functions = {'acos': acos,
               'asin': asin,
               'atan': atan,
               'atan2': atan2,
               'ceil': ceil,
               'cos': cos,
               'cosh': cosh,
               'degrees': degrees,
               'exp': exp,
               'fabs':fabs,
               'floor': floor,
               'fmod': fmod,
               'frexp': frexp,
               'hypot': hypot,
               'ldexp': ldexp,
               'log': log,
               'log10': log10,
               'modf': modf,
               'pow': pow,
               'radians': radians,
               'sin': sin,
               'sinh': sinh,
               'sqrt': sqrt,
               'tan': tan,
               'tanh': tanh}
  '''
  variables = {'e': e, 'pi': pi}

  try:
    eval(expression, variables)#, functions)
  except (SyntaxError, NameError, ZeroDivisionError):
    return False
  else:
    return True

if __name__=="__main__":
    print (validateSyntax("1+2==3"))