'''
本篇我也會寫在notion
參考的是https://ithelp.ithome.com.tw/articles/10197110
'''
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

iris = datasets.load_iris()
iris_data=iris.data
iris_label=iris.target
print("www")
'''
上方
將iris的data跟label載入
'''
train_data , test_data , train_label , test_label = train_test_split(iris_data,iris_label,test_size=0.2)
'''
上方
將資料分成兩個部分 一部分train 一部分test
print(iris_label)
print(iris_data)
'''
knn = KNeighborsClassifier()
knn.fit(train_data,train_label)
print(knn.predict(test_data))
print(test_label)
'''
第一行用KNN分類法
第二行做訓練
'''
'''
for i in range(a):
    b+=1
    print(knn.predict(test_data))
    print(test_label)
    print(b)
    
    
b=0
list_answer=knn.predict(test_data).all(keepdims=True)
list_test=knn.predict(test_data).sum(axis=0,keepdims=True)
print(list_answer)
print(list_test)
for i in range(len(list_answer)):
    if list_answer[i] == list_test[i]:
        print("true")
    else :
        print("false")
    '''