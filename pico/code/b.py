import numpy as np 
a = [1.65,2.2569,3.000259,4.1458,5.369852,6.14528]
#求均值
a_mean = np.mean(a)
#求方差
a_var = np.var(a)
#求标准差
a_std = np.std(a,ddof=1)
print("平均值为：%f" % a_mean)
print("方差为：%f" % a_var)
print("标准差为:%f" % a_std)
print(max(a))