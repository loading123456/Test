from paddleocr import PaddleOCR,draw_ocr
import googletrans
from PIL import Image, ImageFont, ImageDraw, ImageOps


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
        self.w = line.w
        self.eY = line.enPoint[1]
        self.text = ''

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
        return self.text

ocr = PaddleOCR(use_angle_cls=True, lang='en') 

def translate(imgPath, savePath):
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
        print(paragraph.translate())
        print("===========================================================")
    outputImg.save(savePath)


def getLines():
    pass


def transAndDraw(img, line):
        text = line[1]
        x, y = line[0][0]
        w = line[0][2][0] - line[0][0][0]
        h = line[0][2][1] - line[0][0][1]
        x, y, w, h = int(x), int(y), int(w), int(h)

        bg = Image.new(mode="RGBA", size=(w, h), color=(235, 150, 235))
        img.paste(bg, (x, y))   

        font = ImageFont.truetype(r'font/Arimo-VariableFont_wght.ttf', h)
        _, _, textWidth, textHeight = font.getbbox(text)
        if textWidth < w:
            textWidth = w
        textBox = Image.new(mode="RGBA", size=(textWidth, textHeight ), color=(0, 0, 0, 0))
        d = ImageDraw.Draw(textBox)
        d.text((0, 0), text, font=font, fill=(0, 0, 0))
        textBox.thumbnail((w, 1000  ), Image.Resampling.LANCZOS)
        textBox = textBox.crop((0, 0, w, h))
        img.paste(textBox, (x, y), textBox.convert("RGBA"))


# translate('images/1.png', 'output/1.png')
# translate('images/2.png', 'output/2.png')
# translate('images/3.png', 'output/3.png')
# translate('images/4.png', 'output/4.png')
# translate('images/5.png', 'output/5.png')
# translate('images/6.png', 'output/6.png')
# translate('images/7.png', 'output/7.png')
# translate('images/8.png', 'output/8.png')
# translate('images/9.png', 'output/9.png')
# translate('images/10.png', 'output/10.png')
# translate('images/11.png', 'output/11.png')
# translate('images/12.png', 'output/12.png')
# translate('images/13.png', 'output/13.png')
# translate('images/14.png', 'output/14.png')
# translate('images/15.png', 'output/15.png')
# translate('images/16.png', 'output/16.png')
# translate('images/17.png', 'output/17.png')
# translate('images/18.png', 'output/18.png')
# translate('images/19.png', 'output/19.png')
# translate('images/20.png', 'output/20.png')
# translate('images/21.png', 'output/21.png')
# translate('images/22.png', 'output/22.png')

translate('23.jpg', 'reult23.jpg')
# translate('24.jpg', 'reult24.jpg')
# translate('25.jpg', 'reult25.jpg')