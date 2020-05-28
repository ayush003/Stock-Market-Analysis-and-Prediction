from numba import jit, cuda
from timeit import default_timer as timer
def func(a):
    for i in range(10000000):
        a+=1

@jit
def func2(a):
    for i in range(10000000):
        a+= 1
if __name__=="__main__":
    start = timer()
    func(0)
    print("without GPU:", timer()-start)

    start = timer()
    func2(0)
    print("with GPU:", timer()-start)

