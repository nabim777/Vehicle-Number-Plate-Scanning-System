import numpy as np
import cv2
import imutils
import pytesseract
import mysql.connector
from tkinter import messagebox
from tkinter import Tk
from tkinter import *
from tkinter.filedialog import askopenfilename
def pic_recog():
    Tk().withdraw()
    filename = askopenfilename()

    image = cv2.imread(filename)
    image = imutils.resize(image, width=500)
    #cv2.imshow("Original Image", image)


    gray_scaled = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_scaled = cv2.bilateralFilter(gray_scaled, 15, 20, 20)
    edges = cv2.Canny(gray_scaled, 170, 200)
    #cv2.imshow("Edged", edges)

    contours, heirarchy = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    img1 = image.copy()
    cv2.drawContours(img1, contours, -1, (0, 255, 0), 3)
    #cv2.imshow("All of the contours", img1)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]
    Number_Plate_Contour = 0

    for current_contour in contours:
        perimeter = cv2.arcLength(current_contour, True)
        approx = cv2.approxPolyDP(current_contour, 0.02 * perimeter, True)
        if len(approx) == 4:
            Number_Plate_Contour = approx
            break

    mask = np.zeros(gray_scaled.shape, np.uint8)
    new_image1 = cv2.drawContours(mask, [Number_Plate_Contour], 0, 255, -1, )
    new_image1 = cv2.bitwise_and(image, image, mask=mask)
    #cv2.imshow("Number Plate", new_image1)


    gray_scaled1 = cv2.cvtColor(new_image1, cv2.COLOR_BGR2GRAY)
    ret, processed_img = cv2.threshold(np.array(gray_scaled1), 125, 255, cv2.THRESH_BINARY)
    #cv2.imshow("Number Plate", processed_img)

    #cv2.waitKey(0)

    #Text Recognition
    custom_config=r'--psm 6'
    #pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    text = pytesseract.image_to_string(processed_img,config=custom_config)#config="-l eng+nep --psm 7")
    text = text[1::]
    text=text.replace("\n" , "") 
    if check_blacklist(text)== True:
        messagebox.showinfo("Error", text + "is black listed")
    else:
        register_data(text)
        messagebox.showinfo("Success", text + "Added Successfully")
    cv2.waitKey(0)
    
    
def video_recog():
    cap = cv2.VideoCapture(0)

    while (True):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # canny egde Detection
        # canny_edge = cv2.Canny(gray,170,200)

        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        # cv2.putText(frame,"Nalem7", (40, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))

        contours, h = cv2.findContours(thresh, 1, 2)
        largest_rectangle = [0, 0]
        for cnt in contours:
            lenght = 0.01 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, lenght, True)
            if len(approx) == 4:
                area = cv2.contourArea(cnt)
                if area > largest_rectangle[0]:
                    largest_rectangle = [cv2.contourArea(cnt), cnt, approx]
        x, y, w, h = cv2.boundingRect(largest_rectangle[1])

        image = frame[y:y + h, x:x + w]
        cv2.drawContours(frame, [largest_rectangle[1]], 0, (0, 255, 0), 8)
        cropped = frame[y:y + h, x:x + w]
        cv2.putText(frame, "lisence plate", (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                    (0, 0, 255))
        cv2.imshow('caimera', frame)
        cv2.drawContours(frame, [largest_rectangle[1]], 0, (255, 255, 255), 18)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        cv2.imshow('LISENCE PLATE NUMBER', thresh)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening
        #pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
        cv2.putText(frame, data, (40, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
        data = data[1::]
        data=data.replace("\n" , "")

        register_data(data)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
def check_blacklist(plate):
    try:
        conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       password="u:nz48UV",
                                       database="vehicle_number"
                                       )
        my_cursor = conn.cursor()
        my_cursor.execute("select * from blacklist where numberplate='" +str(plate) +"'")
        row = my_cursor.fetchone()
        if row is None:
            return False
        else:
            return True
    except Exception as es:
        messagebox.showerror("Error", f"Due to :{str(es)}")
def register_data(num):
    try:
        conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       password="u:nz48UV",
                                       database="vehicle_number"
                                       )
        my_cursor = conn.cursor()
        my_cursor.execute('insert into whitelist (numberplate) values(+"'+str(num)+'")')
        conn.commit()
        conn.close()

    except Exception as es:
        messagebox.showerror("Error", f"Due to :{str(es)}")

def add_blacklist(bnum):
    try:
        conn = mysql.connector.connect(host="localhost",
                                       user="root",
                                       password="u:nz48UV",
                                       database="vehicle_number"
                                       )
        my_cursor = conn.cursor()
        my_cursor.execute('insert into blacklist (numberplate) values(+"'+(bnum)+'")')
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", bnum+ "Added Successfully")
    except Exception as es:
        messagebox.showerror("Error", f"Due to :{str(es)}")

#text = pytesseract.image_to_string(processed_image)
#print("Number is :", text)
#cv2.waitKey(0)
