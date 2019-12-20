#!/usr/bin/env python
#coding=utf8
# пример реализации взят с habr.com/ru/post/329604
import matplotlib.pyplot as plt
import numpy as np
from threading import Thread 
from numpy import sqrt
from queue import Queue
def foo(i):
    for j in np.arange(0,i,1):
        M[way[i],way[j]]=float('inf')
def foo2(i, q):
    X1.append(X[way[i]])
    Y1.append(Y[way[i]])
    s1 = q.get()
    s1 = s1 + sqrt((X[way[i-1]]-X[way[i]])**2+(Y[way[i-1]]-Y[way[i]])**2)  #
    q.put(s1)


n = 50;m = 100;ib = 9;way = [];a = 0
#X=np.random.uniform(a,m,n)
#Y=np.random.uniform(a,m,n)
X = [10, 10, 100,100 ,30, 20, 20, 50, 50, 85, 85, 75, 35, 25, 30, 47, 50]
Y = [5,  85, 0,  90,  50, 55, 50, 75 ,25, 50, 20, 80, 25, 70, 10, 50, 100]
X1 = []
Y1 = []
s1 = 0
n=len(X)
M = np.zeros([n,n]) # Шаблон матрицы относительных расстояний между пунктами
for i in np.arange(0,n,1):
         for j in np.arange(0,n,1):
                  if i!=j:
                           M[i,j]=sqrt((X[i]-X[j])**2+(Y[i]-Y[j])**2)# Заполнение матрицы
                  else:
                           M[i,j]=float('inf')#Заполнение главной диагонали матрицы           
way.append(ib)
X1.append(X[way[0]])
Y1.append(Y[way[0]])
q = Queue()
q.put(s1)
for i in np.arange(1,n,1):
         s=[]
         for j in np.arange(0,n,1):                                             #Данный участок нельзя расппараллелить с остальным кодом, поскольку дальнейшие вычисления зависят от полученного здесь результата   
                  s.append(M[way[i-1],j])
         way.append(s.index(min(s)))# Индексы пунктов ближайших городов соседей
         #for j in np.arange(0,i,1):                                             # Участок который можно распараллелить цикл => Thread foo()
         #        M[way[i],way[j]]=float('inf')                                  #
         #X1.append(X[way[i]])                                                   # Операции ниже => Thread foo2()  
         #Y1.append(Y[way[i]])                                                   #                                
         #s1 = s1 + sqrt((X[way[i-1]]-X[way[i]])**2+(Y[way[i-1]]-Y[way[i]])**2)  #
         thread1 = Thread(target=foo, args=[i])
         thread2 = Thread(target=foo2, args=[i,q])
         thread1.start()
         thread2.start()
         thread1.join()
         thread2.join()



s1=q.get()
s1 =  s1 + sqrt((X[way[n-1]]-X[way[0]])**2+(Y[way[n-1]]-Y[way[0]])**2)
assert round(s1,3)==532.326
plt.title('Общий путь-%s.Номер города-%i.Всего городов -%i.\n Координаты X,Y случайные числа от %i до %i'%(round(s1,3),ib,n,a,m), size=14)
#X1=[X[way[i]] for i in np.arange(0,n,1)]
#Y1=[Y[way[i]] for i in np.arange(0,n,1)]
plt.plot(X1, Y1, color='r', linestyle=' ', marker='o')
plt.plot(X1, Y1, color='b', linewidth=1)   
X2=[X[way[n-1]],X[way[0]]]
Y2=[Y[way[n-1]],Y[way[0]]]
plt.plot(X2, Y2, color='g', linewidth=2,  linestyle='-', label='Путь от  последнего \n к первому городу') 
plt.legend(loc='best')
plt.grid(True)
plt.show()
