import cv2
import numpy as np
import glob
import random

def nothing(x):
    pass

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L-H","Trackbars",72,180,nothing)
cv2.createTrackbar("L-S","Trackbars",68,255,nothing)
cv2.createTrackbar("L-V","Trackbars",154,255,nothing)
cv2.createTrackbar("U-H","Trackbars",180,180,nothing)
cv2.createTrackbar("U-S","Trackbars",255,255,nothing)
cv2.createTrackbar("U-V","Trackbars",243,255,nothing)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def show_camera():
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    # print(gstreamer_pipeline(flip_method=0))
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        #window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        # # Window
        while cv2.getWindowProperty("CSI Camera", 0) >= 0:
            _,frame=cap.read()
            hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

            l_h=cv2.getTrackbarPos("L-H","Trackbars")
            l_s=cv2.getTrackbarPos("L-S","Trackbars")
            l_v=cv2.getTrackbarPos("L-V","Trackbars")
            u_h=cv2.getTrackbarPos("U-H","Trackbars")
            u_s=cv2.getTrackbarPos("U-S","Trackbars")
            u_v=cv2.getTrackbarPos("U-V","Trackbars")

            lowest_red= np.array([l_h,l_s,l_v])
            upper_red= np.array([u_h,u_s,u_v])

            mask=cv2.inRange(hsv,lowest_red,upper_red)

            #Erosion
            kernel= np.ones((5,5),np.uint8)
            mask = cv2.erode(mask,kernel)

            # Appromixation method of the contours

            #Contours detection
            contours,_=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area= cv2.contourArea(cnt)
                approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
                x=approx.ravel()[0]
                y=approx.ravel()[1]
                if area> 200:
                # cv2.drawContours(frame,[approx],0,(0,0,0),10)
                    if len(approx)==4:
                        cv2.putText(frame,"Rectangle",(x,y),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0))
                        cv2.drawContours(frame,[approx],0,(0,0,0),5)
                        M = cv2.moments(approx)
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        # draw the contour and center of the shape on the image
                        cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
                        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)

            cv2.imshow("Frame",frame)
            cv2.imshow("Mask",mask)
            key=cv2.waitKey(1)
            if key ==27:
                break

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    show_camera()
