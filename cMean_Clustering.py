import numpy as np
import matplotlib.pyplot as plt  
import cv2 
import skfuzzy 
 
def cMeansAlgorithm(data,n_clusters,m = 2,min_err = 0.001,max_iter = 100):
    pre_c=0 
    u = np.random.random((n_clusters, data.shape[0]))    
    for i in range(max_iter): 
        mf = np.power(u,m)
        c = np.divide(np.dot(mf,data),sum(mf.T).reshape(n_clusters,1))
        diff = np.zeros((c.shape[0], data.shape[0])) 
        for k in range(c.shape[0]):
            diff[k, :] = np.sqrt(sum(np.power(data-np.dot(np.ones((data.shape[0], 1)),np.reshape(c[k, :],(1,c.shape[1]))),2).T))
        diff = np.power(diff,(-2/(m-1))) 
        u = np.divide(diff,np.reshape(sum(diff),(1,diff.shape[1])))
        if i> 0:
            if np.amax(c - pre_c) < min_err:
                break
        pre_c=c; 
    u = np.argmax(u,axis=0)  
    return u,c

    
def cMeans(data, labels_true,number_of_clusters,m = 2,min_err = 0.001,max_iter = 500):  
    u,c = cMeansAlgorithm(data,number_of_clusters,m,min_err,max_iter) 
    figure,ax = plt.subplots(ncols=3, constrained_layout=True,figsize=(9,4)) 
    alldata = np.vstack((data[:,0], data[:,1]))
    if len(data[0])>2:
        alldata = np.vstack((data[:,0], data[:,1], data[:,2]))
    cluster_centers_kmeans,u2= skfuzzy.cluster.cmeans(alldata, number_of_clusters, 2, error=0.001, maxiter=1000, init=None)[:2]

    for i in range(number_of_clusters):
        indx = np.where((labels_true==i))
        ax[0].scatter(data[indx,0],data[indx,1])
        ax[0].set_title('Original')

    for i in range(number_of_clusters):
        indx = np.where((u==i))
        ax[1].scatter(data[indx,0],data[indx,1])
        ax[1].set_title('cMean_Clustering')
    ax[1].scatter(c[:, 0], c[:, 1], c='black', s=200, alpha=0.7)
    cluster_membership = np.argmax(u2, axis=0)

    for i in range(number_of_clusters):
        indx = np.where((cluster_membership==i))
        ax[2].scatter(data[indx,0],data[indx,1])
        ax[2].set_title('cMean_Clustering_using lib')
    ax[2].scatter(cluster_centers_kmeans[:, 0], cluster_centers_kmeans[:, 1], c='black', s=200, alpha=0.7)

    plt.show() 
    return c,u,cluster_centers_kmeans,cluster_membership






def imageCMeans(path,labels_true,number_of_clusters):
    image = cv2.imread(path)
    image=cv2.resize(image,(300,300))  
    image_2d = image.reshape(image.shape[0] * image.shape[1], image.shape[2])
    cluster_centers_cmeans,output,cluster_centers_cmeans2,output2 =cMeans(image_2d, labels_true,number_of_clusters) 
    plt.figure(figsize=(13, 13))
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.subplot(1, 3, 2)
    plt.imshow(cluster_centers_cmeans[output].astype(np.int32).reshape(image.shape))
    plt.title('cMeans image')
    plt.subplot(1, 3, 3)
    plt.imshow(cluster_centers_cmeans2[output2].astype(np.int32).reshape(image.shape))
    plt.title('cMean_Clustering_using lib')
    plt.show()  
 