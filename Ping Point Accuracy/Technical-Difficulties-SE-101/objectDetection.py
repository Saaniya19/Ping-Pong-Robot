import cv2
import numpy as np
import math

CAMERA_DEVICE_ID = 0
IMAGE_WIDTH = 320
IMAGE_HEIGHT = 240

hsv_min = np.array((50, 80, 80))
hsv_max = np.array((120, 255, 255))

colors = []

def isset(v):
    try:
        type (eval(v))
    except:
        return 0
    else:
        return 1

def on_mouse_click(event, x, y, flags, frame):
    global colors
    
    if event == cv2.EVENT_LBUTTONUP:
        color_bgr = frame[y, x]
        color_rgb = tuple(reversed(color_bgr))
        
        print(color_rgb)
        
        color_hsv = rgb2hsv(color_rgb[0], color_rgb[1], color_rgb[2])
        print(color_hsv)
        
        colors.append(color_hsv)
        
        print(colors)
        
def hsv2rgb(h, s, v):
    h = float(h) * 2
    s = float(s) / 255
    v = float(v) / 255
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return (r, g, b)

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    diff = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/diff) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/diff) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/diff) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = diff/mx
    v = mx

    h = int(h / 2)
    s = int(s * 255)
    v = int(v * 255)

    return (h, s, v)

if __name__ == "__main__":
    try:
        #create video capture
        cap = cv2.VideoCapture(CAMERA_DEVICE_ID)
        
        #set resolution to 320x240 to reduce latency
        cap.set(3, IMAGE_WIDTH)
        cap.set(4, IMAGE_HEIGHT)
        
        while True:
            #read frames from the camera
            _, frame = cap.read()
            frame = cv2.blur(frame, (3, 3))
            
            #convert the image to hsv and find range of colors
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            cv2.setMouseCallback('frame', on_mouse_click, frame)
            
            #set color threshhold (filter, needs to be adjusted to proper values)
            #thresh = cv2.inRange(hsv, np.array((120, 80, 80)), np.array((180, 255, 255)))
            
            #find color using threshhold
            if colors:
                #find max & min h, s, v
                minh = min(c[0] for c in colors)
                mins = min(c[1] for c in colors)
                minv = min(c[2] for c in colors)
                maxh = max(c[0] for c in colors)
                maxs = max(c[1] for c in colors)
                maxv = max(c[2] for c in colors)
                
                print("New HSV threshold: ", (minh, mins, minv), (maxh, maxs, maxv))
                hsv_min = np.array((minh, mins, minv))
                hsv_max = np.array((maxh, maxs, maxv))
            
            thresh = cv2.inRange(hsv, hsv_min, hsv_max)
            thresh2 = thresh.copy()
            
            #find contours in threshold (filtered) image
            (major_ver, minor_ver, subminor_ver) = (cv2.__version__.split('.'))
            
            #findContours() has different form for opencv2 and opencv3 (includes boolean or not)
            if major_ver == "2" or major_ver == "3":
                _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            else:
                contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            
            #find contour with max area (most of that color, likely the object) and store it
            max_area = 0
            for cont in contours:
                area = cv2.contourArea(cont)
                if area > max_area:
                    max_area = area
                    best_cont = cont
            
            #find centroids of best_cont and draw a circle there
            if isset('best_cont'):
                M = cv2.moments(best_cont)
                cx, cy = int(M['m10'] / M['m00'], int(M['m01'] / M['m00']))
                cv2.circle(frame(cx, cy), 5, 255, -1)
                print("Central pos: (%d, %d)" % (cx, cy))
            else:
                print("[Warning]Tag lost...")
            
            #show original and processed image
            cv2.imshow('frame', frame)
            cv2.imshow('thresh', thresh2)
            
            #if escape key is press, exit loop
            if cv2.waitKey(33) == 27:
                break
    except Exception as e:
        print(e)
    finally:
        #clean up and exit program
        cv2.destroyAllWindows()
        cap.release()
        
        