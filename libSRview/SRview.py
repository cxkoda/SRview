import numpy as np
import cv2


class SRview:

    def __init__(self, frameShape):
        self.frameShape = frameShape
        self.displayAbberationFlag = True

        self.thetas = np.linspace(0, np.pi, frameShape[0])
        self.phis = np.linspace(0, 2 * np.pi, frameShape[1])
        self.phiss, self.thetass = np.meshgrid(self.phis, self.thetas)
        self.deltass, self.alphass = self.global2local(self.thetass, self.phiss)

        self.setSpeed(0)

    def global2local(self, theta, phi):
        eta = np.sqrt(1 - np.square(np.sin(theta)*np.cos(phi)))
        return np.arctan2(eta, -np.sin(theta)*np.cos(phi)), np.arctan2(np.cos(theta)/eta, np.sin(theta)*np.sin(phi)/eta)

    def local2global(self, delta, alpha):
        mu = np.sqrt(1 - np.square(np.sin(delta)*np.sin(alpha)))
        return -np.arctan2(-mu, np.sin(delta)*np.sin(alpha)), np.arctan2(-np.sin(delta)*np.cos(alpha)/mu, np.cos(delta)/mu)+np.pi

    def relativisticAbberation(self, delta, v):
        cosd = np.cos(delta)
        return np.arccos((cosd-v)/(1-v*cosd))

    def computeAbberatedIndices(self):
        self.SRdeltass = self.relativisticAbberation(self.deltass, self.v)
        self.SRthetass, self.SRphiss = self.local2global(self.SRdeltass, self.alphass)
        self.abberatedIndices = np.array([self.SRthetass / np.pi * self.frameShape[0], self.SRphiss / (2 * np.pi) * self.frameShape[1]]).astype('float32')

    def setSpeed(self, v):
        self.v = v
        self.computeAbberatedIndices()

    def displayAbberation(self, flag):
        self.displayAbberationFlag = flag

    def __call__(self, frame):
        SRframe = frame

        if self.displayAbberationFlag:
            SRframe = cv2.remap(SRframe, self.abberatedIndices[1], self.abberatedIndices[0], cv2.INTER_CUBIC)
        return SRframe
