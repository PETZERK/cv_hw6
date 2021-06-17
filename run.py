import os
from time import time
import cv2
import math
import kcf_tracker

selectingObject = False
initTracking = False
onTracking = False
ix, iy, cx, cy = -1, -1, -1, -1
w, h = 0, 0

interval = 1
duration = 0.01


# mouse callback function
def draw_boundingbox(event, x, y, flags, param):
    global selectingObject, initTracking, onTracking, ix, iy, cx, cy, w, h

    if event == cv2.EVENT_LBUTTONDOWN:
        selectingObject = True
        onTracking = False
        ix, iy = x, y
        cx, cy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        cx, cy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        selectingObject = False
        if abs(x - ix) > 10 and abs(y - iy) > 10:
            w, h = abs(x - ix), abs(y - iy)
            ix, iy = min(x, ix), min(y, iy)
            initTracking = True
        else:
            onTracking = False

    elif event == cv2.EVENT_RBUTTONDOWN:
        onTracking = False
        if w > 0:
            ix, iy = x - w / 2, y - h / 2
            initTracking = True


if __name__ == '__main__':
    test_dir = os.listdir('./test_public')
    for single_label in test_dir:
        gt = open('./test_public/' + single_label + '/groundtruth.txt')
        line = gt.readline()
        label = line.split(',')
        xs = [float(label[0]), float(label[2]), float(label[4]), float(label[6])]
        ys = [float(label[1]), float(label[3]), float(label[5]), float(label[7])]
        width = math.ceil(float(max(xs)) - float(min(xs)))
        height = math.ceil(float(max(ys)) - float(min(ys)))
        ix = int(min(xs))
        iy = int(min(ys))
        w = width
        h = height

        video = cv2.VideoCapture('./videos/' + single_label + '.avi')
        tracker = kcf_tracker.KCFTracker(True, True, True)  # hog, fixed_window, multiscale
        # if you use hog feature, there will be a short pause after you draw a first bounding box, that is due to the use of Numba.
        ret, frame = video.read()
        cv2.rectangle(frame, (ix, iy), (ix + w, iy + h), (0, 255, 255), 2)
        print([ix, iy, w, h])
        tracker.init([ix, iy, w, h], frame)
        f = open('./results/' + single_label + '.txt', 'w')
        while video.isOpened():
            t0 = time()
            ok, frame = video.read()
            try:
                x, y, w, h = tracker.update(frame)
                if x < 0:
                    x = 0
                if y < 0:
                    y = 0
                print(x, y, w, h)
                f.write(str(x)+','+str(y)+','+str(x+w)+','+str(y)+','+str(x+w)+','+str(y+h)+','+str(x)+','+str(y+h)+'\n')
                t1 = time()
                cv2.rectangle(frame, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 255), 3)
                c = cv2.waitKey(interval) & 0xFF
                if c == 27 or c == ord('q'):
                    break
            except:
                break

        video.release()
        cv2.destroyAllWindows()
