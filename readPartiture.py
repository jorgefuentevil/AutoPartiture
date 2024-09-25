import cv2 
import numpy as np

def detectNote(img,img_gray,note,color,  thres, lista,tipo):
    w, h = note.shape[::-1] 
    res = cv2.matchTemplate(img_gray, note, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= thres)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), color, 1)
        lista.append([pt[0],pt[1],tipo])


def detectClef(img,img_gray,clef ,color, thres, lista,tipo):
    w, h = clef.shape[::-1] 
    res = cv2.matchTemplate(img_gray, clef, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= thres)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), color, 1)
        lista.append([pt[0],pt[1],tipo])

def deleteRepited(arr):
    eliminar = []
    for i in range(np.size(arr,0)):            
        for n in range(i + 1,np.size(arr,0)):
            a = abs(arr[i][0] - arr[n][0])
            b = abs(arr[i][1] - arr[n][1])
            if((a < 3) and (b < 3)):
                if(arr[i][2]=="b" and arr[n][2]=="c") :
                    eliminar.append(i)
                elif (arr[i][2]=="c" and arr[n][2]=="b") :
                    eliminar.append(n)
                else:
                    eliminar.append(n)
    eliminar = np.unique(eliminar)
    res= np.delete(arr,eliminar,0)
    return res

#Given an image of a partiture it returns all the notes and the clef
def extractNotes(src):
    # Read the  image
    img = cv2.imread(src)
    # Take the templates to compare
    b1 = cv2.imread("templates/b1.png",0) 
    b2 = cv2.imread("templates/b2.png",0)
    b3 = cv2.imread("templates/b3.png",0) 
    b4 = cv2.imread("templates/b4.png",0) 
    w1 = cv2.imread("templates/w1.png",0) 
    w2 = cv2.imread("templates/w2.png",0) 
    r1 = cv2.imread("templates/r1.png",0)
    r2 = cv2.imread("templates/r2.png",0)
    cor = cv2.imread("templates/cor.png",0)

    sol = cv2.imread("templates/sol.png",0)
    fa = cv2.imread("templates/fa.png",0)

    # Convert the image to grey scale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    

    notasRepited = []

    # Get the clafe
    detectClef(img,img_gray,sol,(0,0,255),0.65,notasRepited,"sol")
    detectClef(img,img_gray,fa,(0,0,255),0.65,notasRepited,"fa")


    # Get all the notes
    detectNote(img,img_gray,b1,(0,0,255),0.65,notasRepited,"b")
    detectNote(img,img_gray,b2,(0,0,255),0.65,notasRepited,"b")
    detectNote(img,img_gray,b3,(0,0,255),0.65,notasRepited,"b")
    detectNote(img,img_gray,b4,(0,0,255),0.65,notasRepited,"b")
    detectNote(img,img_gray,w1,(0,0,255),0.65,notasRepited,"w")
    detectNote(img,img_gray,w2,(0,0,255),0.65,notasRepited,"w")
    detectNote(img,img_gray,r1,(0,0,255),0.65,notasRepited,"r")
    detectNote(img,img_gray,r2,(0,0,255),0.65,notasRepited,"r")
    detectNote(img,img_gray,cor,(0,0,255),0.65,notasRepited,"c")



    #Take the repited out and compares 
    notas = deleteRepited(notasRepited)

    return notas
    
notas_encontradas = extractNotes('partituras/maria.JPG')

print("Notas encontradas en la partitura:", notas_encontradas)
