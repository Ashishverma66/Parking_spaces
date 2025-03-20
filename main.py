import cv2
import pickle
import cvzone
import numpy as np

#Video feed
cap=cv2.VideoCapture('carPark.mp4')

with open('car_park_pos', 'rb') as f:
    pos_List = pickle.load(f)

width, height = 107, 48

def check_parking_space(img_pro):
    space_counter=0
    for pos in pos_List:
        x,y=pos

        img_crop=img_pro[y:y+height, x:x+width]
        # cv2.imshow(str(x*y), img_crop)
        count=cv2.countNonZero(img_crop)


        if count<900:
            color=(0,255,0)
            thickness=5
            space_counter+=1

        else:
            color = (0,0, 255)
            thickness = 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 5), scale=1, thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'Parking Space: {space_counter}/{len(pos_List)}', (100, 50), scale=3, thickness=5, offset=20, colorR=(0,200,0))


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img=cap.read()
    img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_blur=cv2.GaussianBlur(img_gray,(3,3),1)
    img_threshold=cv2.adaptiveThreshold(img_blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)

    img_median=cv2.medianBlur(img_threshold,5)
    kernel=np.ones((3,3),np.uint8)
    img_dilate=cv2.dilate(img_median,kernel,iterations=1)
    check_parking_space(img_dilate)


    cv2.imshow("Image", img)
    # cv2.imshow("Image_blur",img_blur)
    # cv2.imshow("ImageBlur",img_median)
    if cv2.waitKey(10) & 0xFF == ord('q'):  # Check if 'q' is pressed
        break

cv2.destroyAllWindows()
cv2.waitKey(1)