import cv2
import numpy as np
import cv2
import glob
import random
from pyzbar.pyzbar import decode
import os




### CREATE A DIRECTORY TO SAVE ALL THE IMAGE AND DATA OF COLLECTED SOURADNICE ##########

# Directory
directory = "Mission_2"
# Parent Directory path
parent_dir = "C:/Users/Phi Nguyen/Desktop/Lưu tạm/"
  
# Path
path = os.path.join(parent_dir, directory)
  
# Create the directory
# 'GeeksForGeeks' in
# '/home / User / Documents'
if not os.path.exists(path):
    os.mkdir(path)

os.chdir(path)

i=1
def dataCoordinate():
    directory="Piture_"+str(i)
    pod_path=os.path.join(path, directory)
    os.chdir(pod_path)
    picture_path=pod_path+"/Picture.jpg"
    cv2.imwrite(picture_path,frame)
    f = open("souradnice.txt","x") 
    f = open("souradnice.txt", "w")
    f.write(" Global Location: %s\n" % vehicle.location.global_frame)
    f.write(" Global Location (relative altitude): %s\n" % vehicle.location.global_relative_frame)
    f.write(" Local Location: %s\n" % vehicle.location.local_frame)
    f.close()

### CONNECT BETWEEN NVIDIA JETSON NANO AND PIXHAWK #####
from dronekit import connect, VehicleMode
vehicle=connect('/dev/ttyACM0',wait_ready=True, baud=57600)
vehicle.wait_ready('autopilot_version')

def nothing(x):
    pass

# # Images path
# images_path = glob.glob(r"C:\Users\Phi Nguyen\Desktop\Lưu tạm\TestColour\*.png")
# random.shuffle(images_path)

cap= cv2.VideoCapture(0)

# cv2.namedWindow("Trackbars")
# cv2.createTrackbar("L-H","Trackbars",72,180,nothing)
# cv2.createTrackbar("L-S","Trackbars",68,255,nothing)
# cv2.createTrackbar("L-V","Trackbars",154,255,nothing)
# cv2.createTrackbar("U-H","Trackbars",180,180,nothing)
# cv2.createTrackbar("U-S","Trackbars",255,255,nothing)
# cv2.createTrackbar("U-V","Trackbars",243,255,nothing)
# _red=[[72,68,154],[]]

while True:
    _,frame= cap.read()
    #for img_path in images_path:
    #frame=cv2.imread("TestColour1.png")
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # l_h=cv2.getTrackbarPos("L-H","Trackbars")
    # l_s=cv2.getTrackbarPos("L-S","Trackbars")
    # l_v=cv2.getTrackbarPos("L-V","Trackbars")
    # u_h=cv2.getTrackbarPos("U-H","Trackbars")
    # u_s=cv2.getTrackbarPos("U-S","Trackbars")
    # u_v=cv2.getTrackbarPos("U-V","Trackbars")

    # Detect the red color
    # lowest_red= np.array([l_h,l_s,l_v])
    # upper_red= np.array([u_h,u_s,u_v])
    # mask=cv2.inRange(hsv,lowest_red,upper_red)



    ###### DETECT THE RED COLOR #############
    lowest_red1= np.array([0, 100, 20])
    upper_red1= np.array([10,255,255])

    lowest_red2= np.array([160, 100, 20])
    upper_red2= np.array([179,255,255])

    lower_mask_red=cv2.inRange(hsv, lowest_red1, upper_red1)
    upper_mask_red=cv2.inRange(hsv, lowest_red2, upper_red2)
    mask_red=lower_mask_red+upper_mask_red
    #Erosion
    kernel= np.ones((5,5),np.uint8)
    mask_red = cv2.erode(mask_red,kernel)

    #Contours detection
    contours,_=cv2.findContours(mask_red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area= cv2.contourArea(cnt)
        # Appromixation method of the contours
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        x=approx.ravel()[0]
        y=approx.ravel()[1]

        # Compare with condition: How  many pixels???

        if area> 200:
           # cv2.drawContours(frame,[approx],0,(0,0,0),10)
            if len(approx)==4:
                cv2.putText(frame,"Rectangle_Red",(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0))
                cv2.drawContours(frame,[approx],0,(0,0,0),5)
                M = cv2.moments(approx)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                # draw the contour and center of the shape on the image
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
                cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                dataCoordinate()



    ######## DETECT THE BLUE COLOR ####################

    lowest_blue1= np.array([100, 150, 0])
    upper_blue1= np.array([140,255,255])

    lowest_blue2= np.array([94, 80, 2])
    upper_blue2= np.array([126,255,255])

    lower_mask_blue=cv2.inRange(hsv, lowest_blue1, upper_blue1)
    upper_mask_blue=cv2.inRange(hsv, lowest_blue2, upper_blue2)
    mask_blue=lower_mask_blue+upper_mask_blue
    #Erosion
    kernel= np.ones((5,5),np.uint8)
    mask_blue = cv2.erode(mask_blue,kernel)

    #Contours detection
    contours,_=cv2.findContours(mask_blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area= cv2.contourArea(cnt)
        # Appromixation method of the contours
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        x=approx.ravel()[0]
        y=approx.ravel()[1]

        # Compare with condition: How  many pixels???

        if area> 200:
           # cv2.drawContours(frame,[approx],0,(0,0,0),10)
            if len(approx)==4:
                cv2.putText(frame,"Rectangle_Blue",(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0))
                cv2.drawContours(frame,[approx],0,(0,0,0),5)
                M = cv2.moments(approx)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                # draw the contour and center of the shape on the image
                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
                cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                dataCoordinate()


    ### DETECT QR CODE ###
    for barcode in decode(frame):
        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first

        # Decode QR Code
        myData=barcode.data.decode('utf-8')
        # Print result (information of QR code) in terminal
        print(myData)

        # Add bounding box (polygon) for each QR code been detected 
        pts=np.array([barcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(frame,[pts],True,(255,0,255),5)
        pts2 = barcode.rect

        # Put Text in frame of Camera
        cv2.putText(frame,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)
        dataCoordinate()


    #### SHOW ALL THE WINDOWS #############
    cv2.imshow("Frame",frame)
    cv2.imshow("Mask Red",mask_red)
    cv2.imshow("Mask Blue",mask_blue)
    key=cv2.waitKey(1)
    if key ==27:
        break

cap.release()

cv2.destroyAllWindows()
