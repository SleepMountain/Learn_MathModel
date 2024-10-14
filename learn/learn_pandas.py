import numpy as np
import pandas as pd
'''
s = pd.Series([1,3,6,np.nan,44,1])
print(s)
'''


'''
dates = pd.date_range('20160101',periods=6)
print(dates)
'''

'''
dates = pd.date_range('20130101',periods=6)
df = pd.DataFrame(np.arange(24).reshape((6,4)),index=dates,columns=['A','B','C','D'])
print(df)
'''

'''
print(df['A'],df.A)
print(df[0:3],df['20130102':'20130104'])
print(df.loc['20130102'])
print(df.loc[:,['A','B']])
'''

'''
print(df.iloc[3])
print(df.iloc[[1,3,5],1:3])
'''

'''
print(df[df.A>8])
'''

'''
df.iloc[2,2]=1111
df.loc['20130101','B']=2222
df.B[df.A>4] = 0
df['F'] =np.nan
df['E'] =pd.Series([1,2,3,4,5,6],index=pd.date_range('20130101',periods=6))
print(df)
'''

'''
print(np.any(df.isnull())==True)
'''

'''
data = pd.read_csv('url')
data.to_pickle('url')
'''

'''
df1 = pd.DataFrame(np.ones((3,4))*0,columns=['a','b','c','d'])
df2 = pd.DataFrame(np.ones((3,4))*1,columns=['a','b','c','d'])
df3 = pd.DataFrame(np.ones((3,4))*2,columns=['a','b','c','d'])
print(df1)
print(df2)
print(df3)
res = pd.concat([df1,df2,df3],axis=0,ignore_index=True)
print(res)
'''

'''
df1 = pd.DataFrame(np.ones((3,4))*0,columns=['a','b','c','d'],index=[1,2,3])
df2 = pd.DataFrame(np.ones((3,4))*1,columns=['b','c','d','e'],index=[2,3,4])
print(df1)
print(df2)
res1= pd.concat([df1,df2],join='outer')
res2 = pd.concat([df1,df2],join='inner',ignore_index=True)
print(res1)
print(res2)
'''

'''
res = pd.merge(df1,df2,on=['key1','key2'],how='inner' indictor='new_name')
print(res)
'''

'''
boys = pd.DataFrame({'k':['K0','K1','K2','K3'],'age':[4,5,6]})
girls = pd.DataFrame({'k':['K0','K1','K2','K3'],'age':[1,2,3]})
print(boys)
print(girls)
res = pd.merge(boys,girls,on='k',suffixes=['_boy','_girl'],how='inner')
print(res)
'''
