'''
All screen coordinates are in x,y,width,height format, where x,y, is the top-left corner
'''

from mss import MSS
import cv2
import numpy as np
import pywinctl

aw = pywinctl.getActiveWindow()

def FindMoney():
    DigitTemplates = {}
    for i in range(10):
        DigitTemplates[i] = cv2.imread(f'DigitCurrency/{i}.png', cv2.IMREAD_GRAYSCALE)

    with MSS() as sct:
        ScreenshotRegion = {'left' : aw.left, 'top' : aw.top, 'width' : aw.width, 'height' : aw.height}
        Screenshot = sct.grab(ScreenshotRegion)
        ScreenshotArrayBGRA = np.array(Screenshot)
        ScreenshotArrayGREY = cv2.cvtColor(ScreenshotArrayBGRA, cv2.COLOR_BGRA2GRAY)
        ScreenshotArrayTHRESH = cv2.threshold(ScreenshotArrayGREY, 175, 255, cv2.THRESH_BINARY)
        Matches = []
        for i in range(10):
            TemplateMatches = cv2.matchTemplate(ScreenshotArrayTHRESH[1], DigitTemplates[i], cv2.TM_CCOEFF_NORMED)
            MatchLocations = np.where(TemplateMatches >= 0.8)
            for pt in zip(*MatchLocations[::-1]):
                score = TemplateMatches[pt[1], pt[0]]
                Matches.append({'x': pt[0], 'digit': i, 'score': score})
        Matches.sort(key=lambda m: m['x'])
        FinalMatches = []
        if Matches:
            FinalMatches.append(Matches[0])
            for current in Matches[1:]:
                last = FinalMatches[-1]
                if current['x'] - last['x'] < 8: 
                    if current['score'] > last['score']:    #this is the only code i took from the internet,
                        FinalMatches[-1] = current          # the non-maximum suppression.
                else:
                    FinalMatches.append(current)
        try:
            return int(''.join(str(m['digit']) for m in FinalMatches))    
        except:
            return 0

def gate_color_match(rgbList, rgbWanted, threshold):
    return all(abs(c1-c2) < threshold for c1,c2 in zip(rgbList, rgbWanted))

def GateByColor(RGBList):
    Thresh = 20
    gate_info = {
        (85,165,200):("ScoreGate",10),
        (200,135,60):("FuelGate",10),
        (200,70,65):("SpeedGate",10),
        (70,150,60):("LuckyGate",10),
        (175,160,65):("GoldGate", 10),
        (145,145,160):("NormalGate",5)
    }

    for target_rgb, (gateName, cost) in gate_info.items():
        if gate_color_match(RGBList, target_rgb, Thresh):
            return[gateName,cost]
    else:
        return None
    
def FindGates():
    with MSS() as sct:
        ScreenshotRegion = {'left' : aw.left, 'top' : aw.top, 'width' : aw.width, 'height' : aw.height}
        capture = sct.grab(ScreenshotRegion)
        #there has GOT to be a better way to do this
        Slot1Color = capture.pixel(int(aw.width*.5078125), int(aw.height*.1893939))
        Slot2Color = capture.pixel(int(aw.width*.5781250), int(aw.height*.1893939))
        Slot3Color = capture.pixel(int(aw.width*.6510416), int(aw.height*.1893939))
        Slot4Color = capture.pixel(int(aw.width*.7213541), int(aw.height*.1893939))
        RerollToF = capture.pixel(int(aw.width*.8333333), int(aw.height*.2604166))
        if abs((RerollToF[0]) - 40) < 15 and \
        abs(RerollToF[1] - 35) < 15 and \
        abs(RerollToF[2] - 15) < 15: 
            RerollAvailable = True
        else:
            RerollAvailable = False
        print('DEBUG -- RGB values for slots are:', Slot1Color,Slot2Color,Slot3Color,Slot4Color,RerollToF)
        Slot1Info = GateByColor(Slot1Color)
        Slot2Info = GateByColor(Slot2Color)
        Slot3Info = GateByColor(Slot3Color)
        Slot4Info = GateByColor(Slot4Color)
        return [[Slot1Info, Slot2Info, Slot3Info, Slot4Info], RerollAvailable]
    
