'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1A - Part 1 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:			[ NB_2082 ]
# Author List:		[ Harsh, Aditya]
# Filename:			task_1a_part1.py
# Functions:		scan_image
# 					[ checkapprox, getSlopePerp, getSlopeParallel, getDist, getColor  ]
# Global variables:	shapes
# 					[ ]


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, os)                ##
##############################################################
import cv2
import numpy as np
import os
##############################################################


# Global variable for details of shapes found in image and will be put in this dictionary, returned from scan_image function
shapes = {}


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################






##############################################################

def checkapprox(a,b):
    if abs(a-b)<=2 or -2<=a+b<=2:
        return 0
    else:
        return a-b

def getSlopePerp(x1,y1,x2,y2,x3,y3):
    if checkapprox(x1,x2)==0:
        m1 = 0
    else:
        m1=checkapprox(y1,y2)//checkapprox(x1,x2)

    if checkapprox(x2,x3)==0:
        m2 = 0
    else:
        m2=checkapprox(y1,y2)//checkapprox(x1,x2)

    if (m2==0 & m1==0) or (m1*m2 ==-1):
        return True
    else:
        return False

def getSlopeParallel(x1,y1,x2,y2,x3,y3,x4,y4):
    if checkapprox(x1,x2)==0:
        m1 = 0
    else:
        m1=checkapprox(y1,y2)//checkapprox(x1,x2)

    if checkapprox(x2,x3)==0:
        m2 = 0
    else:
        m2=checkapprox(y1,y2)//checkapprox(x1,x2)

    if m1==m1:
        return True
    else:
        return False

def getDist(x1,y1,x2,y2):
    return (((x2-x1)*2)+((y2-y1)*2))*0.5

def getColor(path,x,y):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if (img[y,x]==np.array([255,0,0])).all() or (img[y,x]==np.array([255,0,19])).all():
        return "blue"
    elif (img[y,x]==np.array([1,128,0])).all() or (img[y,x]==np.array([0,128,0])).all():
        return "green"
    elif (img[y,x]==np.array([0,0,255])).all():
        return "red"
    else:
        return "white"
        print(img[y,x])

def scan_image(img_file_path):

    """
    Purpose:
    ---
    this function takes file path of an image as an argument and returns dictionary
    containing details of colored (non-white) shapes in that image

    Input Arguments:
    ---
    `img_file_path` :		[ str ]
        file path of image

    Returns:
    ---
    `shapes` :              [ dictionary ]
        details of colored (non-white) shapes present in image at img_file_path
        { 'Shape' : ['color', Area, cX, cY] }
    
    Example call:
    ---
    shapes = scan_image(img_file_path)
    """

    global shapes
    shapes={}
    ##############	ADD YOUR CODE HERE	##############
    img = cv2.imread(img_file_path,cv2.IMREAD_GRAYSCALE)
    _, threshold = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pos,cnt in enumerate(contours):
        if pos == 0:
            continue
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        area = cv2.contourArea(cnt)
        cx = int(cv2.moments(cnt)['m10']/cv2.moments(cnt)['m00'])
        cy = int( cv2.moments(cnt)['m01']/cv2.moments(cnt)['m00'])
        color = getColor(img_file_path,cx,cy)
        if len(approx) == 3:
            shapes['Triange']=[color,area,cx,cy]
        elif len(approx) == 4:
            _,_,w,h = cv2.boundingRect(cnt)
            n = approx.ravel()
            x1 , y1 = n[0],n[1]
            x2 , y2 = n[2],n[3]
            x3 , y3 = n[4],n[5]
            x4 , y4 = n[6],n[7]
            # print(n)
            ab = getDist(x1,y1,x2,y2)
            bc = getDist(x2,y2,x3,y3)
            cd = getDist(x3,y3,x4,y4)
            ad = getDist(x4,y4,x1,y1)
            ac = getDist(x3,y3,x1,y1)
            bd = getDist(x4,y4,x2,y2)
            if checkapprox(ab,bc)==0 & getSlopePerp(x1,y1,x2,y2,x3,y3):
                shapes['Square']=[color,area,cx,cy]
            elif checkapprox(ab,bc)==0:
                shapes['Rhombus']=[color,area,cx,cy]
            elif checkapprox(ab,cd)==0 and checkapprox(bc,ad)==0:
                shapes['Parallelogram']=[color,area,cx,cy]
            elif getSlopeParallel(x1,y1,x2,y2,x3,y3,x4,y4) or getSlopeParallel(x2,y2,x3,y3,x4,y4,x1,y1):
                shapes['Trapezium']=[color,area,cx,cy]
            else:
                shapes['Quadrilateral']=[color,area,cx,cy]
        elif len(approx) == 5:
            shapes['Pentagon']=[color,area,cx,cy]
        elif len(approx) == 6:
            shapes['Hexagon']=[color,area,cx,cy]
        else:
            shapes["Circle"]=[color,area,cx,cy]

	##################################################
    shapes = {k: v for k, v in sorted(shapes.items(), key=lambda item: item[1][1],reverse=True)}
    return shapes


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    the function first takes 'Sample1.png' as input and runs scan_image function to find details
#                   of colored (non-white) shapes present in 'Sample1.png', it then asks the user whether
#                   to repeat the same on all images present in 'Samples' folder or not

if __name__ == '__main__':

    curr_dir_path = os.getcwd()
    print('Currently working in '+ curr_dir_path)

    # path directory of images in 'Samples' folder
    img_dir_path = curr_dir_path + '/Samples/'
    
    # path to 'Sample1.png' image file
    file_num = 1
    img_file_path = img_dir_path + 'Sample' + str(file_num) + '.png'

    print('\n============================================')
    print('\nLooking for Sample' + str(file_num) + '.png')

    if os.path.exists('Samples/Sample' + str(file_num) + '.png'):
        print('\nFound Sample' + str(file_num) + '.png')
    
    else:
        print('\n[ERROR] Sample' + str(file_num) + '.png not found. Make sure "Samples" folder has the selected file.')
        exit()
    
    print('\n============================================')

    try:
        print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
        shapes = scan_image(img_file_path)

        if type(shapes) is dict:
            print(shapes)
            print('\nOutput generated. Please verify.')
        
        else:
            print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
            exit()

    except Exception:
        print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
        exit()

    print('\n============================================')

    choice = input('\nWant to run your script on all the images in Samples folder ? ==>> "y" or "n": ')

    if choice == 'y':

        file_count = 2
        
        for file_num in range(file_count):

            # path to image file
            img_file_path = img_dir_path + 'Sample' + str(file_num + 1) + '.png'

            print('\n============================================')
            print('\nLooking for Sample' + str(file_num + 1) + '.png')

            if os.path.exists('Samples/Sample' + str(file_num + 1) + '.png'):
                print('\nFound Sample' + str(file_num + 1) + '.png')
            
            else:
                print('\n[ERROR] Sample' + str(file_num + 1) + '.png not found. Make sure "Samples" folder has the selected file.')
                exit()
            
            print('\n============================================')

            try:
                print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
                shapes = scan_image(img_file_path)

                if type(shapes) is dict:
                    print(shapes)
                    print('\nOutput generated. Please verify.')
                
                else:
                    print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
                    exit()

            except Exception:
                print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
                exit()

            print('\n============================================')

    else:
        print('')
