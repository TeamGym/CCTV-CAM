import pickle
import dill
from DetectionResult import DetectionResult

with open('test.class', 'wb') as file:
    dill.dump(DetectionResult(100, [1, 2, 3]), file)

with open('test_p.class', 'wb') as file:
    pickle.dump(DetectionResult(100, [1, 2, 3]), file)

with open('test.class', 'rb') as file:
    data = dill.load(file)
    print(data)
