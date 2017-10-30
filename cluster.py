from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def find_number_of_kmean():
    colors = ['b', 'g', 'r']
    markers = ['o', 'v', 's']
    # k means determine k
    df = pd.read_csv('num_X.csv').iloc[:, 1:]
    distortions = []
    K = range(1, 30)
    for k in K:
        kmeanModel = KMeans(n_clusters=k)
        kmeanModel.fit(df)
        distortions.append(sum(np.min(
            cdist(df, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / df.shape[0])

    # Plot the elbow
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method showing the optimal k')
    plt.show()


if __name__ == "__main__":

	num_x = np.loadtxt("num_X.csv", skiprows=1, delimiter=',')[:, 1:]
	car_detail_df = pd.read_csv('refinedDataWithEncode.csv').iloc[:, 1:]
	kmeanModel = KMeans(n_clusters=30, random_state=66)
	kmeanModel.fit(num_x)
	label = kmeanModel.labels_
	car_detail_df['label'] = pd.Series(label, index=car_detail_df.index)
	car_detail_df.to_csv("car_detail_df.csv",index=False)

