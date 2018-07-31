from statsmodels.discrete.discrete_model import Probit
import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
import numpy

'''Probit analysis plus plotting 3D graph of hit rate distribution with respect to delta and theta'''

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Receive Data
data = pd.read_csv("HL.csv")
print(data)
col = ["delta","epsilon","cross_term"]
dep_var = data["hits"].tolist()
X = data[col]
theta  = data["theta"]

z = Probit(dep_var, X)
result=z.fit()
print(result.summary())

z = np.array(data["hits"].tolist())
x = np.array(data["epsilon"].tolist())
y = np.array(data["delta"].tolist())
print(z)
ax.scatter(x,y,z ,s=1, c=None, depthshade=True)
plt.show()

