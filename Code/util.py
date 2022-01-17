import pandas as pd
import numpy as np

def find_number(text):
    num = re.findall(r'\d+', text)
    return " ".join(num)

def Euc_dist(landmarks1, landmarks2, spacing):

    landmarks1 = spacing * landmarks1
    landmarks2 = spacing * landmarks2
    diff = landmarks1 - landmarks2
    squared = diff * diff
    dist = np.sqrt(np.sum(squared, axis=1))
    mean = np.mean(dist)
    std = np.std(dist)
    return dist, mean ,std