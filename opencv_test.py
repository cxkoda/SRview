import numpy as np
from scipy import interpolate
from scipy import ndimage
import cv2
#import matplotlib.pyplot as plt


video = cv2.VideoCapture('las_vegas.mp4')
videoFormat = [int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(video.get(cv2.CAP_PROP_FRAME_WIDTH))]


thetas = np.linspace(0, np.pi, videoFormat[0])
phis = np.linspace(0, 2*np.pi, videoFormat[1])


def global2local(theta, phi):
    eta = np.sqrt(1 - np.square(np.sin(theta)*np.cos(phi)))
    return np.arctan2(eta, -np.sin(theta)*np.cos(phi)), np.arctan2(np.cos(theta)/eta, np.sin(theta)*np.sin(phi)/eta)

def local2global(delta, alpha):
    mu = np.sqrt(1 - np.square(np.sin(delta)*np.sin(alpha)))
    return -np.arctan2(-mu, np.sin(delta)*np.sin(alpha)), np.arctan2(-np.sin(delta)*np.cos(alpha)/mu, np.cos(delta)/mu)+np.pi


phiss, thetass = np.meshgrid(phis, thetas)
deltass, alphass = global2local(thetass, phiss)



def relativisticAbberation(delta, v):
    cosd = np.cos(delta)
    return np.arccos((cosd-v)/(1-v*cosd))


def getSRindices(v):
    SRdeltass = relativisticAbberation(deltass, v)
    SRthetass, SRphiss = local2global(SRdeltass, alphass)
    return np.array([SRthetass/np.pi * videoFormat[0], SRphiss/(2*np.pi) * videoFormat[1]]).astype('float32')


v = 0
SRind = getSRindices(v)


while(video.isOpened()):
    ret, frame = video.read()
    SRframe = cv2.remap(frame, SRind[1], SRind[0], cv2.INTER_CUBIC)

    #gray = cv2.cvtColor(SRframe, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame', SRframe)

    k = cv2.waitKey(1)

    if k == ord('q'):
        break
    elif k == ord('r'):
        v = 0
        print(v)
        SRind = getSRindices(v)
    elif k == ord('+'):
        v += (1-v)*0.1
        print(v)
        SRind = getSRindices(v)
    elif k == ord('-'):
        v -= (1-v)*0.1
        print(v)
        SRind = getSRindices(v)

video.release()
cv2.destroyAllWindows()