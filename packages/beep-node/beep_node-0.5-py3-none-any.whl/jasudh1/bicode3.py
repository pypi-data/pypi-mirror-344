import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


iris = load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)


scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)


wcss = []
K = range(1,11)
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    wcss.append(kmeans.inertia_)

    
kmeans = KMeans(n_clusters = 3 , random_state=42)
clusters = kmeans.fit_predict(scaled_data)


df['Cluster'] = clusters

print(df.head())

plt.figure(figsize=(8,5))
sns.scatterplot(x=df[iris.feature_names[0]],
                y=df[iris.feature_names[1]],
                hue=df['Cluster'],palette='Set1')
plt.title("K-Means Clustering Results")
plt.xlabel(iris.feature_names[0])
plt.ylabel(iris.feature_names[1])
plt.legend()
plt.show()


score =  silhouette_score(scaled_data, clusters)
print("Silhouette Score:",score)