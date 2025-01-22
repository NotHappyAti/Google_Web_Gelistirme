'''
Main idea behind the async is to run multiple functions at the same time.
In this example we run two functions xfunc and yfunc in parallel.
'''

import time

# This is a synchronous function that takes 5 seconds to complete
def xfunc(): 
    time.sleep(5)
    return(5)

# This is another synchronous function that takes 5 seconds to complete
def yfunc():
    time.sleep(5)
    return(10)

if __name__ == '__main__':
    print(xfunc()) # We wait 5 seconds to complete this function
    print(yfunc()) # After waiting 5 seconds we wait 5 more to complete this function

'''
It goes like this:
1. We call xfunc() and wait 5 seconds for it to complete
2. We call yfunc() and wait 5 more seconds for it to complete
'''