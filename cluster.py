from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.externals import joblib


def find_number_of_kmean():
    colors = ['b', 'g', 'r']
    markers = ['o', 'v', 's']
    # k means determine k
    df = pd.read_csv('num_X.csv').iloc[:, 1:]
    distortions = []
    K = range(1, 15)
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

def create_csv_with_label(model):
    label = model.labels_
    car_detail_df = pd.read_csv('refinedDataWithEncode.csv').iloc[:, 1:]
    car_detail_df['label'] = pd.Series(label, index=car_detail_df.index)
    car_detail_df.to_csv("car_detail_df.csv",index=False)

def create_model_file(model):
    joblib.dump(model, 'km_2.pkl')


if __name__ == "__main__":
    k = 15
    random_seed = 66
    num_x = np.loadtxt("num_X.csv", skiprows=1, delimiter=',')[:, 1:]
    kmeanModel = KMeans(n_clusters=k, random_state=random_seed)
    kmeanModel.fit(num_x)
    # create_csv_with_label(kmeanModel)
    create_model_file(kmeanModel)

