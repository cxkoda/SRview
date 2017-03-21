import cv2
from libSRview.SRview import SRview

video = cv2.VideoCapture('/home/dave/work/SRview/dragster.mp4')
videoFormat = [int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(video.get(cv2.CAP_PROP_FRAME_WIDTH))]

srview = SRview(videoFormat)
v = 0

while(video.isOpened()):
    ret, frame = video.read()
    SRframe = srview(frame)

    #gray = cv2.cvtColor(SRframe, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame', SRframe)

    k = cv2.waitKey(1)

    if k == ord('q'):
        break
    elif k == ord('r'):
        v = 0
        print(v)
        srview.setSpeed(v)
    elif k == ord('+'):
        v += (1-v)*0.1
        print(v)
        srview.setSpeed(v)
    elif k == ord('-'):
        v -= (1-v)*0.1
        print(v)
        srview.setSpeed(v)

video.release()
cv2.destroyAllWindows()