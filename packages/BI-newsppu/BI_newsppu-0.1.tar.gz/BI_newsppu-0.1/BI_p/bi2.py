# Import required libraries

print("""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
import seaborn as sns

# Load the Iris dataset
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)

# (Optional) Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)  # n_init=10 is default for sklearn 1.4+
kmeans.fit(X_scaled)

# Add the cluster labels to the original dataset
X['Cluster'] = kmeans.labels_

# Visualize the Clusters (using the first two features for 2D plot)
plt.figure(figsize=(8,6))
sns.scatterplot(x=X.iloc[:, 0], y=X.iloc[:, 1], hue=X['Cluster'], palette='Set1', s=60)
plt.title('K-Means Clustering of Iris Dataset (based on Sepal features)')
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Sepal Width (cm)')
plt.legend(title='Cluster')
plt.grid(True)
plt.show()

# Optional: compare clusters with actual species
# (Just for understanding - not part of clustering)
df_clusters = pd.DataFrame({
    'Actual Species': iris.target,
    'Cluster Label': kmeans.labels_
})
print("\nCluster Labels vs Actual Species:\n")
print(df_clusters.value_counts().sort_index())

""")