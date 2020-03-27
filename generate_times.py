import numpy as np

from pendulum.model.input.times_schema import Times

count = int(input())
start = float(input())
end = float(input())

array = np.linspace(start, end, count)
obj = {'times': list(array)}
model = Times.parse_obj(obj)

filepath = input()
with open(filepath, 'w') as file:
    file.write(model.json())
