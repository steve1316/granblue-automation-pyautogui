import cv2 as cv
import numpy as np
import pyautogui



def on_mouse(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDOWN:
        print('x = %d, y = %d'%(x, y))
        print(frame.getpixel((x,y)))

def check_bgr_pixel(pt1 = None , pt2 = None):
    """ Get the pixel value

    Args:
        pt1, pt2 : tuple points that define the scope

    Returns:
        None
    """
    if pt1 != None and pt2 != None:
        start, top = pt1
        end, bottom = pt2
    else:
        start, top = 0 , 0
        end, bottom = pyautogui.size()
    
    global frame   
    frame = pyautogui.screenshot(region=(start, top, end, bottom))
    img = cv.cvtColor(np.array(frame), cv.COLOR_BGR2RGB)

    cv.namedWindow("debug")
    cv.setMouseCallback("debug", on_mouse)

    while(1):
        cv.imshow("debug",img)
        k = cv.waitKey(20) & 0xFF
        if k == 27:
            break
    
    # closing all open windows
    cv.destroyAllWindows()

check_bgr_pixel((0,0),(960, 1080))