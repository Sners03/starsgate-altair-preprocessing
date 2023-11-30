
# Importing Image from PIL package 
import cv2
import cv2.typing as cv2_type
import itertools as iter
import numpy as np
import os
from time import time


class onboardTest():
    def __init__(self, path) -> None:
        self.im =  self.__load_image(path)
        self.width, self.height, channels = self.im.shape
        self.im_arr = np.array(self.im)
        self.dirname = f"{time()}"
        os.mkdir(self.dirname)


    def __load_image(self, path):
        # Just for visual debugging
        
        im = cv2.imread(path)
        return im
    


    def is_red(self):
        h, s = cv2.split(cv2.cvtColor(self.im, cv2.COLOR_BGR2HSV))[:2]
        print(h)
        print(len(h))

        print(cv2.split(cv2.cvtColor(self.im, cv2.COLOR_BGR2HSV))[:2])
        idx = (((h >= 170) & (h <= 180)) | ((h >= 0) & (h <= 10))) & ((s >= 100) & (s <= 255))

        # Just for visual debugging
        #cv2.imshow('image', self.im)
        cv2.imshow('red_mask', idx.astype(np.uint8) * 255)

        return idx, np.count_nonzero(idx)
    
    
    def mean_color_area(self, color:cv2_type.MatLike, bias:float=0.1):
        #lower boder
        lower_border = int(round(color.mean()*(1.0-bias)))
        #check isn't neccessary? always above 0?
        lower_border = 0 if lower_border<0 else lower_border #check higher than 0
        #upper border
        upper_border = int(round(color.mean()*(1.0+bias)))
        upper_border = 255 if upper_border>255 else upper_border # check lower than 255

        color_area = ((color <= lower_border) | (color >= upper_border))

        return color_area

    def __cutimage(self, x, y):
        imcopy = self.im.copy()
        roi = imcopy[max(0, y-25):min(y+25, self.width), max(0,x-25):min(self.height, x+50)]
        return roi

    def __find_rois(self, contours):
        #init image var
        for iter, contour in enumerate(contours):
            x,y = contour[0][0]
            filename = f"{iter}.png"
            path = os.path.join(self.dirname, filename)
            print(f"Creating file... {path}")
            image = self.__cutimage(x,y)
            cv2.imwrite(path, image)
    
   
    def shipfilter(self):
        loadrgeb = cv2.COLOR_BGR2RGB
        im = self.im
        color = cv2.cvtColor(im, loadrgeb)
        r, g, b = cv2.split(color)
        idx = (self.mean_color_area(r) & self.mean_color_area(g) & self.mean_color_area(b, bias=0.35))
        waterfilter = idx.astype(np.uint8) * 255

        # Just for visual debugging
        cv2.imshow('image', self.im)
        cv2.imshow('water gone', waterfilter)

        contours, hierarchy = cv2.findContours(waterfilter, cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_TC89_KCOS)

        print(len(contours))
        self.__find_rois(contours=contours)
        
        #cv2.rectangle(self.im, (x1, y1), (x2, y2), (255, 0, 0), 2)

        return idx, np.count_nonzero(idx)

    
    def print_arr(self):
        print(self.im_arr.shape)
        #cv2.imshow('image', self.im)
        #input()
        #cv2.imshow('red_mask', idx.astype(np.uint8) * 255)

def mainrun():
    if __name__ == "__main__":
        test = onboardTest(r"src\ship_images\02.png")
        print(test.im.shape)
        test.shipfilter()

        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
   mainrun()