# -*- coding: utf-8 -*-
"""Problem 2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1svTW07drKwOYhx307PcIHBwwudaPOyTa
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('/content/problem 2.csv')

pd.set_option('display.max_columns',None)

df.head(1)

df.info()

df.isnull().sum()

plt.figure(figsize=(10,6))
sns.heatmap(df.isnull(),yticklabels=False,cmap='viridis')

df.columns

df['Dateofjoining'] = pd.to_datetime(df['Dateofjoining'])
df['LastWorkingDate'] = pd.to_datetime(df['LastWorkingDate'])

df['Year_of_join'] = df['Dateofjoining'].apply(lambda t:t.year)
df['Month_of_join'] = df['Dateofjoining'].apply(lambda t:t.month)
df['Day_of_join'] = df['Dateofjoining'].apply(lambda t:t.day)
df['Year_of_leave'] = df['LastWorkingDate'].apply(lambda t:t.year)
df['Month_of_leave'] = df['LastWorkingDate'].apply(lambda t:t.month)

df.drop(columns='Dateofjoining',inplace=True)

df['Attrition'] = np.nan

mypop = df.pop('Attrition')
df.insert(1,'Attrition',mypop)
mypop1 = df.pop('Year_of_join')
df.insert(8,'Year_of_join',mypop1)
mypop2 = df.pop('Month_of_join')
df.insert(9,'Month_of_join',mypop2)
mypop3 = df.pop('Day_of_join')
df.insert(10,'Day_of_join',mypop3)

df = df.astype({'Year_of_join':int,'Month_of_join':int,'Day_of_join':int})

df['Attrition']=np.where(df['LastWorkingDate'].isnull(),0,1)

df.drop(columns='LastWorkingDate',inplace=True)

df.head(3)

plt.figure(figsize=(10,6))
sns.countplot(data=df,x='Gender',hue='Education_Level')

joiners = df.groupby(by=['Year_of_join','Month_of_join']).count()['Emp_ID'].unstack()

plt.figure(figsize=(10,6))
sns.heatmap(joiners,annot=True,fmt='.4g',cmap='magma')

df['Attrition'].value_counts()

leavers = df.groupby(by=['Year_of_leave','Month_of_leave']).count()['Emp_ID'].unstack()

plt.figure(figsize=(10,6))
sns.heatmap(leavers,annot=True,fmt='.4g',cmap='magma')

sns.jointplot(data=df,x='Age',y='Salary',hue='Gender',height=10)

plt.figure(figsize=(10,6))
fg = sns.FacetGrid(df, col="Gender",  row='Year_of_join')
fg.map(sns.scatterplot, "Salary", "Age")

df.groupby(by=['Education_Level','Gender','Attrition','City']).count()['Emp_ID'].unstack()

sns.jointplot(data=df,x='Age',y='Salary',hue='Attrition',height=10)

plt.figure(figsize=(10,6))
fg = sns.FacetGrid(df, col="Attrition",  row='Year_of_join')
fg.map(sns.scatterplot, "Salary", "Age")

plt.figure(figsize=(10,6))
fg = sns.FacetGrid(df, col="Quarterly Rating",  row='Attrition')
fg.map(sns.scatterplot, "Salary", "Age")

df['Length_of_work'] = df['Year_of_leave'] - df['Year_of_join']

sns.jointplot(data=df,x='Age',y='Salary',hue='Length_of_work',height=10)

plt.figure(figsize=(10,6))
fg = sns.FacetGrid(df, col="Length_of_work",  row='Attrition')
fg.map(sns.scatterplot, "Salary", "Age")

plt.figure(figsize=(10,6))
fg = sns.FacetGrid(df, col="Length_of_work",  row='Gender')
fg.map(sns.scatterplot, "Salary", "Age")

sns.jointplot(data=df,x='Age',y='Total Business Value',hue='Attrition',height=10)

sns.jointplot(data=df,x='Age',y='Total Business Value',hue='Gender',height=10)

df.info()

df.head(1)

sex = pd.get_dummies(df['Gender'],drop_first=True)
city = pd.get_dummies(df['City'])
edu = pd.get_dummies(df['Education_Level'])

train = df.copy()

train.head(1)

train.drop(columns=['MMM-YY','Emp_ID','Gender','City','Education_Level','Joining Designation','Designation','Year_of_leave','Month_of_leave','Length_of_work'],inplace=True)

train = pd.concat([train,sex,city,edu],axis=1)

x = train.drop('Attrition',axis=1)
y = train['Attrition']

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.5)

from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression(solver='liblinear')

logreg.fit(x_train,y_train)

logreg_pred = logreg.predict(x_test)

from sklearn.metrics import classification_report, confusion_matrix

viz_str = '-'* 20
print(viz_str,'LOGISTIC REGRESSION',viz_str)
print('Classification report:')
print(classification_report(y_test,logreg_pred))
print('-'*61)
plt.title('Confusion Matrix')
sns.heatmap(confusion_matrix(y_test,logreg_pred),annot=True,fmt='g',cmap='cubehelix',cbar=False, yticklabels=False, xticklabels=False)

from sklearn.tree import DecisionTreeClassifier

dtree = DecisionTreeClassifier()

dtree.fit(x_test,y_test)

dtree_pred = dtree.predict(x_test)

viz_str = '-'* 20
print(viz_str,'DECISION TREE',viz_str)
print('Classification report:')
print(classification_report(y_test,dtree_pred))
print('-'*61)
plt.title('Confusion Matrix')
sns.heatmap(confusion_matrix(y_test,dtree_pred),annot=True,fmt='g',cmap='cubehelix',cbar=False, yticklabels=False, xticklabels=False)

from sklearn.ensemble import RandomForestClassifier

rndfrst = RandomForestClassifier(n_estimators=100)

rndfrst.fit(x_train,y_train)

rndfrst_pred = rndfrst.predict(x_test)

viz_str = '-'* 20
print(viz_str,'RANDOM FOREST',viz_str)
print('Classification report:')
print(classification_report(y_test,rndfrst_pred))
print('-'*61)
plt.title('Confusion Matrix')
sns.heatmap(confusion_matrix(y_test,rndfrst_pred),annot=True,fmt='g',cmap='cubehelix',cbar=False, yticklabels=False, xticklabels=False)

from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

param_grid = {'C':[0.01,0.1,1,10],'gamma':[1,0.01,0.001]}

svm = SVC()

grid = GridSearchCV(SVC(),param_grid,verbose=3)

grid.fit(x_train,y_train)

grid.best_params_

final_svm = SVC(C=1, gamma=0.01)

final_svm.fit(x_train,y_train)

svm_pred = final_svm.predict(x_test)

viz_str = '-'* 20
print(viz_str,'KNN',viz_str)
print('Classification report:')
print(classification_report(y_test,svm_pred))
print('-'*55)
plt.title('Confusion Matrix')
sns.heatmap(confusion_matrix(y_test,svm_pred),annot=True,fmt='g',cmap='cubehelix',cbar=False, yticklabels=False, xticklabels=False)

