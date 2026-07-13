from Vision import FindGates, FindMoney
import pyautogui
import pywinctl
import time as t
import numpy as np
from mss import MSS
from utils import err, succ, warn

# startup
loopler_focused = False
debug = False
t.sleep(3)

try:
    all_windows = pywinctl.getAllTitles()
    if debug:
        print(f"all active windows: {all_windows}")
except Exception as e: 
    err('pywinctl bad permissions')
    print(f'An error has occured. if you see this, it is likely that you are on wayland on linux. this script only works with x11. please switch.')
    exit()

if not "The Loopler Demo" in all_windows:
    print('the loopler is not open!')
    exit()

if pywinctl.getActiveWindow() != "The Loopler Demo":
    try:
        windows = pywinctl.getWindowsWithTitle("The Loopler Demo")
        print(windows)
        if windows:
            window = windows[0]
            window.activate()
            window.maximize()
            t.sleep(.333)
            loopler_focused = True
            if debug:
                print("try/execept reached end of try successfully")

    except Exception as e:
        print(f"Exception error, is loopler open? exception: {e}")
        if debug:
            print("try/except reached end with exception successfully")
        exit()
        
active_window = pywinctl.getActiveWindow()
active_window_name = pywinctl.getActiveWindowTitle()

if debug:
    print(active_window, active_window_name)

if loopler_focused == True:
    with MSS() as sct:
        ScreenshotRegion = {
            'left' : active_window.left,
            'top' : active_window.top,
            'width' : active_window.width, 
            'height' : active_window.height}
        Screenshot = sct.grab(ScreenshotRegion)
        if debug:
            print('mss screenshot successfull')
            print(Screenshot)
#        foo = np.array(Screenshot)
#        img = cv2.cvtColor(foo,cv2.COLOR_BGRA2BGR)
#        cv2.imwrite("test.png", img)

# memory
GateSlot = {
    1 : {'GateType' : None, 'Level' : 0},
    2 : {'GateType' : None, 'Level' : 0},
    3 : {'GateType' : None, 'Level' : 0},
    4 : {'GateType' : None, 'Level' : 0},
    5 : {'GateType' : None, 'Level' : 0},
    6 : {'GateType' : None, 'Level' : 0},
}


def PrintInfoStatements():
    Gates = FindGates()
    Money = int(FindMoney())
    t.sleep(.1)
    print(f'INFO -- Amount of gold: {Money}')
    print(f'INFO -- Reroll available: {Gates[1]}')
    for i in range(6):
        print(f'Map gate Slot {i+1} contains: {GateSlot[i+1]}')
    for i in range(4):
        if Gates[0][i] != None:
            print(f'INFO -- Shop gate slot {i+1} contains {Gates[0][i][0]}, at price {Gates[0][i][1]}')
        else:
            print(f'INFO -- Shop gate slot {i+1} is empty')

def GhostSlot():
    if GateSlot[4]['GateType'] == None:
        return 0
    elif GateSlot[5]['GateType'] == None: 
        return 1
    elif GateSlot[6]['GateType'] == None:
        return 2
    #-----
    LowestSlotLevel = 4
    if GateSlot[5]['Level'] < GateSlot[LowestSlotLevel]['Level']:
        LowestSlotLevel = 5
    if GateSlot[6]['Level'] < GateSlot[LowestSlotLevel]['Level']:
        LowestSlotLevel = 6
    return LowestSlotLevel - 4

def CheckGateName(GateName, Gates):
    Money = int(FindMoney())
    ClickLocations = [[980,350],[1115,350],[1255,350],[1390,350]]
    PlaceLocations = [[535,250],[275,515],[535,750]]
    for i in range(4):
        if Gates[0][i] != None:
            if Gates[0][i][0] == GateName and Gates[0][i][1] <= Money:
                Money = Money - Gates[0][i][1]
                pyautogui.click(ClickLocations[i])
                t.sleep(.3)
                Slot = GhostSlot()
                pyautogui.click(PlaceLocations[Slot])
                t.sleep(.25)
                GateSlot[Slot]['GateType'] = GateName
                GateSlot[Slot]['Level'] += 1
                print(f'INFO -- Bought {GateName} from slot {i+1} for {Gates[0][i][1]} gold')
                print(f'INFO -- Gold is now {Money}')

def BuyGates():
    Gates = FindGates()
    CheckGateName('GhostGate', Gates)
    CheckGateName('FuelGate', Gates)
    CheckGateName('SpeedGate', Gates)
    CheckGateName('GoldGate', Gates)
    
    if Gates[1] == True:
        print('INFO -- Attempting to reroll shop')
        pyautogui.click(1560,275)
        t.sleep(.25)
        print(f'Gold is now {FindMoney()} after rerolling')
        t.sleep(2)
        BuyGates()
    else:
        print('This shop is finished. Input anything in terminal when you are at the next shop to contine.')
        input()
        PrintInfoStatements()
        BuyGates()
        
PrintInfoStatements()
BuyGates()



