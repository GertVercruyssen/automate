import numpy as np
from PIL import ImageGrab
import pyautogui
import cv2
import time
from time import sleep
from AppKit import NSPasteboard, NSStringPboardType
import datetime
import sys
    
#real resolution = 2560 × 1600 fullscreen is 2880x1800, window size is 1878x1170
#pyautogui.position() is from 0x0 to 1439x899
#screen image is 2880x1800 4 channels
def main(boot):
    if boot == "b":
        booteve()
        formatted_time = datetime.datetime.now().strftime('%H:%M')
        print(formatted_time + " starting mission running")
    
    global docked
    docked = False
    global undocked
    undocked = False
    global cloaked
    cloaked = False
    global actionlist
    actionlist = ["wait5"]
    global waittimer
    waittimer = 0.0
    global waitdockticker
    waitdockticker = 0
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
        if (last_time - starttime) > 28800: #quit after 8 hours
            timetoquit = True
                        
        toprightpixel = (213, 215, 216, 255)
        toprightpixelselected = (214, 214, 214, 255)
        if toprightpixel == screenimage.getpixel((2833,660)) or toprightpixelselected == screenimage.getpixel((2833,660)):
            #print('you are undocked')
            undocked = True
        else:
            undocked = False
            
        if not undocked :
            if toprightpixel == screenimage.getpixel((2843,672)) or toprightpixelselected == screenimage.getpixel((2843,672)):
                #print('you are docked')
                docked = True
            else:
                docked = False
        else:
            docked = False
        
        if undocked:
            cyanpixel = (117, 251, 253, 255)
            if cyanpixel == screenimage.getpixel((1149,646)) and cyanpixel == screenimage.getpixel((1140,649)):
                #print('you are cloaked by gate')
                cloaked = True
            else:
                cloaked = False
            
        if timetoquit == True:
            print('time limit reached: quitting the game')
            pyautogui.press('esc')
            sleep(5)
            pyautogui.moveTo(819, 872)
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
    global waitdockticker
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
            pyautogui.moveTo(817, 760)
            pyautogui.click()
        elif currentaction == "closeconvo":
            pyautogui.moveTo(1152, 382)
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
                actionlist.insert(0,"wait1")
                if cloaked == True and sum(screenimage.getpixel((2303,816))) > 855: #object selected
                    actionlist.insert(1,"warpnext")
                    actionlist.insert(2,"waituntildocked")
                    waitdockticker = 0
                else:
                    actionlist.insert(1,"waituntildocked")
                    waitdockticker = waitdockticker+1
                    #print('waitdockticker: {}'.format(waitdockticker))
            if waitdockticker > 300: #if nothing happens for some time then autopilot
                print('failsafe engaged: unstuck with autopilot !')
                pyautogui.keyDown('ctrl')
                pyautogui.press('s')
                pyautogui.keyUp('ctrl')
                pyautogui.moveTo(1131, 489) #select fomething on the overview just to be safe
                pyautogui.click()
                sleep(35)
                pyautogui.keyDown('ctrl')
                pyautogui.press('s')
                pyautogui.keyUp('ctrl')
                waitdockticker = 0
                    
        elif currentaction == "warpnext":
            pyautogui.moveTo(1178, 406)
            pyautogui.click()
            time.sleep(5)
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
            pyautogui.moveTo(1084, 475)
            pyautogui.click(button='right')
            time.sleep(1)
            pyautogui.moveTo(1106, 511)
            pyautogui.click()
            actionlist.insert(0,"collectcargo")
        elif currentaction == "startmission":
            actionlist.insert(0,"undock")
            actionlist.insert(1,"waituntilundocked")
            actionlist.insert(2,"warpstart")
            actionlist.insert(3,"waituntildocked")
            actionlist.insert(4,"startconvo")
            actionlist.insert(5,"wait25")
            actionlist.insert(6,"completemission")
            actionlist.insert(7,"wait25")
            actionlist.insert(8,"closeconvo")
        elif currentaction == "completemission":
            time.sleep(1)
            pyautogui.moveTo(767, 761)
            pyautogui.click()
            time.sleep(1)
        elif currentaction == "warpstart":
            time.sleep(2)
            pyautogui.moveTo(566, 495)
            pyautogui.click(button='right')
            time.sleep(1)
            if (144, 228, 106, 255) == screenimage.getpixel((1250,949)):
                pyautogui.moveTo(586, 535)
                pyautogui.click()
            else:
                pyautogui.moveTo(589, 507)
                pyautogui.click()
            time.sleep(5)
            pyautogui.moveTo(1131, 489) #select fomething un the overview just to be safe
            pyautogui.click()
        else:
            print('Error: undefined action on the action queue')
            print(currentaction)
    else:
        print('no actions left, starting new plan')
        plannextactions()
        
def plannextactions():
    if docked == True:
        location = readMapLocation()
        if location == "<url=showinfo:1531//60000289 alt='Current Station'>Jatate IV - Moon 17 - Prompt Delivery Storage</url>":
            formatted_time = datetime.datetime.now().strftime('%H:%M')
            print(formatted_time + " starting new mission plan")
            if (121, 157, 72, 255) == screenimage.getpixel((1439,1446)): #agent mission already accepted
                print('finishing accepted mission')
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
                print('starting new mission')
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
            actionlist.append("warpstart")
            actionlist.append("waituntildocked")
    else:
        print('at some random point in space? going home to agent')
        actionlist.append("setdestinationagent")
        actionlist.append("wait5")
        actionlist.append("warpstart")
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
    print('maplocation is: {}'.format(location))
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

def booteve():
    waituntilevening()
    #open eve launcher
    pyautogui.keyDown('command')
    pyautogui.press('space')
    pyautogui.keyUp('command')
    pyautogui.write('eve-online')
    pyautogui.press('enter')
    #wait until ready
    time.sleep(900) #15 minutes should be enough to boot and do small updates
    #launch game
    pyautogui.moveTo(942, 400)
    time.sleep(1)
    pyautogui.click()
    time.sleep(180)
    #minimize launcher
    pyautogui.moveTo(1318, 17)
    time.sleep(2)
    pyautogui.click()
    time.sleep(2)
    pyautogui.click()
    time.sleep(5)
    pyautogui.moveTo(996, 890)
    time.sleep(2)
    pyautogui.click()
    time.sleep(2)
    #select character ???
    #minimize chat
    pyautogui.moveTo(810, 693)
    time.sleep(2)
    pyautogui.click()
    time.sleep(2)
    
def waituntilevening():
    t= datetime.datetime.today()
    future = datetime.datetime(t.year,t.month,t.day,22,0) #set until desired hour
    seconds = (future-t).total_seconds()
    print('waiting {} seconds to start the show'.format(seconds))
    time.sleep(seconds)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        boot = sys.argv[1]
    else:
        boot = "n"
    main(boot)
