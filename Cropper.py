from PIL import Image
from os import path
import os
import tkinter
from tkinter import filedialog

stringGetPath = 'Please select your image'

stringJudgeSquareFail = 'The image is not square and will be cropped.\n\
Enter \'Y\' to continue.\n'

stringExit = 'Enter any key to exit...\n'

stringGetLineWidth = 'please enter the transparent circle width.\n'

stringTargetFileName = 'target'
stringTargetFormat = '.png'


class currentImage:
    def __init__(self, pathImage: path):
        super().__init__()
        self.pathImage = pathImage
        self.file = Image.open(self.pathImage).convert('RGBA')
        self.width = self.file.size[0]
        self.height = self.file.size[1]

    def judgeSquare(self):
        self.length = min(self.file.size[0], self.file.size[1])
        self.radius = float(self.length / 2)
        return self.width == self.height

    def resize(self):
        self.file = self.file.resize((self.length, self.length),
                                     Image.ANTIALIAS)

    def createNewCircle(self):
        self.targetFile = Image.new('RGBA', (self.length, self.length),
                                    (255, 255, 255, 0))

    def getTargetRadius(self, lineWidth: int):
        self.targetRadius = self.radius - lineWidth

    def getPoint(self):
        self.point = self.radius

    def cut(self, lineWidth: int):
        self.getPoint()
        self.createNewCircle()
        self.getTargetRadius(lineWidth)

        pSourceImage = self.file.load()
        pTargetImage = self.targetFile.load()

        for i in range(self.length):
            for j in range(self.length):
                x = abs(i - self.point)
                y = abs(j - self.point)
                distance = pow((pow(x, 2) + pow(y, 2)), 0.5)  # 勾股定理
                if distance < self.targetRadius:
                    pTargetImage[i, j] = pSourceImage[i, j]
        self.save()

    def save(self):
        dirPath = path.split(self.pathImage)[0]
        index = 0

        while True:
            temPath = path.join(
                dirPath,
                (stringTargetFileName + str(index) + stringTargetFormat))
            if not path.exists(temPath):
                break
            index += 1

        self.targetFile.save(temPath)


def getLineWidth():
    return int(eval(input(stringGetLineWidth)))


def getPathDir():
    return input(stringGetPath)


def addBar(string: str):
    if string[:-2] != '\\':
        string += '\\'
        return string


def checkLineWidth(linewidth: int, radius: float):
    if lineWidth < 0:
        print()
        return False
    if lineWidth > radius:
        print()
        return False
    return True


while True:
    root = tkinter.Tk()
    root.withdraw()
    pathImage = filedialog.askopenfilename(
        initialdir="/",
        title=stringGetPath,
        filetypes=(("jpg files", "*.jpg"), ("png files", "*.png")),
    )

    image = currentImage(pathImage)
    if not image.judgeSquare():
        confirmation = input(stringJudgeSquareFail)
        if not (confirmation == 'Y' or confirmation == 'y'):
            continue
        image.resize()

    acquiredPathSuccess = False
    while not acquiredPathSuccess:
        lineWidth = getLineWidth()

        acquiredPathSuccess = checkLineWidth(lineWidth, image.radius)

    image.cut(lineWidth)
    print(stringExit)
    os.system('pause')
    exit(0)
