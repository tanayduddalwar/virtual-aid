import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from cvzone import cornerRect
cap = cv.VideoCapture(0)
from pynput.keyboard import Controller
detector = HandDetector(detectionCon=0.1)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["Del"]]
class Button():
    def __init__(self, pos=[], text="", size=[70, 70]):
        self.pos = pos
        self.size = size
        self.text = text

    def draw(self, img):
        x, y = self.pos
        w, h = self.size
        #cornerRect(img, (x, y, w, h), 20, 1, (255,0 , 10), 1)
        cv.rectangle(img, (x + 2, y + 2), (x + w - 2, y + h - 2), (255, 255, 0), cv.FILLED) 
        cv.putText(img, self.text, (x + 20, y + 55), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)  
        return img
finaltext=" "
keyboard=Controller()
buttonlist = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        button = Button([70*j+10+j-20, 100* i+ 20], key)
        buttonlist.append(button)

def drawall(img, buttonlist):
    for button in buttonlist:
        button.draw(img)
    return img

while True:
    success, img = cap.read()

    if not success:
        print("Failed to capture frame from the camera.")
        break

    # Detect hands in the frame
    hands, img = detector.findHands(img)
    img = drawall(img, buttonlist)
    cv.rectangle(img,(50,380),(700,450),(175,8,175),cv.FILLED)
    cv.putText(img,finaltext,(68,425),cv.FONT_HERSHEY_PLAIN,4,(255,255,255),4) 
    if hands:
        hand1 = hands[0]
        lmList1 = hand1["lmList"]

        img = drawall(img, buttonlist)

        if lmList1:
            for button in buttonlist:
                x, y = button.pos
                w, h = button.size
                if x < lmList1[8][0] < x + w and y < lmList1[8][1] < y + h:
                            cv.rectangle(img, (x + 2, y + 2), (x + w - 2, y + h - 2), (175,8,175), cv.FILLED) 
                            cv.putText(img, button.text, (x + 20, y + 55), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                            # Extract the coordinates for the two points
                            p1 = lmList1[8][:2]
                            p2 = lmList1[12][:2]
                            # Pass the coordinates to findDistance method
                            l,_,_ = detector.findDistance(p1, p2, img)
                            print(l)
                            if l<30:
                                keyboard.press(button.text)
                                if button.text == "Delete":
                                    finaltext = finaltext[:-1]
                                else:
                                    keyboard.press(button.text)
                                    finaltext += button.text;   
                                    cv.rectangle(img, (x + 2, y + 2), (x + w - 2, y + h - 2), (175,8,175), cv.FILLED) 
                                    cv.putText(img, button.text, (x + 20, y + 55), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                                    finaltext=finaltext+button.text
                                sleep(0.2)




    # Display the frame in full screen
    cv.namedWindow("Image", cv.WINDOW_NORMAL)
    cv.setWindowProperty("Image", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    cv.imshow("Image", img)
    
    # Check for the 'q' key to exit the loop
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close OpenCV windows
cap.release()
cv.destroyAllWindows()