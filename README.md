# Project-1

###### faceTrain.py


```ruby
import os
import cv2
import numpy as np
from PIL import Image

import pickle

recognizer = cv2.face.LBPHFaceRecognizer_create();
path = 'dataSet'

def getImagesWithID(path):
    imagepaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces=[]
    IDs = []
    for imagepath in imagepaths:
        faceImg = Image.open(imagepath).convert('L');  # convert to single channel( gray scale)
        faceNp = np.array(faceImg, 'uint8')
        ID = int(os.path.split(imagepath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
        cv2.imshow("training",faceNp)
        cv2.waitKey(10)
    return np.array(IDs),faces

IDs,faces = getImagesWithID(path)   # trả về 2 mảng id và face tương ứng

recognizer.train(faces,IDs)

recognizer.save('recognizer/trainningData.yml')
cv2.destroyAllWindows()
```

###### main.py

 selenium is a tool open source, help excute task on a web page automatically

 scaleFactor – Parameter specifying how much the image size is reduced at each image scale.
 resize a larger face to a smaller one, making it detectable by the algorithm.
 1.3 that mean reduce the size 30% 

 minNeighbors – Parameter specifying how many neighbors each candidate rectangle should have to retain it.
Haar cascade classifier works with a sliding window approach. 
size parameter which usually a pretty small value like 20 20.
slide the windowm with wvery iteration haar's cascaded classficier true output are stored , it actualy detects many many false positives
if give minNeighbor = 0, have many false positves
if give minNeibor = 1, we have few false positives

Best minNeighbor is 3 !




'''ruby




import speech_recognition as sr  # process speech
import cv2   # process image
import pyodbc  # to connect database
import playsound  # to play saved mp3 file
from gtts import gTTS  # google text to speech
import os  # to save/open files
import wolframalpha  # to calculate strings into formula
from selenium import webdriver  # to control browser operations




num  = 1 # global variable index save file
def assistant_speaks(output):
    global num

    # num to rename every audio file
    # with different name to remove ambiguity
    num += 1
    print("PerSon : ", output)

    toSpeak = gTTS(text=output, lang='en', slow=False)
    # saving the audio file given by google text to speech
    file = str(num) + ".mp3 "
    toSpeak.save(file)

    # playsound package is used to play the same file.
    playsound.playsound(file, True)
    os.remove(file)



'''
    listen speech and transform to text
'''
def get_audio():
    r = sr.Recognizer()
    audio = ''

    with sr.Microphone() as source:
        print("Speak...")

        # listen for the first phrase and extract it into audio data
        audio = r.listen(source, phrase_time_limit=10) 
    print("Stop.")  # limit 10 secs

    try:
        # recognize speech using Google Speech Recognition
        text = r.recognize_google(audio, language='en-US')
        print("You : ", text)
        return text

    except:

        assistant_speaks("Could not understand your audio, PLease try again !")
        return 0


'''
  Process text with some task: caculate, seach, open application

'''
def process_text(input):
    try:
        if 'search' in input or 'play' in input:
            # a basic web crawler using selenium
            search_web(input)
            return

        elif "who are you" in input:
            speak = '''Hello, I am Person. Your personal Assistant. 
            I am here to make your life easier. You can command me to perform 
            various tasks such as calculating sums or opening applications '''
            assistant_speaks(speak)
            return


        elif 'open' in input:

            # another function to open
            # different application availaible
            open_application(input.lower())
            return

        else:

            assistant_speaks("I can search the web for you, Do you want to continue?")
            ans = get_audio()
            if 'yes' in str(ans) or 'yeah' in str(ans):
                search_web(input)
            else:
                return
    except:

        assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?")
        ans = get_audio()
        if 'yes' in str(ans) or 'yeah' in str(ans):
            search_web(input)

'''
    search some query on google, youtube, wikipedia...
'''

def search_web(input):
    driver = webdriver.Chrome(executable_path=r"D:\SUBJECT\Project 1\Opencv\chromedriver.exe");

    driver.implicitly_wait(1) # wait in maximum 1s for element's presence. 
    driver.maximize_window()

    if 'youtube' in input.lower():

        assistant_speaks("Opening in youtube")
        indx = input.lower().split().index('youtube')
        query = input.split()[indx + 1:]
        driver.get("https://www.youtube.com/results?search_query =" + '+'.join(query))
        return

    elif 'wikipedia' in input.lower():

        assistant_speaks("Opening Wikipedia")
        indx = input.lower().split().index('wikipedia')
        query = input.split()[indx + 1:]
        driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query))
        return

    else:

        if 'google' in input:

            indx = input.lower().split().index('google')
            query = input.split()[indx + 1:]
            driver.get("https://www.google.com/search?q =" + '+'.join(query))

        elif 'search' in input:

            indx = input.lower().split().index('google')
            query = input.split()[indx + 1:]
            driver.get("https://www.google.com/search?q =" + '+'.join(query))

        else:

            driver.get("https://www.google.com/search?q =" + '+'.join(input.split()))

        return


# function used to open application
# present inside the system.
def open_application(input):
    if "chrome" in input:
        assistant_speaks("Google Chrome")
        os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
        return

    elif "word" in input:
        assistant_speaks("Opening Microsoft Word")
        os.startfile(r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE')
        return

    elif "excel" or "Excel" in input:
        assistant_speaks("Opening Microsoft Excel")
        os.startfile('C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE')
        return

    else:

        assistant_speaks("Application not available")
        return




#connect database
def getProfile(id):
    conn =  pyodbc.connect('Driver={SQL Server};'
                      'Server=DELL-PC\SQLEXPRESS;'
                      'Database=User;'
                      'Trusted_Connection=yes;')


    cmd = "SELECT * FROM UserData WHERE PersonID ="+str(id)
    cursor = conn.execute(cmd)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile


'''
    read the saved model
'''
rec =  cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer/trainningData.yml")

'''
    because have 2 threads in my program
    1 thread for video(A), 1 thread for listen speech(B)
    because program have a task need 2 threads, so we need a call back to move from thread B to thread A
'''
#call back function
def callback(recognizer, audio):
    try:
        outp = get_audio()
      
        global val
        if (outp == "who am i" or outp == "who am I"):
            val = 9

        if (outp == 'good' or outp == 'excellent'):
            print('thank you')
    except sr.UnknownValueError:
        print('could not unsertand audio')
    except sr.RequestError as e:
        print('could not request from Google Speech Recognition service; {0}".format(e)')



'''
    creat an object to listen speech from microphone 
    and other object to recoginizer speech
'''
r = sr.Recognizer()
m = sr.Microphone()


cap = cv2.VideoCapture(0)
val = 0


font = cv2.FONT_HERSHEY_SIMPLEX

#  use to detect objects in a video stream
# return a CascadeClassifier object
face_cascade = cv2.CascadeClassifier('D:\\PROGRAM LANGUAGE\\python\\speechrecoginzer\\haarcascade_frontalface_default.xml')


'''
    when we listen, the energy threshold is already set to a good value,
    and we can reliably catch speech right away
'''
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
stop_listening = r.listen_in_background(m, callback)



#main thread
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    if (val == 9):
        faces = face_cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=5)  # detect face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_color = img[y:y + h, x:x + w]
            id, conf = rec.predict(gray[y:y + h, x:x + w]) # recoginizer face
            profile = getProfile(id)
            if (profile != None):
                cv2.putText(img, "Name : " + str(profile[1]), (x, y + h + 20), font, 1, (0, 0, 255))
                cv2.putText(img, "Gender : " + str(profile[2]), (x, y + h + 45), font, 1, (0, 255, 0))
                cv2.putText(img, "Age : " + str(profile[3]), (x, y + h + 70), font, 1, (255, 255, 0))
            else:
                cv2.putText(img, "Unknow", (x, y + h + 20), font, 1, (0, 0, 255))



    if (cv2.waitKey(10) & 0xFF == ord('b')):
        break
    cv2.imshow('Video', img)


#close connect
cap.release()
cv2.destroyAllWindows()
```

``` 
Chi tiết code

```
```ruby
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
```
CascadeClassifier la 1 phuong thuc hoac mo hinh de huan luyen, cu the o day la huan luyen de nhan biet khuon  mat. Mo hinh train nay duoc doc boi  phuong thuc  cv::CascadeClassifier::load . Mo hinh train duoc tai va cai dat trong may tinh voi 2 file xm va cf. Ket qua tra ve la 1 doi tuong lop CascadeClassifier. Sau do detection duoc hoan thanh boi phuong thuc 
cv::CascadeClassifier::detectMultiScale , no se tra ve 1 hinh chu nhat bao quanh khuon mat.


```ruby
recognizer = cv2.face.LBPHFaceRecognizer_create()
```
Tao ra 1 doi thuoc lop  cv2.face.LBPHFaceRecognizer.


```ruby
faces = face_cascade.detectMultiScale(image_array, scaleFactor = 1.3, minNeighbors = 5)
```
ket qua tra ve la 1 object dai dien cho 1 mang da chieu kieu 'numpy.ndarray. Chinh xac hon nua  thi no tra ve 1 list cac hinh chu nhat ma no  chua cac khuon mat anh da duoc detected khong trung nhau. 1 hinh chua nhat duoc dai dien bang 1 list chua 4 diem la (x, y, w, h) . Thi thoang no se tra ve 1 tuple rong khi khong co gi khop, tuc la khong co chua mat trong do .
scaleFactor – Parameter specifying how much the image size is reduced at each image scale.
 resize a larger face to a smaller one, making it detectable by the algorithm.
 1.3 that mean reduce the size 30% 

 minNeighbors – Parameter specifying how many neighbors each candidate rectangle should have to retain it.
Haar cascade classifier works with a sliding window approach. 
size parameter which usually a pretty small value like 20 20.
slide the windowm with wvery iteration haar's cascaded classficier true output are stored , it actualy detects many many false positives
if give minNeighbor = 0, have many false positves
if give minNeibor = 1, we have few false positives

Best minNeighbor is 3 !

```ruby
    ret, img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
```
ret là 1 biến boolean nếu như img là khả dụng
frame là 1 mảng các vector hình ảnh bắt được

