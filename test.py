import time
import numpy as np
import timeit
# start = time.time()
# l = []
# for i in range(100000):
#     l.append(i)
# print(l[:20])
# print(time.time() -start)

# start = time.time()
# l = 0
# for i in range(1,1000000):
#     if l%i == 0:
#         l += i
# print(l)
# print(time.time() -start)

#start = time.time()
arr = np.array(range(1,10**8))
#a = arr[arr%10000 == 0]
print(timeit.timeit('a = arr[arr%10000 == 0]', setup="import numpy as np;arr = np.array(range(1,10**8))", number=50))