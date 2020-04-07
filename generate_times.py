import numpy as np

step = float(input())
start = float(input())
end = float(input())

array = np.arange(start, end, step)

filepath = input()
np.savetxt(filepath, array)
