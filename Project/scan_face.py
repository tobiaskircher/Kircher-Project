#SCAN FACE

#Import required libraries
import cv2 as cv
import numpy as np

#Function which uses camera to return colours on the fac
def run(facing_screen, facing_up):
    #Set up font
    font = cv.FONT_HERSHEY_SIMPLEX
    
    #Define colours
    PUREBLACK = (0,0,0)
    PUREWHITE = (255,255,255)

    #Prepare for video capture
    capture = cv.VideoCapture(0)

    #Return error if unable to open camera
    if not capture.isOpened():
        return "nocamera"

    else:
        #Set up dimensions and centre for camera view
        ret, frame = capture.read()
        dimensions = frame.shape
        height = dimensions[0]
        width = dimensions[1]
        centre = [width//2, height//2]

    #Function to search the grid for colours
    def scanFace(frame):
        #Set up empty string for face
        face = ''

        #Iterate through squares on the grid
        for y in rows:
            for x in columns:

                #Make variable to store colour within the square
                square_colour = ''

                #Create a mask for that specfic square
                mask = np.zeros(frame.shape[:2], dtype='uint8')
                square_mask = cv.rectangle(mask, (x+rectWidth,y+rectWidth),(x,y), 255, -1)

                #Set up variables 
                count = 0
                detected_value = []
                detected_name = []

                #Find colour with most appearances within the square
                for colour_mask in colour_masks:
                    res_colour = cv.bitwise_and(frame,frame,mask=colour_mask)
                    res = cv.bitwise_and(res_colour,res_colour,mask=square_mask)
                    pixel_points = np.transpose(np.nonzero(res))

                    #Add colour to list (with number of pixels it occurs in), if present
                    if pixel_points.size != 0:
                        detected_value.append(int(np.linalg.norm(pixel_points)))
                        detected_name.append(colours[count])
                        
                    #Increment counter
                    count+=1

                #Assign colour of square to colour with most pixels
                if len(detected_value) != 0:
                    square_colour = detected_name[detected_value.index(max(detected_value))]

                #If no colours were found, assign an symbol representing an unrecognisable colour
                if square_colour == '':
                    square_colour = '?'

                    
                #Add colour of square to colour of face
                face += square_colour

        #Return colours detected
        return face

    #Set flag
    done = False

    #Draw live camera feed each frame
    while not done:
        #OpenCV
        ret, frame = capture.read()
        #Flip camera
        frame = cv.flip(frame,1)

        #Initialse variable for grid
        rectWidth = 50
        halfRectWidth = rectWidth // 2
        gap = 30

        #Position for grid rows
        rows = [centre[1] - halfRectWidth - gap - rectWidth,
             centre[1] - halfRectWidth,
             centre[1] + halfRectWidth + gap]

        #Position for grid coloumns
        columns = [centre[0] - halfRectWidth - gap - rectWidth,
             centre[0] - halfRectWidth,
             centre[0] + halfRectWidth + gap]

        #Draw grid
        for y in rows:
            for x in columns:    
                rectColour = PUREBLACK
                cv.rectangle(frame,(x,y),(x+rectWidth,y+rectWidth), rectColour,1)

        #Display text with what face the user should scan
        text_to_display = "Please scan the " +facing_screen+ " face with the " +facing_up+ " face facing up."
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(frame, text_to_display,(10,50),font,0.65,PUREWHITE,2,cv.LINE_4)

        
        #Display text with instructions
        cv.putText(frame,"Align the cube with the grid shown on the screen.",(10,400),font,0.65,PUREWHITE,2,cv.LINE_4)
        cv.putText(frame, "Press SPACE once aligned, to scan the colours.",(10,450),font,0.65,PUREWHITE,2,cv.LINE_4)

        #Set up HSV colourspace
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        #Create blue boundaries & mask
        blue_lower = np.array([90,80,0])
        blue_upper = np.array([140,255,255])
        blue_mask = cv.inRange(hsv,blue_lower,blue_upper)
        
        #Create green boundaries & mask
        green_lower = np.array([36,25,25])
        green_upper = np.array([86,255,255])
        green_mask = cv.inRange(hsv,green_lower,green_upper)

        #Create red boundaries & mask
        red_lower = np.array([0,50,50])
        red_upper = np.array([5,255,255])
        red_mask = cv.inRange(hsv,red_lower,red_upper)

        #Create white boundaries & mask
        white_lower = np.array([0,0,168])
        white_upper = np.array([172,111,255])
        white_mask = cv.inRange(hsv,white_lower,white_upper)

        ##Create yellow boundaries & mask
        yellow_lower = np.array([20,100,100])
        yellow_upper = np.array([30,255,255])
        yellow_mask = cv.inRange(hsv,yellow_lower,yellow_upper)

        #Create orange boundaries & mask
        orange_lower = np.array([5,50,50])
        orange_upper = np.array([15,255,255])
        orange_mask = cv.inRange(hsv,orange_lower,orange_upper)

        #Create list with all masks
        colour_masks = [blue_mask, green_mask, red_mask, white_mask, yellow_mask, orange_mask]

        #Assign each mask to a letter
        colours = ["b","g","r","w","y","o"]

        #Draw frame onto screen
        cv.imshow("Cube Solver", frame)

        #Get key pressed
        key = cv.waitKey(1)

        #If spacebar is pressed, attempt to detect colours in the grid
        if key == 32:
            face = scanFace(frame)
            face = (''.join(reversed(face[0:3])))+(''.join(reversed(face[3:6])))+(''.join(reversed(face[6:9])))
            #Set flag to true
            done = True

    #End video capture and close windows
    capture.release()
    cv.destroyAllWindows()

    #Return detected colours
    return face
