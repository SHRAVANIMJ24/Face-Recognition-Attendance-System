import os
import numpy as np
import cv2
from PIL import Image
import tkinter.messagebox as mess
from utils.file_utils import assure_path_exists

def TrainImages(message1, message):
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces, IDs = getImagesAndLabels("TrainingImage")

    if not faces:
        mess._show(title='No Registrations', message='Please Register someone first!!!')
        return

    recognizer.train(faces, np.array(IDs))
    recognizer.save("TrainingImageLabel/Trainner.yml")
    message1.configure(text="Profile Saved Successfully")
    message.configure(text=f"Total Registrations till now  : {IDs[0]}")

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces, IDs = [], []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        IDs.append(ID)
    return faces, IDs

def check_haarcascadefile():
    if not os.path.isfile("haarcascade_frontalface_default.xml"):
        mess._show(title='Some file missing', message='Please contact us for help')
