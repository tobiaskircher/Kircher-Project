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
            
            region = frame[y:y+rectWidth, x:x+rectWidth]
            
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

    blue_lower = np.array([90,80,2])
    blue_upper = np.array([120,255,255])
    blue_mask = cv.inRange(hsv,blue_lower,blue_upper)

    face = scanFace(frame)
    
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

