import numpy as np
from scipy.linalg import norm
import matplotlib.pyplot as plt  
import cv2

def gustafsonAlgorithm(data, n_clusters=4,m = 2,min_err = 0.001,max_iter = 500):
    pre_c=0 
    u = np.random.random((n_clusters, data.shape[0]))  
    u = np.divide(u,np.dot(np.ones((n_clusters,1)),np.reshape(sum(u),(1,data.shape[0]))))
    for i in range(max_iter): 
        mf = np.power(u,m) 
        d=sum(mf.T).reshape(n_clusters,1)
        c = np.divide(np.dot(mf,data),d)  
        diff=data.reshape(data.shape[0], 1, -1) - c.reshape(1, c.shape[0], -1)
        temp = np.expand_dims(diff, axis=3)
        temp = np.matmul(temp, temp.transpose((0, 1, 3, 2)))
        numerator = mf.T.reshape(mf.shape[1], mf.shape[0], 1, 1) * temp
        f = sum(numerator,1) / d.reshape(-1, 1, 1)
        diff =np.expand_dims(diff, axis=3) 
        determ = np.power(np.linalg.det(f), 1 / m)
        det_time_inv = determ.reshape(-1, 1, 1) * np.linalg.pinv(f)
        temp = np.matmul(diff.transpose((0, 1, 3, 2)), det_time_inv) 
        dist = np.matmul(temp, diff).reshape(data.shape[0],n_clusters)     
        d = dist.reshape((dist.shape[0], 1, -1))  
        u = np.power(np.divide(dist[:, None, :] , d.transpose((0, 2, 1))), 1 / (m - 1))
        u = np.divide(1 , u.sum(1)).T 
        if i> 0:
            if np.amax(c - pre_c) < min_err:
                break
        pre_c=c;
    u = np.argmax(u,axis=0)
    return u,c
    
def gustafson(data, labels_true,number_of_clusters,m,min_err,max_iter):  
    u ,centers= gustafsonAlgorithm(data, number_of_clusters,m,min_err,max_iter) 
    figure,ax = plt.subplots(ncols=2, constrained_layout=True) 
    for i in range(number_of_clusters):
        indx = np.where((labels_true==i))
        ax[0].scatter(data[indx,0],data[indx,1])
        ax[0].set_title('Original')
    for i in range(number_of_clusters):
        indx = np.where((u==i))
        ax[1].scatter(data[indx,0],data[indx,1])
        ax[1].set_title('gustafson_Clustering')
    ax[1].scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.7)
    plt.show()  
    return centers,u 

def imagegustafson(path,labels_true,number_of_clusters):
    image = cv2.imread(path)
    image=cv2.resize(image,(300,300))  
    image_2d = image.reshape(image.shape[0] * image.shape[1], image.shape[2])
    cluster_centers_cmeans,output =gustafson(image_2d, labels_true,number_of_clusters,m = 2,min_err = 0.001,max_iter = 500) 
    plt.figure(figsize=(13, 13))
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.subplot(1, 3, 2)
    plt.imshow(cluster_centers_cmeans[output].astype(np.int32).reshape(image.shape))
    plt.title('gustafson image') 
 