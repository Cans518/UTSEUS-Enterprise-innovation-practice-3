import cv2
import numpy as np
from PIL import Image

def Histogram(image_1, image_2):
    # 计算单通道直方图
    channels = [0]
    hist_1 = cv2.calcHist([image_1], channels, None, [256], [0.0, 255.0])
    hist_2 = cv2.calcHist([image_2], channels, None, [256], [0.0, 255.0])

    # 计算直方图的重合度
    """
    degree = 0
    for i in range(len(hist_1)):
        if hist_1[i] != hist_2[i]:
            degree = degree + (1 - abs(hist_1[i] - hist_2[i]) / max(hist_1[i], hist_2[i]))
        else:
            degree = degree + 1

    degree = degree / len(hist_1)
    """
    degree = cv2.compareHist(hist_1, hist_2, method=cv2.HISTCMP_CORREL)
    degree = abs(degree)
    return degree

def correlation(image, kernal):
    kernal_heigh = kernal.shape[0]
    kernal_width = kernal.shape[1]
    cor_heigh = image.shape[0] - kernal_heigh + 1
    cor_width = image.shape[1] - kernal_width + 1
    result = np.zeros((cor_heigh, cor_width), dtype=np.float64)
    for i in range(cor_heigh):
        for j in range(cor_width):
            result[i][j] = (image[i:i + kernal_heigh, j:j + kernal_width] * kernal).sum()
    return result

def gaussian_2d_kernel(kernel_size=11, sigma=1.5):
    kernel = np.zeros([kernel_size, kernel_size])
    center = kernel_size // 2

    if sigma == 0:
        sigma = ((kernel_size - 1) * 0.5 - 1) * 0.3 + 0.8

    s = 2 * (sigma ** 2)
    sum_val = 0
    for i in range(0, kernel_size):
        for j in range(0, kernel_size):
            x = i - center
            y = j - center
            kernel[i, j] = np.exp(-(x ** 2 + y ** 2) / s)
            sum_val += kernel[i, j]
    sum_val = 1 / sum_val
    return kernel * sum_val

def ssim(image_1, image_2, window_size=11, gaussian_sigma=1.5, K1=0.01, K2=0.03, alfa=1, beta=1, gama=1):
    image_1 = cv2.cvtColor(image_1, cv2.COLOR_RGB2GRAY)
    image_2 = cv2.cvtColor(image_2, cv2.COLOR_RGB2GRAY)

    image_1=np.array(image_1,dtype=np.float64)
    image_2=np.array(image_2,dtype=np.float64)

    if not image_1.shape == image_2.shape:
        raise ValueError("Input Imagees must has the same size")

    if len(image_1.shape) > 2:
        raise ValueError("Please input the images with 1 channel")

    kernal=gaussian_2d_kernel(window_size,gaussian_sigma)

    # 求ux uy ux*uy ux^2 uy^2 sigma_x^2 sigma_y^2 sigma_xy等中间变量
    ux = correlation(image_1, kernal)
    uy = correlation(image_2, kernal)
    image_1_sqr = image_1 ** 2
    image_2_sqr = image_2 ** 2
    dis_mult_ori = image_1 * image_2

    uxx = correlation(image_1_sqr, kernal)
    uyy = correlation(image_2_sqr, kernal)
    uxy = correlation(dis_mult_ori, kernal)
    ux_sqr = ux ** 2
    uy_sqr = uy ** 2
    uxuy = ux * uy
    sx_sqr = uxx - ux_sqr
    sy_sqr = uyy - uy_sqr
    sxy = uxy - uxuy
    C1 = (K1 * 255) ** 2
    C2 = (K2 * 255) ** 2

    #常用情况的SSIM
    if(alfa==1 and beta==1 and gama==1):
        ssim=(2 * uxuy + C1) * (2 * sxy + C2) / (ux_sqr + uy_sqr + C1) / (sx_sqr + sy_sqr + C2)
        return np.mean(ssim)

    #计算亮度相似性
    l = (2 * uxuy + C1) / (ux_sqr + uy_sqr + C1)
    l = l ** alfa

    #计算对比度相似性
    sxsy = np.sqrt(sx_sqr) * np.sqrt(sy_sqr)
    c= (2 * sxsy + C2) / (sx_sqr + sy_sqr + C2)
    c= c ** beta

    #计算结构相似性
    C3 = 0.5 * C2
    s = (sxy + C3) / (sxsy + C3)
    s = s ** gama

    ssim = l * c * s
    return np.mean(ssim)

def Normalize(image, size=(64, 64), greyscale=False):
    # 重新设置图片大小
    image = cv2.resize(image, size, interpolation=cv2.INTER_CUBIC)
    if greyscale:
        # 将图片转换为灰度图，其每个像素用8个bit表示
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return image

# 计算两张图之间的余弦距离
def Cosine(image1, image2):
    image1 = Normalize(image1)
    image2 = Normalize(image2)

    image1 = Image.fromarray(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
    image2 = Image.fromarray(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))

    images = [image1, image2]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_tuple in image.getdata():
            vector.append(np.average(pixel_tuple))
        vectors.append(vector)
        norms.append(np.linalg.norm(vector, 2))

    a, b = vectors
    a_norm, b_norm = norms
    # dot返回的是点积，对二维数组（矩阵）进行计算
    res = np.dot(a / a_norm, b / b_norm)
    return res

if __name__ == '__main__':
    a = cv2.imread('pic/11.jpg')
    b = cv2.imread('pic/12.jpg')
    #a = cv2.cvtColor(a,cv2.COLOR_BGR2HSV)
    #b = cv2.cvtColor(b,cv2.COLOR_BGR2HSV)
    cv2.imshow('a',a)
    cv2.imshow('b',b)
    cv2.waitKey(0)
    ans = Histogram(a,b)
    print(ans)
