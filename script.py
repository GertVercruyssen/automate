import numpy as np
from PIL import ImageGrab
import pyautogui
import cv2
import time
from time import sleep
from AppKit import NSPasteboard, NSStringPboardType
import datetime
    
#real resolution = 2560 × 1600 fullscreen is 2880x1800, window size is 1878x1170
#pyautogui.position() is from 0x0 to 1439x899
#screen image is 2880x1800 4 channels
def main():
    global docked
    docked = False
    global undocked
    undocked = False
    global actionlist
    actionlist = ["wait5"]
    global waittimer
    waittimer = 0.0
    global screenimage
    global missiontitle
    last_time = time.time()
    timetoquit = False
    finished = False
    #cv2.namedWindow ('window', cv2.WINDOW_NORMAL)
    starttime = last_time
    pyautogui.moveTo(953,516)
    pyautogui.click()
    
    while(not finished):
        screenimage = ImageGrab.grab()
        screen = np.array(screenimage)
        deltat=time.time()-last_time
        #print('Loop took {} seconds'.format(deltat))
        last_time = time.time()
        if (last_time - starttime) > 10800: #after how many seconds should this quit?
            timetoquit = True
            
        whitepixel = (255, 255, 255, 255)
        if whitepixel == screenimage.getpixel((1783,1747)) and whitepixel == screenimage.getpixel((1778,1760)) and whitepixel == screenimage.getpixel((1789,1760)):
            #print('you are undocked')
            undocked = True
        else:
            undocked = False
        
        stationmenupixel = (23, 23, 23, 255)
        stationmenuactivepixel = (21, 23, 25, 255)
        if ((stationmenupixel == screenimage.getpixel((2511,1526)) and stationmenupixel == screenimage.getpixel((2855,1526))) or (stationmenuactivepixel == screenimage.getpixel((2511,1526)) and stationmenuactivepixel == screenimage.getpixel((2855,1526)))) and ( stationmenupixel != screenimage.getpixel((2511,1530)) and stationmenupixel != screenimage.getpixel((2855,1530))):
            #print('you are docked')
            docked = True
        else:
            docked = False
            
        if timetoquit == True:
            print('time limit reached: quitting the game')
            pyautogui.press('esc')
            sleep(5)
            pyautogui.moveTo(1219, 803)
            pyautogui.click()
            finished = True
        else:
            #print('mouse is at position: {}'.format(pyautogui.position()))
            if waittimer <= 0:
                waittimer = 0.0
                nextaction()
            else:
                #print('waittimer: {}'.format(waittimer))
                #print('deltat: {}'.format(deltat))
                waittimer = waittimer-deltat
                    
    formatted_time = datetime.datetime.now().strftime('%H:%M')
    print(formatted_time + " finished")
        #cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)) #WINDOW_NORMAL
        #if cv2.waitKey(1) % 0xFF == ord('q'):
        #    cv2.destroyAllWindows()
        #    break
        
def nextaction():
    global waittimer
    global missiontitle
    if len(actionlist) > 0:
        currentaction = actionlist[0]
        if not currentaction.startswith("wait"):
            print('Performing action {}'.format(currentaction))
        actionlist.pop(0)
        if currentaction == "wait5":
            waittimer = 5.0
        elif currentaction == "wait10":
            waittimer = 10.0
        elif currentaction == "wait25":
            waittimer = 2.5
        elif currentaction == "wait1":
            waittimer = 1.0
        elif currentaction == "waituntilundocked":
            if undocked == False:
                actionlist.insert(0,"waituntilundocked")
                actionlist.insert(0,"wait5")
        elif currentaction == "startconvo":
            pyautogui.moveTo(626, 735)
            pyautogui.click(button='right')
            time.sleep(1)
            pyautogui.moveTo(649, 771)
            pyautogui.click()
        elif currentaction == "acceptmission":
            pyautogui.moveTo(891, 692)
            pyautogui.click()
        elif currentaction == "closeconvo":
            pyautogui.moveTo(1193, 379)
            pyautogui.click()
        elif currentaction == "pressbluebutton":
            pyautogui.moveTo(642, 598)
            pyautogui.click()
        elif currentaction == "collectcargo":
            pyautogui.keyDown('optionleft')
            pyautogui.press('c')
            pyautogui.keyUp('optionleft')
            time.sleep(1)
            pyautogui.keyDown('optionleft')
            pyautogui.press('g')
            pyautogui.keyUp('optionleft')
            time.sleep(1)
            pyautogui.moveTo(896, 661)
            pyautogui.dragTo(908, 544, button='left')
            time.sleep(1)
            pyautogui.keyDown('optionleft')
            pyautogui.press('c')
            pyautogui.keyUp('optionleft')
            time.sleep(1)
            pyautogui.keyDown('optionleft')
            pyautogui.press('g')
            pyautogui.keyUp('optionleft')
        elif currentaction == "closeconvo":
            pyautogui.moveTo(1193, 379)
            pyautogui.click()
        elif currentaction == "setdestinationagent":
            pyautogui.moveTo(626, 735)
            pyautogui.click(button='right')
            time.sleep(1)
            pyautogui.moveTo(649, 795)
            pyautogui.click()
        elif currentaction == "undock":
            pyautogui.keyDown('optionleft')
            pyautogui.press('u')
            pyautogui.keyUp('optionleft')
            time.sleep(7)
        elif currentaction == "autopilot":
            pyautogui.keyDown('ctrl')
            pyautogui.press('s')
            pyautogui.keyUp('ctrl')
        elif currentaction == "waituntildocked":
            if docked == False:
                #toggle MWD
                pyautogui.keyDown('optionleft')
                pyautogui.press('f1')
                pyautogui.keyUp('optionleft')
                actionlist.insert(0,"waituntildocked")
                actionlist.insert(0,"wait5")
        elif currentaction == "readmissiontitle":
            pyautogui.moveTo(960, 402)
            pyautogui.click(clicks=3, interval=0.25)
            pyautogui.keyDown('command')
            pyautogui.press('c')
            pyautogui.keyUp('command')
            missiontitle = getClipboard()
            print('current mission is {}'.format(missiontitle))
        elif currentaction == "prepmission":
            #Currently only supporting drop-off missions
            pyautogui.moveTo(1096, 487)
            pyautogui.click(button='right')
            time.sleep(1)
            pyautogui.moveTo(1117, 524)
            pyautogui.click()
            actionlist.insert(0,"collectcargo")
        elif currentaction == "startmission":
            actionlist.insert(0,"undock")
            actionlist.insert(1,"waituntilundocked")
            actionlist.insert(2,"autopilot")
            actionlist.insert(3,"waituntildocked")
            actionlist.insert(4,"startconvo")
            actionlist.insert(5,"wait25")
            actionlist.insert(6,"completemission")
            actionlist.insert(7,"wait25")
            actionlist.insert(8,"closeconvo")
        elif currentaction == "completemission":
            time.sleep(1)
            pyautogui.moveTo(853, 692)
            pyautogui.click()
            time.sleep(1)
            
        else:
            print('Error: undefined action on the action queue')
            print(currentaction)
    else:
        print('no actions left, starting new plan')
        plannextactions()
        
def plannextactions():
    if docked == True:
        location = readMapLocation()
        if location == "<url=showinfo:1529//60004462 alt='Current Station'>Itamo VI - Moon 6 - Science and Trade Institute School</url>":
            formatted_time = datetime.datetime.now().strftime('%H:%M')
            print(formatted_time + " starting new mission plan")
            if (121, 157, 72, 255) == screenimage.getpixel((2839,1213)): #agent mission already accepted
                actionlist.append("startconvo")
                actionlist.append("wait10")
                actionlist.append("readmissiontitle")
                actionlist.append("wait25")
                actionlist.append("prepmission")
                actionlist.append("wait25")
                actionlist.append("closeconvo")
                actionlist.append("wait25")
                actionlist.append("startmission")
            else:
                actionlist.append("startconvo") #agent mission offered or no agent mission
                actionlist.append("wait10")
                actionlist.append("readmissiontitle")
                actionlist.append("wait25")
                actionlist.append("acceptmission")
                actionlist.append("wait25")
                actionlist.append("prepmission")
                actionlist.append("wait25")
                actionlist.append("closeconvo")
                actionlist.append("wait25")
                actionlist.append("startmission")
                
            #offeredpixel = (214, 154, 63, 255)
            #if offeredpixel == screenimage.getpixel((2837,1213)):
                
        else:
            print('at some random station? going home to agent')
            actionlist.append("setdestinationagent")
            actionlist.append("undock")
            actionlist.append("waituntilundocked")
            actionlist.append("autopilot")
            actionlist.append("waituntildocked")
    else:
        print('at some random point in space? going home to agent')
        actionlist.append("setdestinationagent")
        actionlist.append("wait25")
        actionlist.append("autopilot")
        actionlist.append("waituntildocked")
        
def readMapLocation():
    print('checking location on the map')
    pyautogui.press('f10')
    time.sleep(5)
    pyautogui.moveTo(572, 409)
    pyautogui.click(button='right')
    time.sleep(1)
    pyautogui.moveTo(607, 520)
    pyautogui.click()
    location = getClipboard()
    print('debug, maplocation was: {}'.format(location))
    pyautogui.press('f10')
    time.sleep(3)
    return location

def generateHash(xfirst, xsecond, y):
    hash = 0
    for x in range(xfirst, xsecond, 2): #2 is precision, be careful invalidates all hashes
        currentpixel = screenimage.getpixel((x,y))
        hash = hash + currentpixel[0]
    else:
        return hash
        
def getClipboard():
    pb = NSPasteboard.generalPasteboard()
    pbstring = pb.stringForType_(NSStringPboardType)
    #print(type(text))
    #print u"Pastboard string: %s".encode("utf-8") % repr(pbstring)
    return pbstring

if __name__ == '__main__':
    main()
