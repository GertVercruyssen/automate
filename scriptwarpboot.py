import numpy as np
from PIL import ImageGrab
import pyautogui
import time
from time import sleep
from AppKit import NSPasteboard, NSStringPboardType
import datetime
import sys
import logging
    
#real resolution = 2560 × 1600 fullscreen is 2880x1800, window size is 1878x1170
#pyautogui.position() is from 0x0 to 1439x899
#screen image is 2880x1800 4 channels
def main(boot):
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M',
        filename='output.log',
        encoding='utf-8',
        level=logging.INFO)

    if boot == "b":
        booteve()
        
    output('starting mission running')
    
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
    global loopedsetdestination
    loopedsetdestination = 0 #counter to check if stuck on loop
    global candecline
    candecline = True #only once per run of the program
    last_time = time.time()
    global timetoquit
    timetoquit = False
    finished = False
    starttime = last_time
    pyautogui.moveTo(953,516)
    pyautogui.click()
    
    while(not finished):
        screenimage = ImageGrab.grab()
        deltat=time.time()-last_time
        #output('Loop took {} seconds'.format(deltat))
        last_time = time.time()
        if (last_time - starttime) > 28800: #quit after 8 hours
            timetoquit = True
                        
        toprightpixel = (213, 215, 216, 255)
        toprightpixelselected = (214, 214, 214, 255)
        if toprightpixel == screenimage.getpixel((2862,653)) or toprightpixelselected == screenimage.getpixel((2862,653)):
            #output('you are undocked')
            undocked = True
        else:
            undocked = False
            
        if not undocked :
            if toprightpixel == screenimage.getpixel((2862,672)) or toprightpixelselected == screenimage.getpixel((2862,672)):
                #output('you are docked')
                docked = True
            else:
                docked = False
        else:
            docked = False
        
        if undocked:
            cyanpixel = (117, 251, 253, 255)
            if cyanpixel == screenimage.getpixel((1149,646)) and cyanpixel == screenimage.getpixel((1140,649)): #if booster (1204,647) and (1201,647)
                #output('you are cloaked by gate')
                cloaked = True
            else:
                cloaked = False
            
        if timetoquit == True:
            output('time limit reached: quitting the game')
            pyautogui.moveTo(515, 304)
            sleep(1)
            pyautogui.click()
            finished = True
        else:
            #output('mouse is at position: {}'.format(pyautogui.position()))
            if waittimer <= 0:
                waittimer = 0.0
                nextaction()
            else:
                #output('waittimer: {}'.format(waittimer))
                #output('deltat: {}'.format(deltat))
                waittimer = waittimer-deltat
                    
    output('finished')
        
def nextaction():
    global waittimer
    global missiontitle
    global waitdockticker
    global screenimage
    global actionlist
    global loopedsetdestination
    global candecline
    global timetoquit
    
    if len(actionlist) > 0:
        currentaction = actionlist[0]
        if not currentaction.startswith("wait"):
            output('Performing action {}'.format(currentaction))
        actionlist.pop(0)
        if currentaction == "wait5":
            waittimer = 5.0
        elif currentaction == "wait75":
            waittimer = 7.5
        elif currentaction == "wait25":
            waittimer = 2.5
        elif currentaction == "wait1":
            waittimer = 1.0
        elif currentaction == "waituntilundocked":
            if undocked == False:
                actionlist.insert(0,"waituntilundocked")
                actionlist.insert(0,"wait5")
        elif currentaction == "startconvo":
            pyautogui.moveTo(626, 750)
            pyautogui.click(button='right')
            time.sleep(1)
            pyautogui.moveTo(649, 786)
            pyautogui.click()
            time.sleep(5)
            pyautogui.moveTo(800, 885)
            pyautogui.click()
        elif currentaction == "acceptmission":
            pyautogui.moveTo(916, 884)
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
            time.sleep(3)
            pyautogui.moveTo(896, 665)
            pyautogui.dragTo(894, 540, button='left')
            time.sleep(1)
            pyautogui.keyDown('optionleft')
            pyautogui.press('c')
            pyautogui.keyUp('optionleft')
            time.sleep(1)
            pyautogui.keyDown('optionleft')
            pyautogui.press('g')
            pyautogui.keyUp('optionleft')
        elif currentaction == "closeconvo":
            pyautogui.moveTo(1241, 338)
            pyautogui.click()
        elif currentaction == "setdestinationagent":
            pyautogui.moveTo(626, 750)
            pyautogui.click(button='right')
            time.sleep(1)
            pyautogui.moveTo(649, 810)
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
                    #output('waitdockticker: {}'.format(waitdockticker))
            if waitdockticker > 300: #if nothing happens for some time then autopilot
                output('failsafe engaged: unstuck with autopilot !')
                pyautogui.keyDown('ctrl')
                pyautogui.press('s')
                pyautogui.keyUp('ctrl')
                pyautogui.moveTo(1131, 489) #select fomething on the overview just to be safe
                pyautogui.click()
                sleep(35)
                waitdockticker = 0
                    
        elif currentaction == "warpnext":
            time.sleep(1)
            pyautogui.moveTo(1178, 406)
            pyautogui.click()
            time.sleep(5)
        elif currentaction == "readmissiontitle":
            pyautogui.moveTo(1014, 360)
            pyautogui.click(clicks=3, interval=0.25)
            pyautogui.keyDown('command')
            pyautogui.press('c')
            pyautogui.keyUp('command')
            missiontitle = getClipboard()
            output('current mission is {}'.format(missiontitle))
        elif currentaction == "setmissionroute":
            #Currently only supporting drop-off missions
            pyautogui.moveTo(1132, 439)
            pyautogui.click(button='right')
            time.sleep(1)
            pyautogui.moveTo(1152, 474)
            pyautogui.click()
            time.sleep(1)
            actionlist.insert(0,"checkroute")
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
            actionlist.insert(9,"wait25")
            actionlist.insert(10,"setdestinationagent")
            actionlist.insert(11,"undock")
            actionlist.insert(12,"waituntilundocked")
            actionlist.insert(13,"warpstart")
            actionlist.insert(14,"waituntildocked")
        elif currentaction == "completemission":
            time.sleep(1)
            pyautogui.moveTo(866, 883)
            pyautogui.click()
            time.sleep(1)
        elif currentaction == "warpstart":
            time.sleep(1)
            pyautogui.moveTo(565, 494)
            time.sleep(1)
            pyautogui.moveTo(566, 495)
            time.sleep(1)
            pyautogui.click(button='right')
            time.sleep(1)
            screenimage = ImageGrab.grab()
            if (196, 197, 197, 255) == screenimage.getpixel((1169,1081)):
                pyautogui.moveTo(587, 535)
                pyautogui.click()
            else:
                pyautogui.moveTo(587, 511)
                pyautogui.click()
            time.sleep(5)
            pyautogui.moveTo(1131, 489) #select fomething un the overview just to be safe
            pyautogui.click()
        elif currentaction == "checkroute":
            route = checkforjumpword()
            if not route:
                actionlist.insert(0,"setmissionroute")
                loopedsetdestination = loopedsetdestination+1
                if loopedsetdestination > 4: #stuck in a loop, probably trying to go to lowsec
                    loopedsetdestination = 0
                    if candecline:
                        output('declining. Resetting the convo and actionlist')
                        candecline = False
                        pyautogui.moveTo(962, 885)
                        time.sleep(1)
                        takeScreenshot('declined')
                        time.sleep(1)
                        pyautogui.click()
                        time.sleep(10)
                        pyautogui.moveTo(980, 337)
                        time.sleep(1)
                        pyautogui.click()
                        actionlist = ["wait1"]
                    else:
                        output('No decline available, quitting game')
                        actionlist = ["wait1"]
                        timetoquit = True
                else:
                    actionlist.insert(0,"setmissionroute")
            else:
                loopedsetdestination = 0
        else:
            output('Error: undefined action on the action queue')
            output(currentaction)
    else:
        output('no actions left, starting new plan')
        plannextactions()
        
def plannextactions():
    if docked == True:
        location = readMapLocation()
        if location == "<url=showinfo:1927//60008464 alt='Current Station'>Finid X - Moon 1 - Amarr Navy Assembly Plant</url>":
            output('starting new mission plan')
            if (121, 157, 72, 255) == screenimage.getpixel((1439,1446)): #agent mission already accepted
                output('finishing accepted mission')
                actionlist.append("startconvo")
                actionlist.append("wait75")
                actionlist.append("readmissiontitle")
                actionlist.append("wait1")
                actionlist.append("setmissionroute")
                actionlist.append("wait25")
                actionlist.append("closeconvo")
                actionlist.append("wait1")
                actionlist.append("startmission")
            else:
                actionlist.append("startconvo") #agent mission offered or no agent mission
                output('starting new mission')
                actionlist.append("wait75")
                actionlist.append("readmissiontitle")
                actionlist.append("wait1")
                actionlist.append("setmissionroute")
                actionlist.append("wait25")
                actionlist.append("acceptmission")
                actionlist.append("wait25")
                actionlist.append("collectcargo")
                actionlist.append("wait1")
                actionlist.append("closeconvo")
                actionlist.append("wait1")
                actionlist.append("startmission")
                
        else:
            output('at some random station? going home to agent')
            actionlist.append("setdestinationagent")
            actionlist.append("undock")
            actionlist.append("waituntilundocked")
            actionlist.append("warpstart")
            actionlist.append("waituntildocked")
    else:
        output('at some random point in space? going home to agent')
        actionlist.append("setdestinationagent")
        actionlist.append("wait5")
        actionlist.append("warpstart")
        actionlist.append("waituntildocked")
        
def readMapLocation():
    output('checking location on the map')
    pyautogui.press('f10')
    time.sleep(5)
    pyautogui.moveTo(572, 409)
    pyautogui.click(button='right')
    time.sleep(1)
    pyautogui.moveTo(607, 520)
    pyautogui.click()
    location = getClipboard()
    output('maplocation is: {}'.format(location))
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
    #output(type(text))
    #print u"Pastboard string: %s".encode("utf-8") % repr(pbstring)
    return pbstring

def booteve():
    output('I have awoken!')
    takeScreenshot('test1')
    #open eve launcher
    pyautogui.keyDown('command')
    time.sleep(1)
    pyautogui.press('space')
    pyautogui.keyUp('command')
    time.sleep(1)
    pyautogui.write('eve-online')
    pyautogui.press('enter')
    #wait until ready
    time.sleep(600) #some minutes should be enough to boot and do small updates
    takeScreenshot('test2')
    #launch game
    output('launching game')
    pyautogui.moveTo(942, 400)
    time.sleep(1)
    pyautogui.click()
    time.sleep(120) #2 minutes to boot should be enough test
    takeScreenshot('test3')
    #minimize launcher
    #output('minimize launcher')
    #pyautogui.moveTo(1318, 17)
    #time.sleep(2)
    #pyautogui.click()
    #time.sleep(2)
    #pyautogui.click()
    #time.sleep(5)
    #pyautogui.moveTo(996, 890)
    #time.sleep(2)
    #pyautogui.click()
    #time.sleep(2)
    #minimize chat
    output('minimize chat')
    pyautogui.moveTo(810, 693)
    time.sleep(2)
    pyautogui.click()
    time.sleep(2)
    takeScreenshot('test4')
    
def waituntilevening():
    t= datetime.datetime.today()
    future = datetime.datetime(t.year,t.month,t.day,22,0) #set until desired hour
    seconds = (future-t).total_seconds()
    output('waiting {} seconds to start the show'.format(seconds))
    time.sleep(seconds)
    
def checkforjumpword():
    y = 788
    first = sum(screenimage.getpixel((1211,y))) - 255 #dark
    second = sum(screenimage.getpixel((1213,y))) - 255 #white
    third = sum(screenimage.getpixel((1214,y))) - 255 #dark
    fourth = sum(screenimage.getpixel((1216,y))) - 255 #white
    fifth = sum(screenimage.getpixel((1218,y))) - 255 #dark
    sixth = sum(screenimage.getpixel((1220,y))) - 255 #white
    seventh = sum(screenimage.getpixel((1221,y))) - 255 #dark
    eighth = sum(screenimage.getpixel((1223,y))) - 255 #white
    
    if first < second and second > third and third < fourth and fourth > fifth and fifth < sixth and sixth > seventh and seventh < eighth:
        return True
    else:
        return False
        
def output(text):
    print(text)
    logging.info(text)

def takeScreenshot(name = 0):
    if name == 0:
        name = time.time()
    screenshot = ImageGrab.grab()
    screenshot.save(name+'.png')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        boot = sys.argv[1]
    else:
        boot = "n"
    main(boot)
