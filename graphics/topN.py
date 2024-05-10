import matplotlib.pyplot as plt
import numpy as np

x = [1, 2, 4, 8, 10, 16, 32, 64, 128, 256]
y = [0.7468, 0.7488, 0.7418, 0.7174, 0.7128, 0.7099, 0.7117, 0.7172, 0.7206, 0.7232]

fig, ax = plt.subplots()
ax.plot(x, y, label='MAE', color='blue')
ax.legend()
plt.xlabel('topN')
plt.ylabel('error')
plt.show()
plt.savefig('graphics/topN_MAE.png')

x = [1, 2, 4, 8, 10, 16, 32, 64, 128, 256]
y = [0.9777, 0.9761, 0.9656, 0.9372, 0.9312, 0.9257, 0.9261, 0.9316, 0.9349, 0.9374]
fig, ax = plt.subplots()
ax.plot(x, y, label='RMSE', color='red')
ax.legend()
plt.xlabel('topN')
plt.ylabel('error')
plt.show()
#plt.savefig('graphics/topN_RMSE.pdf')