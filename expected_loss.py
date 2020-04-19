#Import relevant python libraries
import random
import scipy
import numpy as np
from scipy import stats
import math
import scipy.special as sc

#Define h function
def h_fn(a1,b1,a2,b2):
    h=0
    for i in range(a2):
        h=h+(sc.beta(a1+i, b1+b2))/((b2+i)*sc.beta(i+1,b2)*sc.beta(a1,b1))
    return h
#Define loss function
def exp_loss(a1,b1,a2,b2):
    h1=h_fn(a1+1,b1,a2,b2)
    h2=h_fn(a1,b1,a2+1,b2)
    loss=abs(sc.beta(a1+1,b1)*h1/sc.beta(a1,b1) - sc.beta(a2+1,b2)*h2/sc.beta(a2,b2))
    return loss
