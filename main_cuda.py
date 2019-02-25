import numpy as np
import time
import theano as T

a = T.tensor.scalar()
b = T.tensor.scalar()

y = a * b

multiply = T.function(inputs=[a, b], outputs=y)

print(multiply(3, 2))
print(multiply(4, 5))
