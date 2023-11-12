
# Importing Image from PIL package 
import cv2
import cv2.typing as cv2_type
import itertools as iter
import numpy as np
import typing

class onboardTest():
    def __init__(self, path) -> None:
        self.im =  self.__load_image(path)
        self.im_arr = np.array(self.im)


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
    
    def mean_color_area(self, color:cv2_type.MatLike):
        #lower boder
        lower_border = int(round(color.mean()*0.65))
        #check isn't neccessary? always above 0?
        lower_border = 0 if lower_border<0 else lower_border #check higher than 0
        #upper border
        upper_border = int(round(color.mean()*1.35))
        upper_border = 255 if upper_border>255 else upper_border # check lower than 255

        color_area = ((color <= lower_border) | (color >= upper_border))

        return color_area


    
    
    def shipfilter(self):
        r, g, b = cv2.split(cv2.cvtColor(self.im, cv2.COLOR_BGR2RGB))[:3]
        print(int(round(r.mean()*0.9)))
        idx = (self.mean_color_area(r) & self.mean_color_area(g) & self.mean_color_area(b))
        waterfilter = idx.astype(np.uint8) * 255

        # Just for visual debugging
        cv2.imshow('image', self.im)
        cv2.imshow('water gone', waterfilter)

        contours, hierarchy = cv2.findContours(waterfilter, cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

        print(len(contours))
        
        #cv2.rectangle(self.im, (x1, y1), (x2, y2), (255, 0, 0), 2)

        return idx, np.count_nonzero(idx)

    
    def print_arr(self):
        print(self.im_arr.shape)
        #cv2.imshow('image', self.im)
        #input()
        #cv2.imshow('red_mask', idx.astype(np.uint8) * 255)

if __name__ == "__main__":
    test = onboardTest(r"ship_images\02.png")
    test.print_arr()
    test.shipfilter()

    cv2.waitKey(0)
    cv2.destroyAllWindows()