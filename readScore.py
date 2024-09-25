import cv2 
import numpy as np


b = cv2.imread("templates/b1.png",0) 
wh1 = cv2.imread("templates/w1.png",0) 
wh2 = cv2.imread("templates/w2.png",0)
r = cv2.imread("templates/r1.png",0)
q = cv2.imread("templates/q.png",0)

sol = cv2.imread("templates/sol.png",0)
fa = cv2.imread("templates/fa.png",0)

'''
    Function that, from an image finds all the matches of an especific note or clef.

    Parameters
    ----------
    img_gray : Source image with gray filter where notesof clefs have to be serched
    note : Image of the type of note or clef being searched for 
    thres : Value used to separate relevant features from the background 
    list : List where notes and clefs are added
    type : The type of note or clef being searched for ( b, w, q, r , sol(clef), fa(clef) )

'''
def detectNote(img_gray, note,  thres, list, type):
    res = cv2.matchTemplate(img_gray, note, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= thres)
    for pt in zip(*loc[::-1]):
        list.append([pt[0],pt[1],type])

'''
    Function that takes a list of notes and clefs and return the same list without the repited ones.
    It also distinguishes between whether a black note or a quaver

    Parameters
    ----------
    arr : list of notes where repited ones are removed

    Returns
    -------
    res : list without repited notes

'''
def deleteRepited(arr):
    eliminar = []
    for i in range(np.size(arr,0)):            
        for n in range(i + 1,np.size(arr,0)):
            if(arr[i][2]=="b" and arr[n][2]=="q") :
                a = abs(arr[i][0] - arr[n][0])
                b = abs(arr[i][1] - arr[n][1] - 23)
                print(a,b)
                if((a < 3) and (b < 3)):
                    eliminar.append(i)
            else:
                a = abs(arr[i][0] - arr[n][0])
                b = abs(arr[i][1] - arr[n][1])
                if((a < 3) and (b < 3)):
                    eliminar.append(n)
    eliminar = np.unique(eliminar)
    res= np.delete(arr,eliminar,0)
    return res

'''
    Function that draws a rectangle aorround every object from a list of notes in the given image.

    Parameters
    ----------
    arr : list of notes.
    img : image where the rectangle is drawn.

'''
def drawNotes(arr, img):
    for note in arr:
        if note[2] == "b":
            w, h = b.shape[::-1]
            cv2.rectangle(img, (int(note[0]),int(note[1])), (int(note[0])+w, int(note[1])+h), (0,0,255), 1)   
        elif note[2] == "wh1":
            w, h = wh1.shape[::-1]
            cv2.rectangle(img, (int(note[0]),int(note[1])), (int(note[0])+w, int(note[1])+h), (0,255,0), 1) 
        elif note[2] == "wh2":
            w, h = wh2.shape[::-1]
            cv2.rectangle(img, (int(note[0]),int(note[1])), (int(note[0])+w, int(note[1])+h), (0,255,0), 1)   
        elif note[2] == "r":
            w, h = r.shape[::-1]
            cv2.rectangle(img, (int(note[0]),int(note[1])), (int(note[0])+w, int(note[1])+h), (255,0,0), 1)   
        elif note[2] == "q":
            w, h = q.shape[::-1]
            cv2.rectangle(img, (int(note[0]),int(note[1])), (int(note[0])+w, int(note[1])+h), (0,0,255), 1)   
          
     
     
#Given an image of a score it returns all the notes and the clef
def extractNotes(src):
    # Read the  image
    img = cv2.imread(src)
    # Take the templates to compare
    

    # Convert the image to grey scale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    

    notasRepited = []

    # Get the clafe
    detectNote(img_gray,sol,0.65,notasRepited,"sol")
    detectNote(img_gray,fa,0.65,notasRepited,"fa")


    # Get all the notes
    detectNote(img_gray,b,0.65,notasRepited,"b")
    #detectNote(img,img_gray,b2,0.65,notasRepited,"b2")
    #detectNote(img,img_gray,b3,0.65,notasRepited,"b3")
    #detectNote(img,img_gray,b4,0.65,notasRepited,"b4")
    detectNote(img_gray,wh1,0.65,notasRepited,"wh1")
    detectNote(img_gray,wh2,0.65,notasRepited,"wh2")
    detectNote(img_gray,r,0.65,notasRepited,"r")
    #detectNote(img,img_gray,r2,0.65,notasRepited,"r2")
    detectNote(img_gray,q,0.65,notasRepited,"q")



    #Take the repited out 
    notas = deleteRepited(notasRepited)

    #Draw the notes in the image and save it
    drawNotes(notas,img)
    cv2.imwrite("resultado.jpg",img)

    return notas
    
notas_encontradas = extractNotes('partituras/una-ves-hubo-un-juez.JPG')
print(np.size(notas_encontradas,0))


print("Notas encontradas en la partitura:\n", notas_encontradas)
