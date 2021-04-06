import cv2 as cv
import numpy as np

font = cv.FONT_HERSHEY_SIMPLEX
PUREBLACK = (0,0,0)
PUREWHITE = (255,255,255)
capture = cv.VideoCapture(0)

if not capture.isOpened():
    print("Unable To Open Webcam.")
    exit()

else:
    ret, frame = capture.read()
    dimensions = frame.shape
    height = dimensions[0]
    width = dimensions[1]
    centre = [width//2, height//2]

def scanFace(frame):
    face = ''
    rectWidth = 50
    halfRectWidth = rectWidth // 2
    gap = 30
    
    rows = [centre[1] - halfRectWidth - gap - rectWidth,
         centre[1] - halfRectWidth,
         centre[1] + halfRectWidth + gap]

    columns = [centre[0] - halfRectWidth - gap - rectWidth,
         centre[0] - halfRectWidth,
         centre[0] + halfRectWidth + gap]

    mask = np.zeros(frame.shape[:2], dtype='uint8')

    for y in rows:
        for x in columns:
            
            #region = frame[y:y+rectWidth, x:x+rectWidth]
            
            square_mask = cv.rectangle(mask, (x+rectWidth,y+rectWidth),(x,y), 255, -1)

            rectColour = PUREBLACK

            cv.rectangle(frame,(x,y),(x+rectWidth,y+rectWidth), rectColour,1)

    res = cv.bitwise_and(frame,frame, mask=square_mask)
    cv.imshow("grid_mask", res)

    res2 = cv.bitwise_and(frame,frame,mask=blue_mask)
    cv.imshow("blue_mask", res2)

    res3 = cv.bitwise_and(res2,res2, mask=square_mask)
    cv.imshow("res3", res3)

    pixelpoints = np.transpose(np.nonzero(res3))
    
    #print("\nNEW OUTPUT")
    #print(pixelpoints)

    if pixelpoints.size != 0:
        print("blue")

    return face

    
while True:
    ret, frame = capture.read()

    frame = cv.flip(frame,1)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    blue_lower = np.array([94,80,2])
    blue_upper = np.array([120,255,255])
    blue_mask = cv.inRange(hsv,blue_lower,blue_upper)

    green_lower = np.array([36,25,25])
    green_upper = np.array([86,255,255])
    green_mask = cv.inRange(hsv,green_lower,green_upper)

    red_lower = np.array([0,50,50])
    red_upper = np.array([5,255,255])
    red_mask = cv.inRange(hsv,red_lower,red_upper)

    white_lower = np.array([0,0,168])
    white_upper = np.array([172,111,255])
    white_mask = cv.inRange(hsv,white_lower,white_upper)

    yellow_lower = np.array([20,100,100])
    yellow_upper = np.array([30,255,255])
    yellow_mask = cv.inRange(hsv,yellow_lower,yellow_upper)

    orange_lower = np.array([5,50,50])
    orange_upper = np.array([15,255,255])
    orange_mask = cv.inRange(hsv,orange_lower,orange_upper)

    cv.imshow("colour_mask",green_mask)

    #face = scanFace(frame)
    
    cv.imshow("Cube Solver", frame)

    key = cv.waitKey(1)

    if key == 27:
        break
    if key == 32:
        print(face[0:3])
        print(face[3:6])
        print(face[6:9])

        
capture.release()
cv.destroyAllWindows()

