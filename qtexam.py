
import sys
import cv2
import os
import numpy as np
import time
import math

from ThalamusDSloader import *
from ThalamusEngine.Interface import *
from cvMatching import get_SIFT_mathching, show_matching

#+UI
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
#-UI

import sys
from PyQt5.QtWidgets import QApplication, QWidget


class Window(QWidget):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        mainGrid = QGridLayout()

        label = [["ScriptFile:", "EngineName:"]]
        editDefault = [["Script.txt", "Thalamus QT Example"]]
        buttonText = ["Engine Start"]
        buttonFunc = [self.InitEngine]
        subgrid, self.startEdit = self.createGroupBox("Global Coord Test", label, editDefault, buttonText, buttonFunc)
        mainGrid.addWidget(subgrid, 0, 0)

        label = [["PosX", "PosY", "PosZ", "AttX", "AttY", "AttZ"]]
        editDefault = [["0", "0", "0", "0", "0", "0"]]
        buttonText = ["Get Global", "Pos Set", "Att Set", "Pos/Att Set", "BirdView"]
        buttonFunc = [self.getGlobal, self.globalPosSet, self.globalAttSet, self.globalPosAttSet, self.globalBirdview]
        subgrid, self.globalCoordEdit = self.createGroupBox("Global Coord Test", label, editDefault, buttonText, buttonFunc)
        mainGrid.addWidget(subgrid, 1, 0)

        label = [["ObjID", "TypeID", "ObjNAme"],["PosX", "PosY", "PosZ", "AttX", "AttY", "AttZ"], ["ClrX", "ClrY", "ClrZ", "AmpX", "AmpY", "AmpZ"]]
        editDefault = [["-1", "0", ""], ["0", "0", "0", "0", "0", "0"], ["0", "0", "0", "0", "0", "0"]]
        buttonText = ["objGetParam", "Type Set", "Name Set", "Pos Set", "Att Set", "Clr Set", "Amp Set", "Whole Set"]
        buttonFunc = [self.objGetParam,self.objSetType,self.objSetName,self.objSetPos,self.objSetAtt,self.objSetClr,self.objSetAmp,self.objSetParam]
        subgrid, self.objControlEdit = self.createGroupBox("Object Control", label, editDefault, buttonText, buttonFunc)
        mainGrid.addWidget(subgrid, 2, 0)

        label = [["ObjID", "ModelID", "Offset"], ["PosX", "PosY", "PosZ", "AttX", "AttY", "AttZ"]]
        editDefault = [["-1", "0", "-1"], ["0", "0", "0", "0", "0", "0"]]
        buttonText = ["MoelGetParam", "Param Set"]
        buttonFunc = [self.mdlGetParam, self.mdlSetParam]
        subgrid, self.mdlControlEdit = self.createGroupBox("Modeiling Control", label, editDefault, buttonText, buttonFunc)
        mainGrid.addWidget(subgrid, 3, 0)

        label = [["SrcPosX", "SrcPosY", "SrcWidth", "SrcHeight", "DestWidth", "DestHeight"], ["ObjID", "CPU Core"]]
        editDefault = [["0", "0", "1280", "720", "300", "300"], ["-1", "12"]]
        buttonText = ["DepthMap", "ColorMap", "NoShade", "LightEff", "Bounding Box", "Rasterizing", "VideoDataSet"]
        buttonFunc = [self.funcDepthMap, self.funcColorMap, self.funcNoShade, self.funcLightEffect, self.funcBBox, self.funcRasterize, self.VideoDataSet]
        subgrid, self.func1Edit = self.createGroupBox("Scene Generation", label, editDefault, buttonText, buttonFunc)
        mainGrid.addWidget(subgrid, 4, 0)

        label = [["DepthMap:", "Width", "Height", "MeshUp Inv", "FreeModelNum", "Thread"],["ColorImg:", "SeqDataset", "meshupIdx","overayCnt"]]
        editDefault = [["Dataset/Dataset03/DepthBin03.txt","300", "300", "9", "5", "12"],["Dataset/Dataset03/Color03.png", "Dataset/DATASet_dronetest/","0","15"]]
        buttonText = ["MeshUp", "Texture Overay", "Texure Int", "TextureView", "TextureView_subcam", "bulkDS overlay", "Save Recon", "Load Recon", "compare recon" ]
        buttonFunc = [self.func2MeshUp, self.func2TexOveray, self.func2TexInt, self.func2TexView, self.func2TexView_subcam,
                      self.func2bulkDsOverlay, self.func2saveRecon, self.func2loadRecon, self.func2compareRecon]
        subgrid, self.func2Edit = self.createGroupBox("Mesh up, Texture Overay", label, editDefault, buttonText, buttonFunc)
        mainGrid.addWidget(subgrid, 5, 0)

        self.setLayout(mainGrid)
        self.setWindowTitle("Thalamus Engine UI")
        self.meshup_pose = [0,0,0,0,0,0]
        self.resize(600, -1)


    def func2compareRecon(self):
        SetGlobalPosition(0, 0, -900)
        SetGlobalAttitude(0,24, 0)
        InitializeRenderFacet(-1, -1)

        #+get Current Texture view
        TheadNum = int(self.func2Edit[5].text())
        SrcPosX, SrcPosY, SrcWidth, SrcHeight, DestWidth, DestHeight, ObjID, CPUCore = self.getFunc1Param()
        TextuedView = np.zeros((DestHeight, DestWidth, 3), np.uint8)

        getTextureImg(TheadNum, TextuedView.ctypes, SrcPosX, SrcPosY, SrcWidth, SrcHeight, DestWidth, DestHeight, ObjID)
        TextuedView = cv2.resize(TextuedView, (300, 300), interpolation=cv2.INTER_AREA)
        TextuedView = cv2.cvtColor(TextuedView, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Texture View", TextuedView)
        # +get Current Texture view

        TargetFrame = 750
        cap = cv2.VideoCapture("Dataset/DATASet_recon2/img.avi")
        cap.set(cv2.CAP_PROP_POS_FRAMES, TargetFrame)
        success, TargeImage = cap.read()
        TargeImage = cv2.resize(TargeImage, (300, 300), interpolation=cv2.INTER_AREA)
        TargeImage = cv2.cvtColor(TargeImage, cv2.COLOR_BGR2GRAY)

        cv2.imshow("Target Image", TargeImage)

        #+matching
        matching = get_SIFT_mathching(TargeImage, TextuedView)

        filt_matching = []
        for matching in matching:
            if math.fabs(matching[0][1] - matching[1][1]) < 10:
                filt_matching.append(matching)

        resimg = show_matching(TargeImage, TextuedView, filt_matching)
        cv2.imshow("resimg", resimg)
        #-matching

        Depth_Map = np.zeros((300, 300), np.float32)
        Depth_Mask = np.zeros((300, 300, 3), np.uint8)
        if 0 != LoadBinDepthMapPnt("Dataset/DATASet_recon2/DepthMap.bin", 300, 300, 0, 10000, Depth_Map.ctypes, Depth_Mask.ctypes, TargetFrame):

            imgSzX = 1280
            imgSzY = 720
            avg_tgt = np.array([0., 0., 0.])
            avg_tex = np.array([0., 0., 0.])
            cnt = 0
            for matching in filt_matching:
                cnt += 1
                targetViewPnt = matching[0]
                tgtdepth = Depth_Map[int(targetViewPnt[1])][int(targetViewPnt[0])]
                tgtX = targetViewPnt[0] * imgSzX / 300
                tgtY = targetViewPnt[1] * imgSzY / 300
                tgt3d = Pixelto3D(tgtX, tgtY, tgtdepth)
                avg_tgt += np.array(tgt3d)

                textViewPnt = matching[1]
                tex_viewX = textViewPnt[0] * imgSzX / 300
                tex_viewY = textViewPnt[1] * imgSzY / 300
                tmpdist, _, _, _, _, _ = ReturnDistance(tex_viewX, tex_viewY)
                texPnt = Pixelto3D(tex_viewX, tex_viewY, tmpdist)
                avg_tex += np.array(texPnt)
                #print(tgt3d, texPnt)

            avg_tgt /= cnt
            avg_tex /= cnt

            unit_tgt = avg_tgt / np.sqrt(np.sum(avg_tgt * avg_tgt))
            unit_tex = avg_tex / np.sqrt(np.sum(avg_tex * avg_tex))

            print(cnt, avg_tgt, avg_tex, avg_tgt - avg_tex, math.acos(np.sum(unit_tgt*unit_tex)) / math.pi * 180)
        else:
            print("error")


    def func2saveRecon(self):
        cmdIdx = self.func2Edit[8].text()
        SaveReconstruction(5, "recon"+cmdIdx+".bin", self.meshup_pose)
    def func2loadRecon(self):
        print("GetCameraSize", GetCameraSize(-1))
        print("GetCameraSize", GetCameraSize(0))

        cmdIdx = self.func2Edit[8].text()
        res = LoadReconstruction(5, "recon"+cmdIdx+".bin")
        print(res)
        pose = res[1]
        setModelPosRot(1, pose[0], pose[1], pose[2], 0, 0, 0)
        setModelPosRot(2, 0, 0, 0, pose[3], pose[5], pose[4])

        InitializeRenderFacet(-1, -1)

    def func2bulkDsOverlay(self):
        datasetPath = self.func2Edit[7].text()
        cmdIdx = int(self.func2Edit[8].text())
        overayCnt = int(self.func2Edit[9].text())

        #+dataset Loading
        image_FileName, groundtruth_Filename, depth_Filename, IMULog, MotionContolLog, RoverCmdLog, depth_Width, depth_Height = getMetadata(datasetPath=datasetPath, filename="meta.json")
        RoverCmd = getTextData(RoverCmdLog)
        McLog = getTextData(MotionContolLog)
        # -dataset Loading

        # + Robot Cmd Log Analysis
        cmdPeriod = getPeriodfromRobotCmd(RoverCmd, 60, len(McLog[0]))
        for period_idx, period in enumerate(cmdPeriod):
            for mcIdx in range(period.startIdx, period.endIdx):
                if McLog[1][mcIdx] != 0:  # 0:Stop, 1:Move, 2:Rotation
                    if cmdPeriod[period_idx].ActualMvIdx == -1:
                        cmdPeriod[period_idx].ActualMvIdx = mcIdx
                    if cmdPeriod[period_idx].ActualStopIdx < mcIdx:
                        cmdPeriod[period_idx].ActualStopIdx = mcIdx
            period.show()
        # - Robot Cmd Log Analysis


        if image_FileName != None:
            imgcnt = 0
            GroundTruth = getGroundTruth(groundtruth_Filename)
            ThreadNum = 6

            prcCnt = 0
            cap = cv2.VideoCapture(image_FileName)
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    print("Dataset Complete")
                    break

                if imgcnt < cmdPeriod[cmdIdx].ActualMvIdx:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, cmdPeriod[cmdIdx].ActualMvIdx)
                    imgcnt = cmdPeriod[cmdIdx].ActualMvIdx

                    self.meshup_pose = GroundTruth[imgcnt]

                    # +Mesh up
                    depInv = int(self.func2Edit[3].text())
                    MeshUpType = int(self.func2Edit[4].text())
                    Depth_Map = np.zeros((depth_Height, depth_Width), np.float32)
                    Depth_Mask = np.zeros((depth_Height, depth_Width, 3), np.uint8)
                    if 0 != LoadBinDepthMapPnt(depth_Filename, depth_Width, depth_Height, 0, 10000, Depth_Map.ctypes, Depth_Mask.ctypes, imgcnt):
                        ret = ObjMeshUp(depth_Width, depth_Height, MeshUpType, depInv)
                        print("ObjMeshUp:", ret)
                        InitializeRenderFacet(-1, -1)
                    # +Mesh up

                    # +store current mesh position
                    px = GroundTruth[imgcnt][0]
                    py = GroundTruth[imgcnt][1]
                    pz = GroundTruth[imgcnt][2]
                    ax = GroundTruth[imgcnt][3]
                    ay = GroundTruth[imgcnt][5]
                    az = GroundTruth[imgcnt][4]
                    # -store current mesh position

                    setModelPosRot(1, px, py, pz, 0, 0, 0)
                    setModelPosRot(2, 0, 0, 0, ax, ay, az)  # 순서 중의, y축의 회전의 yaw이다

                    continue

                if cmdPeriod[cmdIdx].ActualStopIdx < imgcnt:
                    break

                print("imgcnt:", imgcnt, "(GT)x,y,z,r,p,y:", GroundTruth[imgcnt][0], GroundTruth[imgcnt][1], GroundTruth[imgcnt][2], GroundTruth[imgcnt][3], GroundTruth[imgcnt][4], GroundTruth[imgcnt][5])
                SetGlobalPosition(-GroundTruth[imgcnt][0], -GroundTruth[imgcnt][1], -GroundTruth[imgcnt][2])
                SetGlobalAttitude(-GroundTruth[imgcnt][3], -GroundTruth[imgcnt][5], -GroundTruth[imgcnt][4])
                InitializeRenderFacet(-1, -1)

                imgcnt += 1
                cv2.imshow('image', image)

                h, w, _ = image.shape
                TexureOveray(ThreadNum, image.ctypes, w, h, w, h)

                if cv2.waitKey(1) & 0xFF == 27:
                    break
                if overayCnt == prcCnt:
                    break
                prcCnt += 1

            cap.release()
        else:
            print("Error on dataset")
        print("meshup complete")


    def createGroupBox(self, gbxName, labeltext, editDefault, buttonText, buttonFunc):
        groupBox = QGroupBox(gbxName)
        grid = QGridLayout()
        groupBox.setLayout(grid)

        editList = []
        for j in range(len(labeltext)):
            k = 0
            for i in range(len(labeltext[j])):
                label = QLabel(self)
                label.setText(labeltext[j][i])
                grid.addWidget(label, j, k)
                k += 1

                edit = QLineEdit(self)
                edit.setText(editDefault[j][i])
                grid.addWidget(edit, j, k)
                editList.append(edit)
                k += 1

        for i in range(len(buttonText)):
            btn = QPushButton(buttonText[i], self)
            btn.clicked.connect(buttonFunc[i])
            grid.addWidget(btn, len(labeltext), i)

        return groupBox, editList

    def InitEngine(self):
        AsmFileName = self.startEdit[0].text().encode('UTF-8')
        SimWindowText = self.startEdit[1].text().encode('UTF-8')
        if True == LoadThalamusInterface():
            errCode = InitEngine(AsmFileName)
            if errCode != 0:
                errMsg = ""
                if errCode & 1 != 0:
                    errMsg += "env.txt "
                if errCode & 2 != 0:
                    errMsg += "script"
                QMessageBox.about(self, "Initialize Error:"+str(errCode), "Error On " + errMsg)

            StartExt3DEngine(AsmFileName, SimWindowText)
        else:
            OnMsgText("Error on Loading Library")

    #+Global Coord Button Func
    def getGlobal(self):
        px, py, pz = GetGlobalPos()
        ax, ay, az = GetGlobalAtt()
        self.globalCoordEdit[0].setText(str(px))
        self.globalCoordEdit[1].setText(str(py))
        self.globalCoordEdit[2].setText(str(pz))
        self.globalCoordEdit[3].setText(str(ax))
        self.globalCoordEdit[4].setText(str(ay))
        self.globalCoordEdit[5].setText(str(az))

    def globalPosSet(self):
        x = float(self.globalCoordEdit[0].text())
        y = float(self.globalCoordEdit[1].text())
        z = float(self.globalCoordEdit[2].text())
        SetGlobalPosition(x,y,z)
        InitializeRenderFacet(-1, -1)
    def globalAttSet(self):
        x = float(self.globalCoordEdit[3].text())
        y = float(self.globalCoordEdit[4].text())
        z = float(self.globalCoordEdit[5].text())
        SetGlobalAttitude(x, y, z)
        InitializeRenderFacet(-1, -1)
    def globalPosAttSet(self):
        self.globalPosSet()
        self.globalAttSet()
    def globalBirdview(self):
        self.globalCoordEdit[1].setText("8000")
        self.globalCoordEdit[2].setText("-3000")
        self.globalCoordEdit[3].setText("90")
        self.globalPosAttSet()

    #-Global Coord Button Func

    #+Obj Control
    def objGetParam(self):
        objID = GetHighLightedObj()
        if -1 != objID:
            self.objControlEdit[0].setText(str(objID))
            self.objControlEdit[1].setText(str(GetObjType(objID)))
            self.objControlEdit[2].setText(GetObjName(objID))
            x,y,z = GetObjPos(objID)
            self.objControlEdit[3].setText(str(x))
            self.objControlEdit[4].setText(str(y))
            self.objControlEdit[5].setText(str(z))
            x, y, z = GetObjAtt(objID)
            self.objControlEdit[6].setText(str(x))
            self.objControlEdit[7].setText(str(y))
            self.objControlEdit[8].setText(str(z))
            x, y, z = GetObjClr(objID)
            self.objControlEdit[9].setText(str(x))
            self.objControlEdit[10].setText(str(y))
            self.objControlEdit[11].setText(str(z))
            x, y, z = GetObjAmp(objID)
            self.objControlEdit[12].setText(str(x))
            self.objControlEdit[13].setText(str(y))
            self.objControlEdit[14].setText(str(z))
    def objSetType(self):
        objID = int(self.objControlEdit[0].text())
        if objID == -1:
            type = int(self.objControlEdit[1].text())
            SetObjectType(objID, type)
            InitializeRenderFacet(-1, -1)
            InitializeRenderFacet(-1, -1)
    def objSetName(self):
        print("sss")
        objID = int(self.objControlEdit[0].text())
        if objID != -1:
            SetObjName(objID, self.objControlEdit[2].text())
    def objSetPos(self):
        objID = int(self.objControlEdit[0].text())
        if objID != -1:
            x = float(self.objControlEdit[3].text())
            y = float(self.objControlEdit[4].text())
            z = float(self.objControlEdit[5].text())
            SetObjPos(objID, x, y, z)
            InitializeRenderFacet(-1, -1)
    def objSetAtt(self):
        objID = int(self.objControlEdit[0].text())
        if objID != -1:
            x = float(self.objControlEdit[6].text())
            y = float(self.objControlEdit[7].text())
            z = float(self.objControlEdit[8].text())
            SetObjAtt(objID, x, y, z)
            InitializeRenderFacet(-1, -1)
    def objSetClr(self):
        objID = int(self.objControlEdit[0].text())
        if objID == -1:
            x = float(self.objControlEdit[9].text())
            y = float(self.objControlEdit[10].text())
            z = float(self.objControlEdit[11].text())
            SetObjClr(objID, x, y, z)
            InitializeRenderFacet(-1, -1)
    def objSetAmp(self):
        objID = int(self.objControlEdit[0].text())
        if objID != -1:
            x = float(self.objControlEdit[12].text())
            y = float(self.objControlEdit[13].text())
            z = float(self.objControlEdit[14].text())
            SetObjAmp(objID, x, y, z)
            InitializeRenderFacet(-1, -1)
    def objSetParam(self):
        self.objSetType()
        self.objSetName()
        self.objSetPos()
        self.objSetAtt()
        self.objSetAmp()
    #-Obj Control

    #+Model Control
    def mdlGetParam(self):
        objID = GetHighLightedObj()
        self.mdlControlEdit[0].setText(str(objID))
        if objID != -1:
            ModelID = getModelIDByObjID(objID)
            if ModelID != -1:
                self.mdlControlEdit[1].setText(str(ModelID))
                Modleffset = int(self.mdlControlEdit[2].text())
                res, data = getModelPosRot(ModelID + Modleffset)
                if res != 0:
                    self.mdlControlEdit[3].setText(str(data[0]))
                    self.mdlControlEdit[4].setText(str(data[1]))
                    self.mdlControlEdit[5].setText(str(data[2]))
                    self.mdlControlEdit[6].setText(str(data[3]))
                    self.mdlControlEdit[7].setText(str(data[4]))
                    self.mdlControlEdit[8].setText(str(data[5]))


    def mdlSetParam(self):
        objID = GetHighLightedObj()
        self.mdlControlEdit[0].setText(str(objID))
        if objID != -1:
            ModelID = getModelIDByObjID(objID)
            if ModelID != -1:
                self.mdlControlEdit[1].setText(str(ModelID))
                Modleffset = int(self.mdlControlEdit[2].text())
                px = float(self.mdlControlEdit[3].text())
                py = float(self.mdlControlEdit[4].text())
                pz = float(self.mdlControlEdit[5].text())
                ax = float(self.mdlControlEdit[6].text())
                ay = float(self.mdlControlEdit[7].text())
                az = float(self.mdlControlEdit[8].text())
                setModelPosRot(ModelID + Modleffset, px, py, pz, ax, ay, az)
                InitializeRenderFacet(-1,-1)
    #-Model Control
    #+Function 1
    def getFunc1Param(self):
        SrcPosX = int(self.func1Edit[0].text())
        SrcPosY = int(self.func1Edit[1].text())
        SrcWidth = int(self.func1Edit[2].text())
        SrcHeight = int(self.func1Edit[3].text())
        DestWidth = int(self.func1Edit[4].text())
        DestHeight = int(self.func1Edit[5].text())
        ObjID = int(self.func1Edit[6].text())
        CPUCore = int(self.func1Edit[7].text())
        return SrcPosX, SrcPosY, SrcWidth, SrcHeight, DestWidth, DestHeight, ObjID, CPUCore
    def funcDepthMap(self):
        print("depth map")

        SrcPosX, SrcPosY, SrcWidth, SrcHeight, DestWidth, DestHeight, ObjID, CPUCore = self.getFunc1Param()

        Depth_Map = np.zeros((DestHeight, DestWidth), np.float32)
        Depth_Mask = np.zeros((DestHeight, DestWidth, 3), np.uint8)

        t0 = time.monotonic()
        GetDepthMap(Depth_Map.ctypes, Depth_Mask.ctypes, DestWidth, DestHeight, CPUCore, SrcPosX, SrcPosY, SrcWidth, SrcHeight, ObjID)
        t1 = time.monotonic() - t0
        print("Time elapsed: ", t1)
        SaveRawSingleDepthFile("DepthMap.bin", Depth_Map)

        ObjIDMask, FaceIDMask, EdgeMask = cv2.split(Depth_Mask)
        Depth_Map = cv2.normalize(Depth_Map, None, alpha=0, beta=1.0, norm_type=cv2.NORM_MINMAX)
        cv2.imshow("Depth Map", Depth_Map)
        cv2.imshow("Depth Mask", EdgeMask)
    def funcColorMap(self):
        SrcPosX, SrcPosY, SrcWidth, SrcHeight, DestWidth, DestHeight, ObjID, CPUCore = self.getFunc1Param()

        Shade_Mask = np.zeros((DestHeight, DestWidth, 3), np.uint8)
        Shade_Img = np.zeros((DestHeight, DestWidth, 3), np.uint8)

        GetShadeImage(Shade_Img.ctypes, Shade_Mask.ctypes, DestWidth, DestHeight, CPUCore, SrcPosX, SrcPosY, SrcWidth, SrcHeight, ObjID)
        cv2.imshow("Shade_Img", Shade_Img)

    def funcNoShade(self):
        SrcPosX, SrcPosY, SrcWidth, SrcHeight, DestWidth, DestHeight, ObjID, CPUCore = self.getFunc1Param()

        Shade_Mask = np.zeros((DestHeight, DestWidth, 3), np.uint8)
        Shade_Img = np.zeros((DestHeight, DestWidth, 3), np.uint8)

        GetColorImageNoShade(Shade_Img.ctypes, Shade_Mask.ctypes, DestWidth, DestHeight, CPUCore, SrcPosX, SrcPosY, SrcWidth, SrcHeight)
        cv2.imshow("Shade_Img", Shade_Img)
    def funcLightEffect(self):
        print("sss")

    def funcRasterize(self):
        SrcPosX, SrcPosY, SrcWidth, SrcHeight, DestWidth, DestHeight, ObjID, CPUCore = self.getFunc1Param()
        Color_width = DestWidth
        Color_Height = DestHeight

        Color_image = np.zeros((Color_Height, Color_width, 3), np.uint8)
        Depth_Map = np.zeros((Color_Height, Color_width), np.float32)
        Depth_Mask = np.zeros((Color_Height, Color_width, 3), np.uint8)

        InitializeRenderFacet(-1, -1)  # refresh

        GetRasterizedImage(Color_image.ctypes, Depth_Map.ctypes, Depth_Mask.ctypes,
                           Color_width, Color_Height, CPUCore, SrcPosX, SrcPosY, SrcWidth, SrcHeight, ObjID)
        cv2.imshow("Rasterizing Color Image", Color_image)

        ObjIDMask, FaceIDMask, EdgeMask = cv2.split(Depth_Mask)
        Depth_Map = cv2.normalize(Depth_Map, None, alpha=0, beta=1.0, norm_type=cv2.NORM_MINMAX)
        cv2.imshow("Depth Map", Depth_Map)
        cv2.imshow("Depth Mask", EdgeMask)

    def VideoDataSet(self):
        SrcPosX, SrcPosY, SrcWidth, SrcHeight, _, _, ObjID, CPUCore = self.getFunc1Param()

        DestWidth = 256
        DestHeight = 256
        Depth_Map = np.zeros((DestHeight, DestWidth), np.float32)
        Depth_Mask = np.zeros((DestHeight, DestWidth, 3), np.uint8)
        fp_depth = open("vid_dataset/DepthMap.bin", "wb")

        vid_width = 512
        vid_height = 512
        output_filename = "vid_dataset/img.avi"
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(output_filename, fourcc, 30, (vid_width, vid_height))
        Shade_Mask = np.zeros((vid_height, vid_width, 3), np.uint8)
        Shade_Img = np.zeros((vid_height, vid_width, 3), np.uint8)

        if not writer.isOpened():
            raise Exception("Can't open video file")

        f_log = open("vid_dataset/fwLog.txt", "w")
        f_log.write("sr: 0 Int MV 1 2500 -11600\n")

        for imgcnt, z_pos in enumerate(range(1000, 0, -10)):
            self.globalCoordEdit[2].setText(str(z_pos))
            self.globalPosAttSet()

            GetShadeImage(Shade_Img.ctypes, Shade_Mask.ctypes, vid_width, vid_height, CPUCore, SrcPosX, SrcPosY, SrcWidth, SrcHeight, ObjID)
            writer.write(Shade_Img)
            cv2.imshow("Shade_Img", Shade_Img)

            GetDepthMap(Depth_Map.ctypes, Depth_Mask.ctypes, DestWidth, DestHeight, CPUCore, SrcPosX, SrcPosY, SrcWidth, SrcHeight, ObjID)
            fp_depth.write(Depth_Map.astype(np.float32).tobytes())

            Depth_Map = cv2.normalize(Depth_Map, None, alpha=0, beta=1.0, norm_type=cv2.NORM_MINMAX)
            cv2.imshow("Depth Map", Depth_Map)

            enc = int(11600 * imgcnt / 100)
            f_log.write(f"sr: {imgcnt} PF>{enc}	{enc}	-5	5	-212	149	2	0	\n")
            cv2.waitKey(1)
            print("image:", imgcnt)

        f_log.write(f"sr: {imgcnt} Int EN -1 1\n")
        writer.release()
        fp_depth.close()
        print("complete")

    def funcBBox(self):
        print("Bound Box")
        MaxBoundBoxNum = 128
        BoundBox = np.zeros(MaxBoundBoxNum * 4, np.int32)
        BoundBoxNum = GetBoundBox(BoundBox.ctypes)
        print("BBNum " + str(BoundBoxNum))
        SrcPosX, SrcPosY, SrcWidth, SrcHeight, DestWidth, DestHeight, ObjID, CPUCore = self.getFunc1Param()

        BoundBoxImg = np.zeros((SrcHeight,SrcWidth, 3), np.uint8)
        GetColorImage(BoundBoxImg.ctypes, SrcWidth, SrcHeight)
        for i in range(BoundBoxNum):
            x1 = BoundBox[4 * i + 0]
            x2 = BoundBox[4 * i + 1]
            y1 = BoundBox[4 * i + 2]
            y2 = BoundBox[4 * i + 3]
            print("BoundBox : {0} {1} {2} {3}".format(x1, y1, x2, y2))
            cv2.rectangle(BoundBoxImg, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=1, lineType=cv2.LINE_4,
                          shift=0)
        cv2.imshow("BoundBox", BoundBoxImg)
    # -Function 1

    #+Function 2
    #buttonFunc = [self.func2MeshUp, self.func2TexOveray, self.func2TexInt, self.func2TexView]
    def func2MeshUp(self):

        depWidth = int(self.func2Edit[1].text())
        depHeight = int(self.func2Edit[2].text())
        depInv = int(self.func2Edit[3].text())
        MeshUpType = int(self.func2Edit[4].text())

        Depth_Map = np.zeros((depHeight, depWidth), np.float32)
        Depth_Mask = np.zeros((depHeight, depWidth, 3), np.uint8)

        if 0 != LoadBinDepthMapPnt(self.func2Edit[0].text(), depWidth, depHeight, 600, 6000, Depth_Map.ctypes, Depth_Mask.ctypes):
            Depth_Map = cv2.normalize(Depth_Map, None, alpha=0, beta=1.0, norm_type=cv2.NORM_MINMAX)
            cv2.imshow("Depth Map", Depth_Map)
            ret = ObjMeshUp(depWidth, depHeight, MeshUpType, depInv)
            print("ObjMeshUp:", ret)
            InitializeRenderFacet(-1, -1)
        else:
            print("Loading Error")
    def func2TexOveray(self):
        depWidth = int(self.func2Edit[1].text())
        depHeight = int(self.func2Edit[2].text())
        TheadNum = int(self.func2Edit[5].text())
        Texture = cv2.imread(self.func2Edit[6].text())
        Texture = cv2.resize(Texture, (depWidth, depHeight))
        cv2.imshow("Texture Src", Texture)

        _, _, SrcWidth, SrcHeight, _, _, _, _ = self.getFunc1Param()
        TexureOveray(TheadNum, Texture.ctypes, depWidth, depHeight, SrcWidth, SrcHeight)
    def func2TexInt(self):
        TheadNum = int(self.func2Edit[5].text())
        TextureInterpolation(TheadNum)
        print("Interpolation")

    def func2TexView(self):
        TheadNum = int(self.func2Edit[5].text())
        SrcPosX, SrcPosY, SrcWidth, SrcHeight, DestWidth, DestHeight, ObjID, CPUCore = self.getFunc1Param()
        TextuedView = np.zeros((DestHeight, DestWidth, 3), np.uint8)

        getTextureImg(TheadNum, TextuedView.ctypes, SrcPosX, SrcPosY, SrcWidth, SrcHeight, DestWidth, DestHeight, ObjID)
        cv2.imshow("Texture View", TextuedView)

    def func2TexView_subcam(self):
        TheadNum = int(self.func2Edit[5].text())
        SrcPosX, SrcPosY, SrcWidth, SrcHeight, DestWidth, DestHeight, ObjID, CPUCore = self.getFunc1Param()
        TextuedView = np.zeros((DestHeight, DestWidth, 3), np.uint8)

        SetDisplayCamera(-1)
        getTextureImg(TheadNum, TextuedView.ctypes, SrcPosX, SrcPosY, SrcWidth, SrcHeight, DestWidth, DestHeight, ObjID)
        cv2.imshow("Texture View Main view", TextuedView)

        SetDisplayCamera(0) #960, 720
        getTextureImg(TheadNum, TextuedView.ctypes, SrcPosX, SrcPosY, 960, SrcHeight, DestWidth, DestHeight, ObjID)
        cv2.imshow("Texture View Sub View", TextuedView)


    #-Function 2
if __name__ == '__main__':
    print(cv2.__version__)
    print(os.getcwd())

    app = QApplication(sys.argv)
    clock = Window()
    clock.show()
    sys.exit(app.exec_())

