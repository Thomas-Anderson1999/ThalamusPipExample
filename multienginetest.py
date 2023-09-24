

import sys
import cv2
import os
import numpy as np
import time

from ThalamusEngine.Interface import *


if __name__ == '__main__':
    print(cv2.__version__)
    print(os.getcwd())

    AsmFileName = b"Script.txt"
    SimWindowText = b"GL Exam1"
    InitSimulation(AsmFileName, SimWindowText)

    AsmFileName = b"ScriptRover.txt"
    InitEngine(AsmFileName, 1280, 720, 1)

    Key = ord('z')
    while True:
        if Key == ord('a'):
            SetProcessingEngineIndex(0)
        if Key == ord('b'):
            SetProcessingEngineIndex(1)

        if Key == ord('z'):
            DestHeight = 300
            DestWidth = 300

            Depth_Map = np.zeros((DestHeight, DestWidth), np.float32)
            Depth_Mask = np.zeros((DestHeight, DestWidth, 3), np.uint8)

            t0 = time.monotonic()
            GetDepthMap(Depth_Map.ctypes, Depth_Mask.ctypes, DestWidth, DestHeight, 12, 0, 0, 1280, 720, -1)
            t1 = time.monotonic() - t0
            print("Time elapsed: ", t1)

            ObjIDMask, FaceIDMask, EdgeMask = cv2.split(Depth_Mask)
            Depth_Map = cv2.normalize(Depth_Map, None, alpha=0, beta=1.0, norm_type=cv2.NORM_MINMAX)
            cv2.imshow("Depth MapB", Depth_Map)
            cv2.imshow("Depth MaskB", EdgeMask)

        Key = cv2.waitKey(30)


