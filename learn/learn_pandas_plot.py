import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


'''
#Series线性
data = pd.Series(np.random.randn(1000),index=np.arange(1000))
data =data.cumsum()
data.plot()
plt.show()
'''

'''
#DataFrame
data = pd.DataFrame(np.random.randn(1000,4),index=
                    np.arange(1000),columns=list("ABCD"))
data =data.cumsum()
data.plot()
plt.show()
'''

'''
data = pd.DataFrame(np.random.randn(1000,4),index=
                    np.arange(1000),columns=list("ABCD"))
data =data.cumsum()
ax = data.plot.scatter(x='A',y='B',color='DarkBlue',label='Class 1')
data.plot.scatter(x='A',y='C',color='DarkGreen',label='Class 2',ax=ax)
plt.show()
'''
