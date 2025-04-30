import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split , GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report , confusion_matrix , roc_auc_score , roc_curve , accuracy_score
from sklearn.preprocessing import StandardScaler , LabelEncoder

df = pd.read_csv("titanic.csv")

print(df.head())

print(df.isnull().sum())

df.drop(columns = ['Name','PassengerId','Cabin','Ticket'] , inplace = True)

df['Age'].fillna(df['Age'].median() , inplace = True)
df['Embarked'].fillna(df['Embarked'].mode()[0],inplace=True)

print(df.isnull().sum())


df['Sex'] = LabelEncoder().fit_transform(df['Sex'])
df = pd.get_dummies(df,columns=['Embarked'],drop_first=True)


df['FamilySize'] = df['SibSp'] + df['Parch'] +1
df.drop(columns=['SibSp','Parch'] , inplace = True)

df.head()

scaler = StandardScaler()
scaled_features = scaler.fit_transform(df.drop('Survived',axis=1))
x = pd.DataFrame(scaled_features, columns=df.drop('Survived',axis=1).columns)
y= df['Survived']

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=42)

model = LogisticRegression()
params = {
    'C' : [0.01,0.1,1,10],
    'solver' : ['liblinear','lbfgs']
}
grid = GridSearchCV(model, param_grid=params , cv = 5, scoring='accuracy')
grid.fit(x_train,y_train)

best_model = grid.best_estimator_



y_pred = best_model.predict(x_test)
print("Confusion Matrix: \n" , confusion_matrix(y_test , y_pred))
print("\nClassification Report:\n", classification_report(y_test,y_pred))
print("Accuracy:" , accuracy_score(y_test,y_pred))


y_probs = best_model.predict_proba(x_test)[:,1]
auc_score = roc_auc_score(y_test , y_probs)
fpr , tpr , thresholds = roc_curve(y_test , y_probs)
plt.figure(figsize=(6,4))
plt.plot(fpr,tpr,label=f"Logistic regression (AUC = {auc_score:.2f})")
plt.plot([0,1],[0,1],linestyle='--')
plt.xlabel("false positive rate")
plt.ylabel("true positive rate")
plt.title("roc curve")
plt.legend()
plt.grid()
plt.show()



plt.figure(figsize=(6,4))
sns.heatmap(df.corr(),annot=True,cmap = 'coolwarm',fmt='.2f')
plt.title("Correlation Heatmaop of features", fontsize=14)
plt.show()


sns.countplot(x='Survived',data=df,palette='Set2')
plt.title("survival Distribution",fontsize=14)
plt.xlabel("Survived(0 = No , 1 = yes)")
plt.ylabel("count")
plt.grid(axis='y')
plt.show()


sns.barplot(x='Sex' , y = 'Survived', data = df , palette = 'muted')
plt.xticks([0,1], ['Male','Female'])
plt.title("Survival Rate by Gender",fontsize = 14)
plt.ylabel("Survival probality")
plt.show()


plt.figure(figsize = (6,4))
sns.violinplot(x='Survived',y='Fare',data=df,palette = 'Set3')
plt.title("fare dist by survival status")
plt.xlabel("survived")
plt.ylabel("fare")
plt.show()


ct = pd.crosstab(df['Pclass'],df['Survived'], normalize='index')*100
ct.plot(kind='bar',stacked=True,colormap='viridis',figsize=(5,4))
plt.title("survival rate by passenger class(%)",fontsize = 14)
plt.ylabel("Percentage")
plt.xlabel("passenger class")
plt.legend(["Did not survive", "survived"])
plt.grid(axis='y')
plt.show()