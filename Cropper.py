from PIL import Image
from os import path
import os
import tkinter
from tkinter import filedialog

stringGetPath = 'Please select your image'

stringJudgeSquareFail = 'The image is not square and will be cropped.\n\
Enter \'Y\' to continue.\n'

stringExit = 'Enter any key to exit...\n'

stringGetLineWidth = 'please enter the border width.\n'
stringImageSize = '(image width = {0}, image height = {1},\
 recommended width = {2}.)\n'

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

    def getTargetRadius(self):
        self.targetRadius = self.radius - self.lineWidth

    def getPoint(self):
        self.point = self.radius

    def cut(self):
        self.getPoint()
        self.createNewCircle()
        self.getTargetRadius()

        pSourceImage = self.file.load()
        pTargetImage = self.targetFile.load()

        for i in range(self.length):
            for j in range(self.length):
                x = abs(i - self.point)
                y = abs(j - self.point)
                distance = pow((pow(x, 2) + pow(y, 2)), 0.5)  # 勾股定理
                if distance < self.targetRadius:
                    pTargetImage[i, j] = pSourceImage[i, j]
                if distance < self.radius and distance >= self.targetRadius:
                    tem = list(pSourceImage[i, j])
                    colorPerPx = 255 / self.lineWidth
                    px = distance - self.targetRadius
                    for t in range(3):
                        '''tem[t] += int(colorPerPx * px)'''
                        if tem[t] > 255:
                            tem[t] = 255
                    tem[3] -= int(colorPerPx * px)
                    pTargetImage[i, j] = tuple(tem)
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

    def getLineWidth(self):
        print(stringGetLineWidth, end='')
        print(stringImageSize.format(self.file.width, self.file.height,
                                     int(self.height / 10)),
              end='')
        self.lineWidth = int(eval(input('')))


def getPathDir():
    return input(stringGetPath)


def addBar(string: str):
    if string[:-2] != '\\':
        string += '\\'
        return string


def checkLineWidth(lineWidth: int, radius: float):
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
        image.getLineWidth()

        acquiredPathSuccess = checkLineWidth(image.lineWidth, image.radius)

    image.cut()
    print(stringExit)
    os.system('pause')
    exit(0)
