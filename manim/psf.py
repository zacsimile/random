import numpy as np

def colorize(arr, c=None):
    if c is None:
        newarr = (255*arr).astype(np.uint8)
    else:
        # arr = (arr-arr.min())/(arr.max()-arr.min())
        newarr = (255*arr[...,None]*c.to_rgb()[None,...]).astype(np.uint8)

    return newarr

def gauss1D(x, a=1, mu=0, sig=1, b=0):
    g = a*(np.exp(-((x-mu)**2)/(2*(sig**2))) + b)

    return g

def gauss2D(x, y, a=1, mu=[0,0], sig=1, b=0):
    g = a*(np.exp(-((x[:,None]-mu[0])**2+(y[None,:]-mu[1])**2)/(2*(sig**2))) + b)

    return g

def donut1D(x, a=1, mu=0, sig=1, b=0):
    q = ((x-mu)**2)/(2*(sig**2))
    d = a*(np.exp(1)*q*np.exp(-q) + b)

    return d
    
def donut2D(x, y, a=1, mu=[0,0], sig=1, b=0, sigp=None):
    q = ((x[:,None]-mu[0])**2+(y[None,:]-mu[1])**2)/(2*(sig**2))
    if sigp is not None:
        # Strange case for saturating the middle of the donut
        qp = ((x[:,None]-mu[0])**2+(y[None,:]-mu[1])**2)/(2*(sigp**2))
        d = a*(np.exp(1)*qp*np.exp(-q) + b)
    else:
        d = a*(np.exp(1)*q*np.exp(-q) + b)

    return d

def lorentzian1D(x, a=1, mu=0, gamma=1, b=0):
    return a/(2*np.pi)*gamma/((x-mu)**2+(gamma/2)**2)