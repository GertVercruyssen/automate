import numpy as np
from PIL import ImageGrab
import pyautogui
import cv2
import time
    
docked = False
undocked = False
#real resolution = 2560 × 1600 fullscreen is 2880x1800, window size is 1878x1170
#pyautogui.position() is from 0x0 to 1439x899
#screen image is 2880x1800 4 channels
def main():
    last_time = time.time()
    global screenimage
    #cv2.namedWindow ('window', cv2.WINDOW_NORMAL)
    while(True):
        screenimage = ImageGrab.grab()
        screen = np.array(screenimage)
        deltat=time.time()-last_time
        print('Loop took {} seconds'.format(deltat))
        last_time = time.time()
        #print('should be near white for autopilot:')
        whitepixel = (255, 255, 255, 255)
        if whitepixel == screenimage.getpixel((1783,1747)) and whitepixel == screenimage.getpixel((1778,1760)) and whitepixel == screenimage.getpixel((1789,1760)):
            print('you are undocked')
        
        stationmenupixel = (23, 23, 23, 255)
        if (stationmenupixel == screenimage.getpixel((2519,1505)) and stationmenupixel == screenimage.getpixel((2819,1505))) and ( stationmenupixel != screenimage.getpixel((2519,1530)) and stationmenupixel != screenimage.getpixel((2819,1530))):
            print('you are docked')
        
        hash = generateHash(1125,1402,819)
        hash = hash + generateHash(1125,1402,812)
        print('hash generated is: {}'.format(hash))
        
        print('mouse is at position: {}'.format(pyautogui.position()))
        
        
        #cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)) #WINDOW_NORMAL
        #if cv2.waitKey(1) % 0xFF == ord('q'):
        #    cv2.destroyAllWindows()
        #    break

def generateHash(xfirst, xsecond, y):
    hash = 0
    for x in range(xfirst, xsecond, 2):
        currentpixel = screenimage.getpixel((x,y))
        hash = hash + currentpixel[0]
    else:
        return hash

if __name__ == '__main__':
    main()
