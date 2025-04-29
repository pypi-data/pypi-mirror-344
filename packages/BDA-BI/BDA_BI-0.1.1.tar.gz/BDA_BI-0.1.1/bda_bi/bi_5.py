print("""# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn.preprocessing import StandardScaler

# Step 1: Load the Iris dataset
iris = datasets.load_iris()
X = iris.data  # Features: sepal length, sepal width, petal length, petal width
feature_names = iris.feature_names

# Step 2: Preprocessing
# Standardize the features (important for K-Means)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 3: Apply K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42)  # We know there are 3 species
kmeans.fit(X_scaled)
labels = kmeans.labels_

# Step 4: Add cluster labels to a DataFrame for analysis
df = pd.DataFrame(X, columns=feature_names)
df['Cluster'] = labels

# Step 5: Visualize the Clusters
plt.figure(figsize=(8,6))
plt.scatter(X_scaled[:, 2], X_scaled[:, 3], c=labels, cmap='viridis', s=50)
plt.xlabel('Petal Length (standardized)')
plt.ylabel('Petal Width (standardized)')
plt.title('K-Means Clustering of Iris Dataset')
plt.show()

# Step 6: Print Cluster Centers
print("Cluster Centers (standardized features):")
print(kmeans.cluster_centers_)""")

