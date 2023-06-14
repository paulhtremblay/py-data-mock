import random
import numpy as np

def resample(l:list) -> list:
    final = []
    for i in range(len(l)):
        final.append(random.choice(l))
    return final

def repeat_resample(sample_a:list, sample_b:list, num_iter:int = 1000) -> list:
    difference_in_means = []
    for i in range(num_iter):
        resample_a = resample(sample_a)
        resample_b = resample(sample_b)
        difference_in_means.append(np.mean(resample_a) - np.mean(resample_b))
    return difference_in_means

