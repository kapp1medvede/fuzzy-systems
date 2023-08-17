
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

n = 1
m = 1
def Imagenhacement(e_layer,lamdas,means,ws):
    new_image = np.zeros(e_layer.shape)
    width = e_layer.shape[1]
    height = e_layer.shape[0]
    for i in range(m):
        for j in range(n):
            res=(e_layer-means[i, j])/(1-(e_layer*means[i, j])+0.000001)
            s = (1+res)**lamdas[i, j]
            z = (1-res)**lamdas[i, j]
            win = (s-z)/(s+z)
            w1 = ws[i, j].T.copy()
            for k in range(width):
                for l in range(height):
                    s = (1+ win[l, k])**w1[l, k]
                    z = (1- win[l, k])**w1[l, k]
                    res = (s-z)/(s+z)
                    new_image[l, k] = (new_image[l, k]+res)/(1+(new_image[l, k]*res)+0.000001)
    source=(-1,1)
    dest=(0,255)
    res_image = (dest[1] - dest[0])*((new_image - source[0]) / (source[1] - source[0])) + dest[0] 
    res_image = np.round(res_image)
    res_image = res_image.astype(np.uint8)
    return res_image
 
def window_means_variance(e_layer,w, i, j,WIDTH,HEIGHT,means):
        mean = 0
        for k in range(HEIGHT):
            for l in range(WIDTH):
                s = (1+e_layer[k, l])**w[i, j, l, k]
                z = (1-e_layer[k, l])**w[i, j, l, k]
                res = (s-z)/(s+z)
                mean = (mean+res)/(1+(mean*res))
        mean /= np.sum(w[i, j])
        variance = 0
        means[i,j]=mean
        for k in range(HEIGHT):
            for l in range(WIDTH):
                res=(e_layer[k, l]-means[i, j])/(1-(e_layer[k, l]*means[i, j])+0.000001)
                norm=abs(0.5 * np.log((1+res)/((1-res)+0.000001)))
                variance += w[i, j, l, k] * np.power(norm, 2)
        variance /= np.sum(w[i, j])
        return variance

def imageFuzzy(path):
    img = cv2.imread(path)
    img=cv2.resize(img,(300,300))
    WIDTH = img.shape[1]
    HEIGHT = img.shape[0]
    x0, x1, y0, y1 = 0, WIDTH - 1, 0, HEIGHT - 1
    layer_b, layer_g, layer_r = cv2.split(img)
    dest=(-1,1)
    source=(0,255)
    e_layer_b=(dest[1] - dest[0])*((layer_b - source[0]) / (source[1] - source[0])) + dest[0]
    e_layer_g=(dest[1] - dest[0])*((layer_g - source[0]) / (source[1] - source[0])) + dest[0]
    e_layer_r=(dest[1] - dest[0])*((layer_r - source[0]) / (source[1] - source[0])) + dest[0]
    res = (e_layer_b+ e_layer_g)/(1+(e_layer_b*e_layer_g)+0.000001)
    res=(res+ e_layer_r)/(1+(res * e_layer_r)+0.000001)
    scalar=1/3
    s = (1+res)**scalar
    z = (1-res)**scalar
    e_layer_rgb = (s-z)/(s+z+0.000001) 
    
    ps= np.zeros((m, n,WIDTH,HEIGHT))
    for i in range(m):
        for j in range(n):
            for k in range(WIDTH-1):
                for l in range(HEIGHT-1):    
                    c=math.factorial(m)/((math.factorial(i)*math.factorial(m-i))+0.000001)
                    qx =  c*(np.power((k-x0)/(x1-k), i) * np.power((x1-k)/(x1-x0), m)) 
                    c=math.factorial(m)/((math.factorial(j)*math.factorial(m-j))+0.000001)
                    qy= c*(np.power((l-y0)/(y1-l), j) * np.power((y1-l)/(y1-y0), n))
                    ps[i, j, k, l] = qx * qy
    
    
    ws = np.zeros((m, n, WIDTH, HEIGHT))
    gamma=1
    for i in range(m):
        for j in range(n):
            psgamma = np.power(ps[i, j], gamma)
            for k in range(WIDTH):
                for l in range(HEIGHT):    
                    ws[i, j, k, l] = psgamma[k, l] / (np.sum(ps[:, :, k, l])+0.000001)
        
    means = np.zeros((m, n))
    variances = np.zeros((m, n))
    lamdas = np.zeros((m, n))  
    variance = 0.35
    for i in range(m):
        for j in range(n):
            variances[i, j] = window_means_variance(e_layer_rgb,ws, i, j,WIDTH,HEIGHT,means)
            lamdas[i, j] = np.sqrt(variance) / (np.sqrt(variances[i, j])+0.000001)   
     
    res_r = Imagenhacement(e_layer_r,lamdas,means,ws)
    res_g = Imagenhacement(e_layer_g,lamdas,means,ws)
    res_b = Imagenhacement(e_layer_b,lamdas,means,ws)
    res_img = cv2.merge([res_b, res_g, res_r])
    plt.figure(figsize=(10, 10))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(res_img, cv2.COLOR_BGR2RGB))
    plt.title('Fuzzy image')
    plt.show()


    

path = "4.jpg"    
imageFuzzy(path)
