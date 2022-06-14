import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from send_email import send_mail_to_reciever

# from PIL import ImageGrab

path = 'Training_images'
images = []
classNames = []
myList = os.listdir(path)
name_email_dict = {
    'bikram mondal': 'bikrammondal82841@gmail.com',
    'debargha saha': 'debarghasaha01@gmail.com',
    'koustav majhi': 'kaustavmajhi2000@gmail.com',
    'madhurima': 'madhurimabhattacharjee141@gmail.com',
    'manojit roy': 'roy.monojit982810@gmail.com'    
}

'''
print("List of images files provided by the students:")
for x in myList:
    print(x)
print('*'*20)
'''

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

'''
    
print("\nThe list of names of all the students are as follows:")
count = 1
for x in classNames:
    print(f"{count}: {x}")
    count += 1
print('*'*20)

'''

def findEncodings(images):
    encodeList = []


    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    
    with open('Attendance.csv', 'r+') as f:
        # path = ''C:/Users/MANOJIT/OneDrive/Desktop/FRAP/Attendance.csv'
        myDataList = f.readlines()
        
        nameList = []
        flag = False
        for line in myDataList:
            if flag:
                break
            
            entry = line.split(',')
            nameList.append(entry[0])
            
        
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')
                flag = True
        
       
            
    
    return True


#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr

print('{0:^100}'.format('---- WELCOME TO THE AUTOMATED-FACE-RECOGNITION-ATTENDANCE-MARKING SYSTEM ----'))
print('*'*20)
print("Encoding started...")
encodeListKnown = findEncodings(images)
print('Encoding completed!')
print('*'*20)

print("\nIt'll take some time to start the camera. Please stay looking at the camera until the confirmation!\n")
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
# img = captureScreen()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    flag = False
    #count = 0
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
# print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
# print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            '''if not flag:
                print("Marking attendance...")
                flag = markAttendance(name)
                print(f"Hello, {name}")
            
            if flag and count>10000:
                break
            else:
                count += 1
                continue
            '''
            if name == 'Wearing Mask' or name == 'WEARING MASK':
                print("You're wearing a mask! It's necessary to put off the mask while taking the facial attendance.") 
                continue

            print("\nMarking attendance...")
            flag = markAttendance(name)
            
            send_mail_to_reciever('ankuran.biswas@gmail.com', 'ddksezmbntadutnq', name_email_dict[name.lower()], name.title())
            print(f"Hello, {name}")
            if flag:
                break

    

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
    if flag:
        print("Your attendance has been marked!\nPlease check the your registered mail inbox for official confirmation!\n\n\n\n")
        break;
    

