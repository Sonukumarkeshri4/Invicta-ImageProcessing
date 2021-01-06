# Importing necessary libraries
import cv2
import numpy as np

# Reading the image of leaves saved in same folder
frame = cv2.imread('level1.jpg')



while True:
    # Converting to HSV values for better contour visualisation
    hsvFrame = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)
    
    # Removing all coloured parts except green(Masking) in selected range
    mask_green = cv2.inRange(frame, np.array([31, 61, 46]), np.array([89,218,134]))
    content_green = cv2.countNonZero(mask_green)
    #cv2.imshow("mask1",mask_green)
    
    # Removing all coloured parts except yellow(Masking) in selected range
    mask_yellow = cv2.inRange(hsvFrame, np.array([20, 143, 139]), np.array([30, 252, 246]))
    content_yellow = cv2.countNonZero(mask_yellow)
    #cv2.imshow("mask2",mask_yellow)

    # Finding contour to exactly detect only that particular colour by dialation and bitwise_and operator
    kernal = np.ones((5,5),"uint8")
    
    #For Green
    mask_green = cv2.dilate(mask_green, kernal)
    green = cv2.bitwise_and(frame, frame, mask = mask_green)

    #For yellow
    mask_yellow = cv2.dilate(mask_yellow, kernal)
    yellow = cv2.bitwise_and(hsvFrame, hsvFrame, mask = mask_yellow)

    # Creating contour to track the yellow colour
    contours, hierarchy = cv2.findContours(mask_yellow,cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE)

    #Rectangle around the yellow contour
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area> 300):
            x,y,w,h = cv2.boundingRect(contour)
            frame = cv2.rectangle(frame,(x,y), (x+w, y+h), (255,0,0), 1)
            cv2.putText(frame,'Old leaf %d'%(content_yellow), (x-10, y-10),
                        cv2.FONT_HERSHEY_PLAIN ,1, (0,0,255),1)
            
    
    #Creating contour to track everything in Level1.jpg image
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    _,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    dilated = cv2.dilate(thresh,kernel,iterations = 13 )
    contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        [x,y,w,h] = cv2.boundingRect(contour)
        # Condition such that all the image part will not be covered 
        if h>300 and w>300: #for bigger contours
            continue
        # Condition that the small contours are not tracked
        if h<120 and w<120: #for smaller contours
            continue
        cv2.rectangle(frame,(x,y), (x+w, y+h), (255,0,0), 1)
        if content_green > 3591 :
            cv2.putText(frame,'Fresh leaf %d'%(content_green), (x-10, y-10),
                        cv2.FONT_HERSHEY_PLAIN ,1, (0,0,255),1)
        else:
            cv2.putText(frame,'Old leaf', (x-10, y-10),
                        cv2.FONT_HERSHEY_PLAIN ,1, (0,0,255),1)
        cv2.imshow("mask",frame)
        cv2.imwrite("output1.jpg",frame)
        
    

    key = cv2.waitKey(1)
    if key == 27:
        break
cv2.destroyAllWindows()
    

