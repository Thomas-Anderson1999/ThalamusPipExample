import numpy as np
import json

def getGroundTruth(filename):
    res = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            #print(line)
            tmpLins = line.split("\t")
            res.append([float(tmp) for tmp in tmpLins])
    return np.array(res)

def getMetadata(datasetPath, filename):
    try:
        with open(datasetPath+filename, "r") as fpjson:
            datasetMeta = json.load(fpjson)
            #print(datasetMeta)

            image_FileName = datasetPath + datasetMeta["image"]
            groundtruth_Filename = datasetPath + datasetMeta["groundtruth"]
            depth_Filename = datasetPath + datasetMeta["depthmapFile"]
            IMULog = datasetPath + datasetMeta["IMULog"]
            MotionContolLog = datasetPath + datasetMeta["MotionControlLog"]
            RoverCmdLog = datasetPath + datasetMeta["RoverCmd"]
            depth_Width = datasetMeta["DepthWidth"]
            depth_Height = datasetMeta["DepthHeight"]
            #print(image_FileName, groundtruth_Filename, depth_Filename, depth_Width, depth_Height)
            return image_FileName, groundtruth_Filename, depth_Filename, IMULog, MotionContolLog, RoverCmdLog, depth_Width, depth_Height
    except:
        return None, None, None, None, None

def getTextData(filename):
    with open(filename, "r") as fpLog:
        Types = [] #0:str, 1:int 2:float
        res = []
        while True:
            line = fpLog.readline()
            if not line:
                break
            #print(line)

            if line.find(' ') != -1:
                line = line.split()
            elif line.find('\t') != -1:
                line = line.split()

            #+ First Line Analysis to get type
            if len(Types) == 0:
                for word in line:
                    try:
                        tmpStr = float(word)
                        if word.find('.') != -1:
                            Types.append(2)
                        else:
                            Types.append(1)
                        res.append([])
                    except:
                        Types.append(0)
                        res.append([])
            # - First Line Analysis to get type

            for idx, word in enumerate(line):
                if Types[idx] == 0:
                    res[idx].append(word)
                elif Types[idx] == 1:
                    res[idx].append(int(word))
                elif Types[idx] == 2:
                    res[idx].append(float(word))
            #print(Types)
            #break
        for idx, type in enumerate(Types):
            if type != 0:
                res[idx] = np.array(res[idx])

        return res
    return None



################################################################



class cInterval:
    def __init__(self):
        self.startIdx = 0 #멈춰있는 기간을 포함한 시작점
        self.endIdx = 0 #멈춰있는 기간을 포함한 끝점
        self.ActionType = "none" #MV, RT, STOP
        self.ActionValue = 0 #실제로 간 거리
        self.AccTime = 0
        self.AccSpd = 0
        self.preIdx = 0
        self.ActualMvIdx = -1    # 실제로 움직이기 시작하는 idx
        self.ActualStopIdx = -1  # 실제로 멈춘 idx

    def show(self):
        print(self.startIdx, self.endIdx, self.preIdx, self.ActionType, self.ActionValue, self.AccTime, self.AccSpd)
def getPeriodfromRobotCmd(RoverCmdLog, preIndx, endIdx):
    res = []
    lens = len(RoverCmdLog[0])
    for i in range(lens):
        res.append(cInterval())
        if RoverCmdLog[0][i] - preIndx < 0:
            res[i].startIdx = 0
        else:
            res[i].startIdx = RoverCmdLog[0][i] - preIndx

        res[i].ActionType = RoverCmdLog[2][i]
        res[i].AccTime = RoverCmdLog[3][i]
        res[i].AccSpd = RoverCmdLog[4][i]
        res[i].ActionValue = RoverCmdLog[5][i]
        res[i].preIdx = preIndx

        res[i].endIdx = endIdx #update in next index
        if i != 0 :
            res[i-1].endIdx = res[i].startIdx
    return res