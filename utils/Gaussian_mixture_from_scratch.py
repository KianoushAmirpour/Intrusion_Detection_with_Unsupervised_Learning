import numpy as np
from sklearn.cluster import KMeans

def multivariate_gaussian(X, mu, cov_mat):
    
    n = X.shape[1]
    X = (X - mu)
    
    assert mu.shape == (n,)
    assert cov_mat.shape == (n,n)

    part_1 = 1 / ((2 * np.pi)** (n/2) * (np.linalg.det(cov_mat) ** 0.5))
    
    inv_mat = np.linalg.inv(cov_mat)
    part_2 = np.exp(-0.5 * np.sum(np.dot(X, inv_mat) * X, axis=1))

    P = part_1  * part_2
    
    return P

def initialize(X, num_clusters):
    
    # using kmeans centroids to initialize the Gmm
    
    kmeans = KMeans(num_clusters)
    kmeans.fit(X)
    centroids = kmeans.cluster_centers_
    
    clusters = []
    
    for i in range(num_clusters):
        
        clusters.append({"pi_k" : 1 / num_clusters,
                        "mean_k" : centroids[i],
                        "cov_k": np.identity(X.shape[1])})
    
    return clusters   

def E_step(X, clusters):
    
    global gamma, total
    
    num_clusters = len(clusters)
    
    gamma = np.zeros((X.shape[0], num_clusters))
    
    for i, cluster in enumerate(clusters):
        
        pi = cluster["pi_k"]
        mean = cluster["mean_k"]
        cov = cluster["cov_k"]
        
        gamma[:, i] = pi * multivariate_gaussian(X, mean, cov)
    
    total = np.sum(gamma, axis=1)[:, np.newaxis]
    
    gamma = gamma / total
    
def M_step(X , clusters):
    
    global gamma
    
    for i, cluster in enumerate(clusters):
        
        gamma_k = gamma[:,i][:,np.newaxis]
        
        pi_k = np.mean(gamma_k, axis=0)
        
        mean_k = np.sum(gamma_k * X, axis=0) / np.sum(gamma_k, axis=0)
        
        cov_k = (gamma_k * (X - mean_k)).T @ (X- mean_k) / np.sum(gamma_k, axis=0)
        
        cluster["pi_k"] = pi_k
        cluster["mean_k"] = mean_k
        cluster["cov_k"] = cov_k

def get_liklihood(X, clusters):
    
    global gamma, total
    
    sample_liklihood = np.log(total)
    return np.sum(sample_liklihood), sample_liklihood

def train(X, num_clusters, n_epochs):
    
    clusters = initialize(X , num_clusters)
    liklihoods = np.zeros((n_epochs,))
    
    for i  in range(n_epochs):
        E_step(X, clusters)
        M_step(X,clusters)
        
        liklihood, sample_liklihoods = get_liklihood(X, clusters)
        liklihoods[i] = liklihood
        print("Epoch", i+1, "Likelihood", liklihood)
    return liklihoods


