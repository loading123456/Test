import time
from paddleocr import PaddleOCR
import googletrans
from PIL import Image, ImageFont, ImageDraw


class Line:
    def __init__(self, stPoint ,enPoint, text) -> None:
        self.stPoint = stPoint
        self.enPoint = enPoint
        self.cePoint = [(stPoint[0] + enPoint[0])/2, (stPoint[0] + enPoint[0])/2]
        self.w = enPoint[0] - stPoint[0] 
        self.h = enPoint[1] - stPoint[1] 
        self.text = text


class Paragraph:
    def __init__(self, line:Line) -> None:
        self.lines = [line]
        self.X_NOUN = 0
        self.Y_NOUN = 0
        self.epX = 0
        self.epY = line.h
        self.lineAmount = 1
        self.x = line.stPoint[0]
        self.y = line.stPoint[1]
        self.w = line.w
        self.eY = line.enPoint[1]
        self.text = ''
        self.lineHeight = 0

    def insertLine(self, line:Line):
        if self.isValid(line):
            self.update(line)
            return True
        return False

    def isValid(self, line:Line):
        if((abs(line.stPoint[1] - self.lines[-1].enPoint[1]) <= line.h * 1
                or abs(line.stPoint[1] - self.lines[-1].enPoint[1]) <= self.lines[-1].h * 1
            )
            and (abs(line.cePoint[0] - self.lines[-1].cePoint[0]) <= line.w/2
                or abs(line.cePoint[0] - self.lines[-1].cePoint[0]) <= self.lines[-1].w/2
            )
        ):
            return True
        return False

    def update(self, line:Line):
        self.lines.append(line)
        self.lineAmount += 1

        if line.stPoint[0] < self.x:
            self.x = line.stPoint[0]
        if line.w > self.w:
            self.w = line.w
        self.eY = line.enPoint[1]

        
    def translate(self):
        text = ''
        for line in self.lines:
            text += line.text + ' '
        self.text = googletrans.Translator().translate(text.lower(), dest='vi').text
        
    def draw(self, img):
        fontSize = (self.eY - self.y) * 0.95 / self.lineAmount
        lineHeight = (self.eY - self.y)/self.lineAmount
        self.lineHeight = lineHeight

        bg = Image.new(mode="RGBA", size=(abs(int(self.w)), abs(int(self.y - self.lines[-1].stPoint[1]))), color=(235, 255, 235))
        img.paste(bg, (int(self.x), int(self.y)))  

        self.insertText(self.getFontSize(fontSize), img)
    
    def getFontSize(self, nFontSize):
        fontsize = abs(int(nFontSize))
        font = ImageFont.truetype(r'font/Arimo-VariableFont_wght.ttf', fontsize)
        while font.getsize(self.text)[0] > self.w * self.lineAmount:
            fontsize -= 2
            font = ImageFont.truetype(r'font/Arimo-VariableFont_wght.ttf', fontsize)
        return fontsize

    def insertText(self, fontSize, img):
        pos = 0
        words = self.text.split()
        d = ImageDraw.Draw(img)
        for i in range(self.lineAmount):
            font = ImageFont.truetype(r'font/Arimo-VariableFont_wght.ttf', fontSize-2)
            textInLine = words[pos]
            for j in range(pos + 1,len(words)):
                if font.getsize(textInLine + ' ' + words[j])[0] <= self.w + font.getsize(words[j])[0]/2 :
                    textInLine +=  ' ' + words[j]
                else:
                    d.text((int(self.x), int(self.y + i * self.lineHeight) ), textInLine, font=font, fill=(0, 0, 0))
                    pos = j
                    break
                if j==len(words)-1:
                    d.text((int(self.x), int(self.y + i * self.lineHeight) ), textInLine, font=font, fill=(0, 0, 0))
                    pos = j
                    return

ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log = False) 

def translate(imgPath, savePath):
    print("=========================> ", imgPath," <=============================")

    st = time.time()
    outputImg  = Image.open(imgPath).convert("RGB")
    result = ocr.ocr(imgPath, cls=True, )
    lines = []

    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            lines.append(Line(line[0][0], line[0][2], line[1][0]))

    paragraphs = []

    for line in lines:
        inserted = False
        for paragraph in paragraphs:
            if paragraph.insertLine(line):
                inserted = True
                break 
        if not inserted:
            paragraphs.append(Paragraph(line))
    
    for paragraph in paragraphs:
        paragraph.translate()

    for paragraph in paragraphs:
        paragraph.draw(outputImg)

    print("Execution time: ", time.time() - st)

    outputImg.save(savePath)



# translate('images/1.jpg', 'output/1.jpg')
# translate('images/2.jpg', 'output/2.jpg')
# translate('images/3.jpg', 'output/3.jpg')
# translate('images/4.jpg', 'output/4.jpg')
# translate('images/5.jpg', 'output/5.jpg')
# translate('images/6.jpg', 'output/6.jpg')
# translate('images/7.jpg', 'output/7.jpg')
# translate('images/8.jpg', 'output/8.jpg')
# translate('images/9.jpg', 'output/9.jpg')
# translate('images/10.jpg', 'output/10.jpg')
translate('images/11.jpg', 'output/11.jpg')
# translate('images/12.jpg', 'output/12.jpg')
# translate('images/13.jpg', 'output/13.jpg')
# translate('images/14.jpg', 'output/14.jpg')
# translate('images/15.jpg', 'output/15.jpg')
# translate('images/16.jpg', 'output/16.jpg')