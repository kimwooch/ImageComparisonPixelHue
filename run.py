import cv2
import numpy as np
from PIL import Image
import math

def get_Pixel(path):
    #modifies image to have 350 by 450 pixels and returns the pixel values in an image in a list given the path of the image.
    new_width = 350
    new_height = 450
    new_dim = (new_width, new_height)
    #read and resize image for comparison given the dimension
    img = Image.open(path)
    resizedImg = img.resize(new_dim, Image.ANTIALIAS)
    pix = np.array(resizedImg).astype(float)
    #prints array of pixels in the image
    pix = pix.flatten()
    return pix

def get_Hist(path):
    #modifies image to have 350 by 450 pixels, converts it to a gray-scaled image, and returns the frequency of pixels in range 0-255.
    new_width = 350
    new_height = 450
    new_dim = (new_width, new_height)
    #read and resize image for comparison given the dimension
    gray_img = cv2.imread(path, 0)
    resizedImg = cv2.resize(gray_img, new_dim, interpolation = cv2.INTER_AREA)
    #calculates frequency of pixels in range 0-255
    hist = cv2.calcHist([resizedImg], [0], None, [256], [0,256])
    return hist

def is_Similar(image1, image2, imgType):
    #calculates euclidean distance between two images given two image variables and returns a boolean value by comparing calculated euclidean distance between the two images and the averaged calculated euclidean probability of all images.
    e_distance = math.sqrt(np.sum((image1-image2)**2))
    s = 1/(1+e_distance)
    #s value is the average of euclidean distance of the four lists below.
    if imgType == 'histo' and s > 0.00012221124002933538:
        return True
    elif imgType == 'pixel' and s > 0.00003087982893648478:
        return True
    else:
        return False

def percentageEuclidean(image1, image2, imgType):
    if imgType == 'histo':
        img1 = get_Hist(image1)
        img2 = get_Hist(image2)
        #calculates euclidean distance between two images given two image variables and the percentage of accuracy given euclidean value.
        e_distance = math.sqrt(np.sum((img1-img2)**2))
        s = 1/(1+e_distance)
        return s
    elif imgType == 'pixel':
        img1 = get_Pixel(image1)
        img2 = get_Pixel(image2)
        #calculates euclidean distance between two images given two image variables and the percentage of accuracy given euclidean value.
        e_distance = math.sqrt(np.sum((img1-img2)**2))
        s = 1/(1+e_distance)
        return s
    else:
        return

def P_Similarity(image1, image2):
    #returns a boolean value given two image variables by comparing calculated euclidean distance between the two image pixels and the averaged calculated euclidean probability of all image pixels.
    img1 = get_Pixel(image1)
    img2 = get_Pixel(image2)
    return is_Similar(img1, img2, 'pixel')
   
def H_Similarity(image1, image2):
    #returns a boolean value given two image variables by comparing calculated euclidean distance between the two image histograms and the averaged calculated euclidean probability of all image histograms.
    img1 = get_Hist(image1)
    img2 = get_Hist(image2)
    return is_Similar(img1, img2, 'histo')

def highestMatch(lstComplete, imgType):
    #returns the highest similarity percentage in the given list of image files.
    euclideanLst = []
    count = 0
    max = percentageEuclidean(lstComplete[0], lstComplete[2], imgType)
    #compares all the jpg images given a list and appends the percentage of accuracy to euclideanLst.
    for x in range(len(lstComplete)):
        for y in range(len(lstComplete)):
            euclideanLst.append(percentageEuclidean(lstComplete[x], lstComplete[y], imgType))
    #finds the maximum value in euclideanLst
    for x in euclideanLst:
        if x > max and x != 1.0:
            max = x
    return max

def avgEuclidean(lstComplete, imgType):
    #returns average euclidean percentage in a given list of image file.
    euclideanLst = []
    count = 0
    #compares all the jpg images given a list and appends the percentage of accuracy to euclideanLst.
    for x in range(len(lstComplete)):
        for y in range(len(lstComplete)):
            if percentageEuclidean(lstComplete[x], lstComplete[y], imgType) != 1.0:
                percentage = percentageEuclidean(lstComplete[x], lstComplete[y], imgType)
                euclideanLst.append(percentage)
                count = count+1
    #calculates average value of euclidean percentages.
    avg = sum(euclideanLst)/count
    return avg

def accuracyPercentageTest(lstPrediction):
    #calculates the percentage of accuracy given a list of same people.
    pcount = 0
    hcount= 0
    h_probability = 0.0
    p_probability = 0.0
    for i in range(len(lstPrediction)):
        for j in range(len(lstPrediction)):
            if H_Similarity(lstPrediction[i],lstPrediction[j]) and percentageEuclidean(lstPrediction[i], lstPrediction[j], 'histo') != 1.0:
                pcount += 1
    for i in range(len(lstPrediction)):
        for j in range(len(lstPrediction)):
            #makes sure that euclidean distance of two images is over the threshold and two images are not equal
            if P_Similarity(lstPrediction[i],lstPrediction[j]) and percentageEuclidean(lstPrediction[i], lstPrediction[j], 'pixel') != 1.0:
                hcount += 1
    #given the list below each list has 1 same person and since the algorithm compares 9 times, I subtracted 9 out of total number.
    p_probability = pcount / ((len(lstPrediction)**2)-9)
    h_probability = hcount/ ((len(lstPrediction)**2)-9)
    return p_probability, h_probability


def accuracyTest(lstComplete, lst1):
    #calculates the percentage of accuracy give two lists with the same people.
    pcount = 0
    hcount = 0
    for x in range(len(lst1)):
        for y in range(len(lstComplete)):
            if P_Similarity(lst1[x], lstComplete[y]):
                pcount = pcount+1
    for x in range(len(lst1)):
        for y in range(len(lstComplete)):
            if H_Similarity(lst1[x], lstComplete[y]):
                hcount = hcount+1
    p_probability = pcount / (len(lstComplete)*len(lst1))
    h_probability = hcount / (len(lstComplete)*len(lst1))
    return p_probability, h_probability

if __name__ == '__main__':
    #list of jpg files for person1
    lst1 = ["0_64.jpg", "0_122.jpg", "0_156.jpg", "0_174.jpg", "0_192.jpg","0_210.jpg", "0_228.jpg", "0_246.jpg", "0_264.jpg"]
    #list of jpg files for person2
    lst2 = ["1_45.jpg", "1_67.jpg", "1_75.jpg", "1_82.jpg", "1_93.jpg","1_102.jpg", "1_103.jpg", "1_104.jpg", "1_105.jpg"]
    #list of jpg files for person3
    lst3 = ["1_173.jpg", "1_208.jpg", "1_226.jpg", "1_244.jpg", "1_262.jpg","1_280.jpg", "1_298.jpg", "1_316.jpg", "1_353.jpg"]
    #list of jpg files for person4
    lst4 = ["4_188.jpg", "4_199.jpg", "4_209.jpg", "4_218.jpg", "4_223.jpg", "4_233.jpg", "4_276.jpg", "4_281.jpg","4_286.jpg"]
    #list of jpg files for person1,2,3,4
    lstcmp = ["0_64.jpg", "0_122.jpg", "0_156.jpg", "0_174.jpg", "0_192.jpg","0_210.jpg", "0_228.jpg", "0_246.jpg", "0_264.jpg","1_45.jpg", "1_67.jpg", "1_75.jpg", "1_82.jpg", "1_93.jpg","1_102.jpg", "1_103.jpg", "1_104.jpg", "1_105.jpg","1_173.jpg", "1_208.jpg", "1_226.jpg", "1_244.jpg", "1_262.jpg","1_280.jpg", "1_298.jpg", "1_316.jpg", "1_353.jpg", "4_188.jpg", "4_199.jpg", "4_209.jpg", "4_218.jpg", "4_223.jpg", "4_233.jpg", "4_276.jpg", "4_281.jpg","4_286.jpg"]

    #used these two averages for s value above.
    print((avgEuclidean(lst1, 'histo') + avgEuclidean(lst2, 'histo') + avgEuclidean(lst3, 'histo') + avgEuclidean(lst4, 'histo'))/4)
    print((avgEuclidean(lst1, 'pixel') + avgEuclidean(lst2, 'pixel') + avgEuclidean(lst3, 'pixel') + avgEuclidean(lst4, 'pixel'))/4)
    
    #calculated the accuracy of both pixel and histogram values by averaging four averages of euclidean percentage values of each lists above.
    lstpixel = []
    lsthisto = []
    p_probability, h_probability = accuracyPercentageTest(lst1)
    lstpixel.append(p_probability)
    lsthisto.append(h_probability)
    p_probability, h_probability = accuracyPercentageTest(lst2)
    lstpixel.append(p_probability)
    lsthisto.append(h_probability)
    p_probability, h_probability = accuracyPercentageTest(lst3)
    lstpixel.append(p_probability)
    lsthisto.append(h_probability)
    p_probability, h_probability = accuracyPercentageTest(lst4)
    lstpixel.append(p_probability)
    lsthisto.append(h_probability)

    averagedPixelProb = sum(lstpixel)/4
    averagedHistoProb = sum(lsthisto)/4

    print('Accuracy of pixel: %f, Accuracy of histogram: %f' % (averagedPixelProb, averagedHistoProb))

#given the images above, the accuracy of pixel was 31.2% and the accuracy of histogram was 17.4%
#the low result of accuracy is due to different dimension of jpg files yolo captures and different colored images from the change of environment.

