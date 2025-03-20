import cv2
import pickle



img= cv2.imread('carParkImg.png')

width, height = 107, 48

try:
    with open('car_park_pos', 'rb') as f:
        pos_List = pickle.load(f)
except:
    pos_List=[]




def mouse_click(events,x,y,flags,params):
    if events==cv2.EVENT_LBUTTONDOWN:
        pos_List.append((x,y))
    if events==cv2.EVENT_RBUTTONDOWN:
        for i,pos in enumerate(pos_List):
            x1,y1=pos
            if x1<x<x1+width and y1<y<y1+height:
                pos_List.pop(i)

    with open('car_park_pos','wb') as f:
        pickle.dump(pos_List,f)

while True:
    img = cv2.imread('carParkImg.png')

    for pos in pos_List:
            cv2.rectangle(img, pos,(pos[0]+width, pos[1]+height), (250, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouse_click)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Check if 'q' is pressed
        break

cv2.destroyAllWindows()
cv2.waitKey(1)